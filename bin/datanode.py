# Kyle Hart
# 3 February 2018
#
# Project: sqlfat
# File: datanode.py
# Description: datanode for the sqlfat parallel database

import socket
from threading import Thread, Lock
import sqlite3
import sys
import traceback
import re
import pickle
import os


class DataNode:
    '''
    The datanodes are stood up to get a connection from the master node and execute queries and transactions in accordance
    with orders from the master. The datanodes maintain the parallel database in sqlite db files, and through an active
    socket connection with the master they essentially daemonize the normally static sqlite. Because the sql parsing and
    query execution plan are controlled by the master, the datanodes are essentially dumb--they execute sql and return
    the results. However, with transactional statements, the nodes only must report the status of their initial execution
    back to the master and wait for his final orders for commit. Each datanode is multithreaded such that they can
    concurrently handle multiple connections, this allows for a multi-master architecture.
    '''

    def __init__(self):
        '''
        Stand up a datanode with a tcp socket listening for connection from the master node
        '''
        # Get the location of our sqlfat directory
        sqlfat_home = os.environ['SQLFAT_HOME']
        # We find our config file here
        config = "{}/etc/config".format(sqlfat_home)

        # Parsing the config file for nodes' addresses and port numbers
        with open(config) as file:
            read_data = file.read()
        lines = re.split('\n', read_data)

        # REGEX
        port_pattern = re.compile('\d{1,5}')

        # Get host names and ports
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = int(re.search(port_pattern, lines[2])[0])

        # Create socket to listen for master node's connection
        self.sock = socket.socket()
        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print('Bind failed.' + str(sys.exc_info()))
            exit(1)

    def listen(self):
        '''
        Wait to establish connection with the master node, upon connection create a new thread to handle that master.
        :return:
        '''
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            print("Server: Connection from " + str(addr))
            # Times out after an hour
            #conn.settimeout(6000)
            # Once connected, open new thread
            try:
                Thread(target=self.master_thread, args=(conn,)).start()
            except:
                print("Multiprocessing Error! ")
                traceback.print_exc()

    def master_thread(self, conn):
        '''
        Wait for orders from master: _quit, _use, or _ddl. Respectively these will prompt the datanode to either quit
        the connection, use a new database, or execute a transactional statement. With the transaction the datanode will
        try an initial execution and report failure or success back to the master, once the master gets status from all
        datanodes it will send back a message to either commit or abort that transaction.
        :param conn: socket connection to the master.
        :return:
        '''
        master_active = True
        database_conn = None
        # Wait for orders from the master
        while master_active:
            orders = self.recieve_input(conn)
            if "_quit" in orders:
                conn.close()
                master_active = False
            # Get a sqlite connection to the new database, close any other connection that might be open
            elif "_use/" in orders:
                if database_conn is not None:
                    database_conn.close()
                db = re.sub("_use/", "", orders)
                db = "/sqlfat/data/" + db
                print(db)
                database_conn = sqlite3.connect(db)
                print("Using database: " + db)
            # Execute ddl statement
            elif "_ddl/" in orders:
                # No other transactions during 2 phase commit
                with Lock():
                    ddl_statement = re.sub("_ddl/", "", orders)
                    result = self.prep_transaction(database_conn, ddl_statement)
                    print("Prepping transaction: " + ddl_statement)
                    conn.send(pickle.dumps(result))
                    # Wait for masters response
                    action = self.recieve_input(conn)
                    if "_commit" in action:
                        database_conn.commit()
                        print("Committed Transaction")

                    elif "_abort" in action:
                        database_conn.rollback()
                        print("Aborted Transaction")
            elif "_query/" in orders:
                sql = re.sub("_query/", "", orders)
                curs = database_conn.cursor()
                curs.execute(sql)
                rows = [x for x in curs.fetchall()]
                conn.send(pickle.dumps(rows))

    def recieve_input(self, conn, BUFFER_SIZE = 1024):
        '''
        Wrapper function for recieving input. Ensures we do not exceed given buffer size.
        :param conn: socket connection
        :param BUFFER_SIZE: byte limit for message
        :return: message received
        '''
        client_input = conn.recv(BUFFER_SIZE)
        input_size = sys.getsizeof(client_input)

        if input_size > BUFFER_SIZE:
            print("Input exceeds buffer size")

        result = pickle.loads(client_input)
        print(result)
        return result

    def prep_transaction(self, database_conn, ddl):
        '''
        Initial execution of transaction in 2 phase commit. Report success or failure.
        :param database_conn: connection to sqlite db file
        :param ddl: ddl statement
        :return: success or failure of initial transaction
        '''
        curs = database_conn.cursor()
        try:
            curs.execute(ddl)
            return "_success/" + self.host
        except sqlite3.Error:
            return "_fail/" + self.host


if __name__ == '__main__':
    usage = "python3 datanode.bin [host] [port]"
