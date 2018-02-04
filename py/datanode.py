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
            print("Server: Connection from " + str(addr))
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
                db = "/sqlfat/data/" + db
                database_conn = sqlite3.connect(db)
                print("Using database: " + db)

            elif "_ddl/" in orders:
                with Lock():
                    ddl_statement = re.sub("_ddl/", "", orders)
                    result = self.prep_transaction(database_conn, ddl_statement)
                    print("Prepping transaction: " + ddl_statement)
                    conn.send(result.encode())
                    # Wait for masters response
                    action = self.recieve_input(conn)
                    if "_commit" in action:
                        database_conn.commit()
                        print("Committed Transaction")

                    elif "_abort" in action:
                        database_conn.rollback()
                        print("Aborted Transaction")

    def recieve_input(self, conn, BUFFER_SIZE = 1024):
        client_input = conn.recv(BUFFER_SIZE)
        input_size = sys.getsizeof(client_input)

        if input_size > BUFFER_SIZE:
            print("Input exceeds buffer size")

        result = client_input.decode().rstrip()
        print(result)
        return result

    def prep_transaction(self, database_conn, ddl):
        curs = database_conn.cursor()
        try:
            curs.execute(ddl)
            return "_success/" + self.host
        except sqlite3.Error:
            return "_fail/" + self.host


if __name__ == '__main__':
    usage = "python3 datanode.py [host] [port]"
    if len(sys.argv) != 3:
        print(usage)
        exit(1)
    node = DataNode(sys.argv[1], sys.argv[2])
    print("Datanode up!")
    node.listen()