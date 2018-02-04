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
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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

        # Get a list containing socket connections to all datanodes
        self.datanodes = []
        for lines in read_data[2:]:
            ip = re.search(ip_pattern, lines)[0]
            sock = socket.socket()
            sock.connect((ip, node_port))
            print("Connected to : " + ip + ":" + str(node_port))
            self.datanodes.append(sock)

    def listen(self):
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            print("Server: Connection from " + str(addr))
            conn.settimeout(300)
            try:
                Thread(target=self.client_thread, args=(conn,)).start()
            except:
                print("Multiprocessing Error! ")
                traceback.print_exc()

    def client_thread(self, conn):
        client_active = True
        database_conn = None
        catalog = sqlite3.connect("/sqlfat/data/catalog.db")
        # more sophisticated query processing will go here later
        while client_active:
            orders = self.recieve_input(conn)
            # print("received orders:" + orders)
            if "_quit" in orders:
                self.catalog.close()
                response = self.quit()
                client_active = False
            elif "_use/" in orders:
                db = re.sub("_use/", "", orders)
                response = self.use(db)
            elif "_ddl/" in orders:
                transaction = re.sub("_ddl/", "", orders)
                response = self.ddl(transaction, catalog)
            conn.send(response.encode())

    def use(self, database):
        message = "_use/" + database
        for nodes in self.datanodes:
            nodes.send(message.encode())
        return "Using database: " + database

    def quit(self):
        message = "_quit"
        for nodes in self.datanodes:
            nodes.send(message.encode())
            nodes.close()
        return "Closing connection"

    def ddl(self, statement, catalog):
        message = "_ddl/" + statement
        commit = True
        response = ""
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            for nodes in self.datanodes:
                nodes.send(message.encode())
            futures = [executor.submit(self.recieve_input, nodes) for nodes in self.datanodes]
            for future in as_completed(futures):
                result = future.result()
                host = re.split("/", result)[1]
                if "_fail" in future.result():
                    response += "Transaction failure at host: " + host + "\n"
                    commit = False
                elif "_success" in future.result():
                    response += "Transaction success at host: " + host + "\n"
        for nodes in self.datanodes:
            if commit == True:
                self.transact("_commit")
                if "CREATE TABLE" in statement:
                    table = re.split(" ", statement)[2]
                    (host, port) = nodes.getpeername()
                    id = int(re.split("node", "", host))
                    catalog.execute("INSERT INTO dtables (tname, nodeurl, nodeid) "
                                    "VALUES ({}, {}, {})".format(table, host, id))
            else:
                self.transact("_abort")
        if commit == True:
            response += "Committed"
        else:
            response += "Aborted"
        return response

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
    print("Master Up!")
    master.listen()