import socket
from threading import Thread, Lock
import sqlite3
import sys
import traceback
import re


class DataNode:

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.sock = socket.socket()
        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print('Bind failed.' + str(sys.exc_info()))
            exit(1)

    def listen(self):
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            conn.settimeout(300)
            try:
                Thread(target=self.master_thread, args=(conn,)).start()
            except:
                print("Multiprocessing Error! ")
                traceback.print_exc()

    def master_thread(self, conn):
        master_active = True
        database_conn = None

        while master_active:
            orders = self.recieve_input(conn)

            if "_quit" in orders:
                conn.close()
                master_active = False

            elif "_use/" in orders:
                if database_conn is not None:
                    database_conn.close()
                db = re.sub("_use/", "", orders)
                database_conn = sqlite3.connect(db)

            elif "_ddl/" in orders:
                with Lock():
                    ddl_statement = re.sub("_ddl/", "", orders)
                    result = self.prep_transaction(database_conn, ddl_statement)
                    conn.send(result.encode())
                    # Wait for masters response
                    action = self.recieve_input(conn)
                    if "_commit" in action:
                        database_conn.commit()
                    elif "_abort" in action:
                        database_conn.rollback()

    def recieve_input(self, conn, BUFFER_SIZE = 1024):
        client_input = conn.recv(BUFFER_SIZE)
        input_size = sys.getsizeof(client_input)

        if input_size > BUFFER_SIZE:
            print("Input exceeds buffer size")

        result = client_input.decode().rstrip()
        return result

    def prep_transaction(self, database_conn, ddl):
        curs = database_conn.cursor()
        try:
            curs.execute(ddl)
            return "_success"
        except sqlite3.Error:
            return "_fail"


if __name__ == '__main__':
    usage = "python3 datanode.py [host] [port]"
    if len(sys.argv) != 3:
        print(usage)
        exit(1)
    node = DataNode(sys.argv[1], sys.argv[2])
    print("Datanode up!")
    node.listen()
