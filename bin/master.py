# Kyle Hart
# 3 February 2018
#
# Project: sqlfat
# File: master.py
# Description: a masternode for the sqlfat parallel database.

from .utility import DbUtils
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
import socket
import re
import sys
import traceback
import pickle
import sqlite3


class Master:
    '''
    The master node does not hold any data, rather it takes a client connection and listens performs operations ordered
    by client.The master node parses sql statements received from the client, finds a query execution plan and relays
    operations to datanodes. Specifically with transaction statements the master is responsible for maintaining ACID
    properties throughout the database via a two-phase commit protocol. The master also maintains a catalog table holding
    metadata on all the tables in the parallel database, which allows for more efficient partitioning and replication
    across the datanodes.
    '''

    def __init__(self, host, config):
        '''
        Initialize master node with a socket to listen for client connections.
        Read config file to find addresses of datanodes and establish connection.
        :param host: ip address or hostname of master node (should be local)
        :param config: configuration file
        '''

        # Parsing the config file for nodes' addresses and port numbers
        with open(config) as file:
            read_data = file.read()
        lines = re.split('\n', read_data)

        # REGEX
        port_pattern = re.compile('\d{1,5}')

        # Get host names and ports
        self.host = host
        self.client_port = int(re.search(port_pattern, lines[0])[0])
        self.master_port = int(re.search(port_pattern, lines[1])[0])
        self.data_port = int(re.search(port_pattern, lines[2])[0])

        # Create socket for client connections
        self.client_sock = socket.socket()
        self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.client_sock.bind((self.host, self.client_port))
        except socket.error:
            print('Bind failed.' + str(sys.exc_info()))
            exit(1)

        # Create socket for master connections
        self.master_sock = socket.socket()
        self.master_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.master_sock.bind((self.host, self.master_port))
        except socket.error:
            print('Bind failed.' + str(sys.exc_info()))
            exit(1)

        # Get a list containing socket connections to all datanodes
        self.datanodes = []
        self.masters_addrs = []
        self.masters = []
        for hosts in lines[5:]:
            sock = socket.socket()
            sock.connect((hosts, self.data_port))
            print("Connected to Datanode: " + hosts + ":" + str(self.data_port))
            self.datanodes.append(sock)
            if hosts != self.host:
                self.masters_addrs.append(hosts)

        # Get a utility tool for parsing sql and managing catalog
        self.utility = DbUtils(self.datanodes)

    def client_listen(self):
        '''
        Listen for client connections on the client socket.
        With each new connection create a new thread to handle exchange, and allow for more connections
        :return:
        '''
        self.client_sock.listen(5)
        while True:
            conn, addr = self.client_sock.accept()
            print("Server: Connection from clinet: " + str(addr))
            conn.settimeout(300)
            # Give each connected client a new thread
            try:
                Thread(target=self.client_thread, args=(conn,)).start()
            except:
                print("Multiprocessing Error! ")
                traceback.print_exc()

    def master_listen(self):

        self.master_sock.listen(5)
        while True:
            conn, addr = self.master_sock.accept()
            print("Connection from " + str(addr))
            conn.settimeout(300)
            # Give each connected client a new thread
            try:
                Thread(target=self.master_thread, args=(conn,)).start()
            except:
                print("Multiprocessing Error! ")
                traceback.print_exc()

    def client_thread(self, conn):
        '''
        Thread to handling individual client connections.
        Waits for message from client to either use a new database, execute a ddl statement, or close connection.
        Sends back status messages to client for each operation
        :param conn: socket connection to client
        :return:
        '''
        # Connect to other masters
        for hosts in self.masters_addrs:
            sock = socket.socket()
            sock.connect((hosts, self.master_port))
            print("Connected to Master: " + hosts + ":" + str(self.master_port))
            self.masters.append(sock)

        client_active = True
        response = ""
        # Loop waiting for client's message (i.e., orders) then act accordingly
        while client_active:
            orders = self.recieve_input(conn)
            try:
                self.utility.parse(orders)
            except SyntaxError:
                response = "SYNTAX ERROR IN STATEMENT: " + orders

            if self.utility.statement_type() == "SELECT":
                statements = self.utility.get_node_strings()
                response = self.select(statements)

            elif self.utility.statement_type() == "INSERT":
                statements = self.utility.get_node_strings()
                response = self.ddl(statements)

            elif self.utility.statement_type() == "CREATE TABLE":
                statements = self.utility.get_node_strings()
                response = self.ddl(statements)
                if "Committed" in response:
                    meta = self.utility.enter_table_data()
                    for nodes in self.masters:
                        message = '_enter ' + meta
                        nodes.send(message.encode())

            elif self.utility.statement_type() == "USE":
                self.utility.set_db()
                db = self.utility.get_db()
                response = self.use(db)

            elif self.utility.statement_type() == "LOAD":
                pass

            elif self.utility.statement_type() == "QUIT":
                response = "Quitting Database"
                client_active = False

            # Upon _ddl we execute a 2-phase commit and send results back to client
            elif "_ddl/" in orders:
                transaction = re.sub("_ddl/", "", orders)
                response = self.ddl(transaction)
                if response == "Committed":
                    self.utility.enter_table_data()
            conn.send(response.encode())

    def master_thread(self, conn):
        master_active = True
        response = ""
        while master_active:
            orders = self.recieve_input(conn)

    def use(self, database):
        '''
        Tell datanodes to open connections to the given DB
        :param database: sqlite db file
        :return: status string which can be sent back to client
        '''
        message = "_use/" + database
        for nodes in self.datanodes:
            nodes.send(message.encode())
        return "Using database: " + database

    def select(self, statements):
        data = []
        # Create a thread pool to handle each of the datanode's queries concurrently
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            # Tell nodes to prep transaction
            for idx, nodes in enumerate(self.datanodes):
                message = "_query/" + statements[idx]
                nodes.send(message.encode())
            # Get responses
            futures = [executor.submit(self.recieve_input, nodes) for nodes in self.datanodes]
            # Check commit status for each node, log into status string
            for future in as_completed(futures):
                for rows in future.result():
                    data.append(rows)
        return "Query Returned {} rows".format(len(data))

    def quit(self):
        '''
        UNUSED; Close the sockets to our datanodes
        :return: status string which can be sent back to client
        '''
        message = "_quit"
        for nodes in self.datanodes:
            nodes.send(message.encode())
            nodes.close()
        return "Closing connection"

    def ddl(self, statement, catalog):
        '''
        Multithreaded 2-phase commit for parallel datanodes.
        Sends ddl statement to each node for execution, nodes report back success or failure.
        If all initial execution is successful, we order a commit on all nodes, otherwise order an abort
        :param statement: ddl statement
        :param catalog: sqlite3 db connection to catalog, holds meta data on nodes and tables
        :return: status string which can be sent back to client
        '''
        message = "_ddl/" + statement
        commit = True
        response = ""
        # Create a thread pool to handle each of the datanode's transactions concurrently
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            # Tell nodes to prep transaction
            for nodes in self.datanodes:
                nodes.send(message.encode())
            # Get responses
            futures = [executor.submit(self.recieve_input, nodes) for nodes in self.datanodes]
            # Check commit status for each node, log into status string
            for future in as_completed(futures):
                result = future.result()
                host = re.split("/", result)[1]
                if "_fail" in future.result():
                    response += "Transaction failure at host: " + host + "\n"
                    commit = False
                elif "_success" in future.result():
                    response += "Transaction success at host: " + host + "\n"
        # If all nodes succeeded in prep send phase 2 commit message, otherwise order all to abort
        for nodes in self.datanodes:
            if commit == True:
                self.transact("_commit")
                # Successful table writes are written to catalog
                if "CREATE TABLE" in statement:
                    table = re.split(" ", statement)[2]
                    (host, port) = nodes.getpeername()
                    id = int(re.sub("200.0.0.1", "", str(host)))
                    catalog.execute("INSERT INTO dtables (tname, nodeurl, nodeid) "
                                    "VALUES (\"{}\", \"{}\", {})".format(table, host, id))
                    catalog.commit()
            else:
                self.transact("_abort")
        # Update status string
        if commit == True:
            response += "Committed"
        else:
            response += "Aborted"
        return response

    def transact(self, status):
        '''
        Order nodes to commit or abort a transaction
        :param status: commit or abort
        :return: None
        '''
        message = status
        for nodes in self.datanodes:
            nodes.send(message.encode())

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
        return result


if __name__ == '__main__':
    usage = "python3 master.bin [host] [port] [config file]"
    if len(sys.argv) != 4:
        print(usage)
        exit(1)
    master = Master(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Master Up!")
    master.listen()
