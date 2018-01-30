import socket as socket
from threading import Thread
import sqlite3
import sys
import traceback


class DataNode:

    def __int__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print('Bind failed.' + str(sys.exc_info()))
            sys.exit()

    def listen(self):
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            conn.settimeout(60)
            try:
                Thread(target=self.client_thread, args=(conn, addr)).start()
            except:
                print("Multiprocessing Error! ")
                traceback.print_exc()

    def client_thread(self, conn, addr, BUFFER_SIZE = 1024):
        client_active = True

        while client_active:
            client_input = self.recieve_input(conn)

            if "_quit" in client_input:
                conn.close()
                client_active = False

            elif "_prepare" in client_input:
                ddl_statement = self.recieve_input(conn)
                database_conn = sqlite3.connect('localdb')
                result = self.prep_transaction(database_conn, ddl_statement)
                conn.send(result.encode())

                action = self.recieve_input(conn)
                if "_commit" in action:
                    database_conn.commit()
                elif "_abort":
                    database_conn.rollback()
                database_conn.close()
        conn.close()
        client_active = False

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
    print()