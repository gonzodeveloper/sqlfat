# Kyle Hart
# 3 February 2018
#
# Project: sqlfat
# File: master.py
# Description: a masternode for the sqlfat parallel database.

from utility import DbUtils
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
import socket
import re
import sys
import traceback
import pickle


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
            orders = self.recieve_input(conn)
            try:
                utility.parse(orders)
            except SyntaxError:
                response = "SYNTAX ERROR IN STATEMENT: " + orders
                data = None
                conn.send(pickle.dumps(response))
                conn.send(pickle.dumps(data))
                continue

            if utility.statement_type() == "SELECT":
                statements = utility.get_node_strings()
                response, data = self.select(statements)

            elif utility.statement_type() == "INSERT":
                statements = utility.get_node_strings()
                commit, response = self.ddl(statements)
                if commit:
                    self.transact("_commit")
                    response += "Transaction committed"
                else:
                    self.transact("_abort")
                    response += "Transaction aborted"
                data = None

            elif utility.statement_type() == "CREATE TABLE":
                statements = utility.get_node_strings()
                commit, response = self.ddl(statements)
                if commit:
                    self.transact("_commit")
                    meta = utility.enter_table_data()
                    for nodes in self.masters:
                        message = '_enter/' + meta
                        nodes.send(pickle.dumps(message))
                else:
                    self.transact("_abort")
                data = None

            elif utility.statement_type() == "USE":
                utility.set_db()
                db = utility.get_db()
                response = self.use(db)
                data = None

            elif utility.statement_type() == "LOAD":
                response = None
                data = None

            elif utility.statement_type() == "QUIT":
                response = "Quitting Database"
                client_active = False
                data = None
            else:
                response = None
                data = None

            conn.send(pickle.dumps(response))
            conn.send(pickle.dumps(data))

    def master_thread(self, conn):
        master_active = True
        while master_active:
            orders = self.recieve_input(conn)
            if '_meta/' in orders:
                meta = re.sub("_enter/", "", orders)
                self.utility.enter_table_meta_str(meta)
            elif '_quit' in orders:
                conn.close()
                master_active = False

    def use(self, database):
        '''
        Tell datanodes to open connections to the given DB
        :param database: sqlite db file
        :return: status string which can be sent back to client
        '''
        message = "_use/" + database
        for nodes in self.datanodes:
            nodes.send(pickle.dumps(message))
        return "Using database: " + database

    def select(self, statements):
        data = []
        # Create a thread pool to handle each of the datanode's queries concurrently
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            # Tell nodes to prep transaction
            for idx, nodes in enumerate(self.datanodes):
                message = "_query/" + statements[idx]
                nodes.send(pickle.dumps(message))
            # Get responses
            futures = [executor.submit(self.recieve_input, nodes) for nodes in self.datanodes]
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
        message = "_quit"
        for nodes in self.datanodes:
            nodes.send(pickle.dumps(message))
            nodes.close()
        return "Closing connection"

    def ddl(self, statements):
        '''
        Multithreaded 2-phase commit for parallel datanodes.
        Sends ddl statement to each node for execution, nodes report back success or failure.
        If all initial execution is successful, we order a commit on all nodes, otherwise order an abort
        :param statement: ddl statement
        :return: status string which can be sent back to client
        '''
        commit = True
        response = ""
        recv_count = 0
        trans_nodes = []
        # Create a thread pool to handle each of the datanode's transactions concurrently
        with ThreadPoolExecutor(max_workers=len(self.datanodes)) as executor:
            # Tell nodes to prep transaction
            for idx, node in enumerate(self.datanodes):
                if statements[idx] is not None:
                    message = "_ddl/" + statements[idx]
                    node.send(pickle.dumps(message))
                    trans_nodes.append(node)
            # Get responses
            futures = [executor.submit(self.recieve_input, nodes) for nodes in trans_nodes]
            # Check commit status for each node, log into status string
            for future in as_completed(futures):
                result = future.result()
                host = re.split("/", result)[1]
                if "_fail" in future.result():
                    response += "Transaction failure at host: " + host + "\n"
                    commit = False
                elif "_success" in future.result():
                    response += "Transaction success at host: " + host + "\n"

        return commit, response

    def transact(self, status):
        '''
        Order nodes to commit or abort a transaction
        :param status: commit or abort
        :return: None
        '''
        message = status
        for nodes in self.datanodes:
            nodes.send(pickle.dumps(message))

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
    usage = "python3 master.py [host] [config file]"
    if len(sys.argv) != 3:
        print(usage)
        exit(1)
    master = Master(sys.argv[1], sys.argv[2])
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
