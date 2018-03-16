# Kyle Hart
# 3 February 2018
#
# Project: sqlfat
# File: client.py
# Description: client for sqlfat parallel database system

import socket
import pickle
import struct

class Client:
    '''
    Client is responsible for connecting to the masternode and sending commands as well as sql statements
    '''

    def __init__(self, host, port=50000):
        '''
        Initialize client to connect to the masternode
        :param host: hostname/ip of the masternode
        :param port: port number of the masternode
        '''
        self.host = host
        self.port = int(port)
        self.sock = socket.socket()
        self.sock.connect((host, port))

        self.response = None
        self.cache = None

    def receive_data(self, conn):
        # Read message length and unpack it into an integer
        raw_msglen = conn.recv(4)
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

    def _recv_response_and_data(self):
        result = self.receive_data(self.sock)
        self.response, self.data = pickle.loads(result)

    def use(self, db):
        '''
        Tell sqlfat to use the given database. If the given database does not exist then one will be automatically created
        :param db: string, database file name
        :return: status message from master node
        '''
        message = "USE " + db
        self.sock.send(pickle.dumps(message))
        self._recv_response_and_data()

    def quit(self):
        '''
        Quit connection with master node sqlfat database
        :return: status message from master node
        '''
        message = "_quit"
        self.sock.send(pickle.dumps(message))
        self._recv_response_and_data()

    def execute(self, statement):
        '''
        Send SQL statement to sqlfat master node for execution
        :param statement: sql statement
        :return: status message from master node
        '''
        self.sock.send(pickle.dumps(statement))
        self._recv_response_and_data()



    '''    
    def transaction(self, statement):

        Send ddl statement to sqlfat master node for execution
        :param statement: ddl statement
        :return: status message from master node

        message = "_ddl/" + statement
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode()
    '''


