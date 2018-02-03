from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
import socket
import re
import sys
import traceback
import sqlite3


class Master:

    def __init__(self, host, port, config):
        self.host = host
        self.port = int(port)

        self.sock = socket.socket()
        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print('Bind failed.' + str(sys.exc_info()))
            exit(1)

        with open(config) as file:
            read_data = file.read()
        read_data = re.split('\n\n', read_data)

        ip_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        addr_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')

        node_addr = re.search(addr_pattern, read_data[0])[0]
        node_port = int(re.split(":", node_addr)[1])

        print(node_port)

        # Get a list containing socket connections to all datanodes
        self.datanodes = []
        for lines in read_data[2:]:
            ip = re.search(ip_pattern, lines)[0]
            sock = socket.socket()
            sock.connect((ip, node_port))
            self.datanodes.append(sock)

    def listen(self):
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            conn.settimeout(300)
            try:
                Thread(target=self.client_thread, args=(conn,)).start()
            except:
                print("Multiprocessing Error! ")
                traceback.print_exc()

    def client_thread(self, conn):
        master_active = True
        database_conn = None

        # more sophisticated query processing will go here later
        while master_active:
            orders = self.recieve_input(conn)

            if "_quit" in orders:
                conn.close()
                master_active = False
            elif "_use/" in orders:
                db = re.sub("_use/", "", orders)
                self.use(db)
            elif "_ddl/" in orders:
                transaction = re.sub("_ddl/", "", orders)
                self.ddl(transaction)

    def use(self, database):
        message = "_use/" + database
        for nodes in self.datanodes:
            nodes.send(message.encode())

    def quit(self):
        message = "_quit"
        for nodes in self.datanodes:
            nodes.send(message.encode)
            nodes.close()

    def ddl(self, statement):
        message = "_ddl/" + statement
        commit = True
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            for nodes in self.datanodes:
                nodes.send(message)
            futures = [executor.submit(self.recieve_input, nodes) for nodes in self.datanodes]
            for future in as_completed(futures):
                if future.result() == "_failure":
                    commit = False
        for nodes in self.datanodes:
            if commit == True:
                self.transact("_commit")
            else:
                self.transact("_abort")

    def transact(self, status):
        message = status
        for nodes in self.datanodes:
            nodes.send(message.encode())

    def recieve_input(self, conn, BUFFER_SIZE = 1024):
        client_input = conn.recv(BUFFER_SIZE)
        input_size = sys.getsizeof(client_input)

        if input_size > BUFFER_SIZE:
            print("Input exceeds buffer size")

        result = client_input.decode().rstrip()
        return result


if __name__ == '__main__':
    usage = "python3 master.py [host] [port] [config file]"
    if len(sys.argv) != 4:
        print(usage)
        exit(1)
    master = Master(sys.argv[1], sys.argv[2], sys.argv[3])
    print("listern")
    master.listen()