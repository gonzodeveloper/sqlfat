# Kyle Hart
# 3 February 2018
#
# Project: sqlfat
# File: master.py
# Description: a masternode for the sqlfat parallel database.

from .utility import DbUtils
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from threading import Thread
import socket
import re
import sys
import traceback
import pickle
import os
import csv
import struct


class Master:
    '''
    The master node does not hold any data, rather it takes a client connection and listens performs operations ordered
    by client.The master node parses sql statements received from the client, finds a query execution plan and relays
    operations to datanodes. Specifically with transaction statements the master is responsible for maintaining ACID
    properties throughout the database via a two-phase commit protocol. The master also maintains a catalog table holding
    metadata on all the tables in the parallel database, which allows for more efficient partitioning and replication
    across the datanodes.
    '''

    def __init__(self):
        '''
        Initialize master node with a socket to listen for client connections.
        Read config file to find addresses of datanodes and establish connection.
        '''
        # Get the location of our sqlfat directory
        self.sqlfat_home = os.environ['SQLFAT_HOME']
        # We find our config file here
        config = self.sqlfat_home + "etc/config"

        # Parsing the config file for nodes' addresses and port numbers
        with open(config) as file:
            read_data = file.read()
        lines = re.split('\n', read_data)

        # REGEX
        port_pattern = re.compile('\d{1,5}')

        # Get host names and ports
        self.host = socket.gethostbyname(socket.gethostname())
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

        # Get a list containing socket connections to all datanodes, and list or addresses to all masters
        self.datanodes = []
        self.masters_addrs = []
        for hosts in lines[5:-1]:
            sock = socket.socket()
            sock.connect((hosts, self.data_port))
            print("Connected to Datanode: " + hosts + ":" + str(self.data_port))
            self.datanodes.append(sock)
            if hosts != self.host:
                self.masters_addrs.append(hosts)
        # List of connection to other masters
        self.masters = []

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

        # Get a utility for parsing and config table maintenence
        utility = DbUtils(self.datanodes)
        client_active = True
        # Loop waiting for client's message (i.e., orders) then act accordingly
        while client_active:
            orders = self.receive_input(conn)
            try:
                utility.parse(orders)
            except SyntaxError:
                response = "SYNTAX ERROR IN STATEMENT: " + orders
                data = None
                conn.send(pickle.dumps((response, data)))
                print("SENT: {}".format(response))
                continue

            if utility.statement_type() == "SELECT":
                statements = utility.get_node_strings()
                response, data = self.select(statements)

            elif utility.statement_type() == "INSERT":
                statements = utility.get_node_strings()
                commit, response, trans_nodes = self.ddl(statements)
                if commit:
                    self.transact("_commit", trans_nodes)
                    response += "Transaction committed"
                    print(response)
                else:
                    self.transact("_abort", trans_nodes)
                    response += "Transaction aborted"
                data = None

            elif utility.statement_type() == "CREATE TABLE":
                statements = utility.get_node_strings()
                commit, response, trans_nodes = self.ddl(statements)
                if commit:
                    self.transact("_commit", trans_nodes)
                    response += "Transaction committed"
                    meta = utility.enter_table_data()
                    for nodes in self.masters:
                        order = '_enter'
                        nodes.send(pickle.dumps((order, meta)))
                else:
                    self.transact("_abort", trans_nodes)
                    response += "Transaction aborted"
                data = None

            elif utility.statement_type() == "USE":
                utility.set_db()
                db = utility.get_db()
                response = self.use(db)
                data = None

            elif utility.statement_type() == "LOAD":
                file = utility.statement['file']
                table = utility.statement['table']
                delimiter = utility.statement['delimiter']
                quotechar = utility.statement['quotechar']

                response = self.load(file, table, delimiter, quotechar)
                data = None

            elif utility.statement_type() == "QUIT":
                response = "Quitting Database"
                client_active = False
                data = None
            else:
                response = None
                data = None

            conn.send(pickle.dumps((response, data)))
            print("RESPONSE: {} \nDATA: {}\nTO: {}".format(response, data, conn.getpeername()))

    def master_thread(self, conn):
        master_active = True
        utility = DbUtils(self.datanodes)
        while master_active:
            orders, meta = self.receive_input(conn)
            if orders == '_enter':
                utility.enter_table_meta_str(meta)
            elif orders == "_quit":
                conn.close()
                master_active = False

    def use(self, database):
        '''
        Tell datanodes to open connections to the given DB
        :param database: sqlite db file
        :return: status string which can be sent back to client
        '''
        order = "_use"
        for nodes in self.datanodes:
            nodes.send(pickle.dumps((order, database)))
        return "Using database: " + database

    def select(self, statements):
        data = []
        select_nodes = []
        # Create a thread pool to handle each of the datanode's queries concurrently
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            # Tell nodes to prep transaction
            for idx, node in enumerate(self.datanodes):
                if statements[idx] is not None:
                    order = "_query"
                    print(order)
                    print(statements[idx])
                    node.send(pickle.dumps((order, statements[idx])))
                    select_nodes.append(node)
            # Get responses
            futures = [executor.submit(self.receive_input, nodes) for nodes in select_nodes]
            # Check commit status for each node, log into status string
            for future in as_completed(futures):
                for rows in future.result():
                    data.append(rows)
        response = "Query Returned {} rows".format(len(data))
        return response, data

    def quit(self):
        '''
        UNUSED; Close the sockets to our datanodes
        :return: status string which can be sent back to client
        '''
        order = "_quit"
        message = None
        for nodes in self.datanodes:
            nodes.send(pickle.dumps((order, message)))
            nodes.close()
        return "Closing connection"

    def ddl(self, statements):
        '''
        Multithreaded 2-phase commit for parallel datanodes.
        Sends ddl statement to each node for execution, nodes report back success or failure.
        If all initial execution is successful, we order a commit on all nodes, otherwise order an abort
        :param statements: ddl statement
        :return: status string which can be sent back to client
        '''
        commit = True
        response = ""
        trans_nodes = []
        # Create a thread pool to handle each of the datanode's transactions concurrently
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            # Tell nodes to prep transaction
            for idx, node in enumerate(self.datanodes):
                if statements[idx] is not None:
                    order = "_ddl"
                    node.send(pickle.dumps((order, statements[idx])))
                    trans_nodes.append(node)
            # Get responses
            futures = [executor.submit(self.receive_data, nodes) for nodes in trans_nodes]
            # Check commit status for each node, log into status string
            for future in as_completed(futures):
                status, host = future.result()
                if status == "_fail":
                    response += "Transaction failure at host: " + host + "\n"
                    commit = False
                elif status == "_success":
                    response += "Transaction success at host: " + host + "\n"

        return commit, response, trans_nodes

    def transact(self, status, trans_nodes):
        '''
        Order nodes to commit or abort a transaction
        :param status: commit or abort
        :return: None
        '''
        message = status
        for nodes in trans_nodes:
            nodes.send(pickle.dumps(message))

    def load(self, filename, table, separated_by, enclosed_by):
        utility = DbUtils(self.datanodes)
        file = self.sqlfat_home + "load/" + filename
        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            futures = []
            successes = 0
            failures = 0
            with open(file, newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=separated_by, quotechar=enclosed_by)
                headers = next(csv_reader)
                meta = utility.get_table_meta(table)
                part_col = utility.partition_col(headers, meta)
                for row in csv_reader:
                    utility.target_node(row, meta, part_col)
                    futures.append(executor.submit(self.load_insert, headers, row, meta))
                for future in as_completed(futures):
                    status, host = future.result()
                    if status == "_success":
                        successes += 1
                    else:
                        failures += 1
        return "Successfully inserted {} rows, failed to insert {}".format(successes, failures)

    def load_insert(self, headers, row, meta, node_idx):
        table = meta['tname']
        col_str = ", ".join(headers)
        val_str = ", ".join(row)
        order = "_single"
        target_node = self.datanodes[node_idx]
        message = "INSERT INTO {} ({}) VALUES ({})".format(table, col_str, val_str)
        target_node.send(pickle.dumps((order, message)))
        return self.receive_input(target_node)

    def receive_data(self, conn):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(conn, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(conn, msglen)

    def recvall(self, conn, size):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < size:
            packet = conn.recv(size - len(data))
            if not packet:
                return None
            data += packet
        return pickle.loads(data)

    def receive_input(self, conn, BUFFER_SIZE = 1024):
        '''
        Wrapper function for receiving input. Ensures we do not exceed given buffer size.
        :param conn: socket connection
        :param BUFFER_SIZE: byte limit for message
        :return: message received
        '''
        client_input = conn.recv(5)
        input_size = sys.getsizeof(client_input)

        if input_size > BUFFER_SIZE:
            print("Input exceeds buffer size")

        result = pickle.loads(client_input)
        print("Message: {}\n From: {}".format(result, conn.getpeername()))
        return result


if __name__ == '__main__':
    master = Master()
    print("Master Up!")
    try:
        Thread(target=master.master_listen, args=()).start()
    except:
        print("Multiprocessing Error! ")
        traceback.print_exc()
    try:
        Thread(target=master.client_listen, args=()).start()
    except:
        print("Multiprocessing Error! ")
        traceback.print_exc()
