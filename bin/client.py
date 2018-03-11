# Kyle Hart
# 3 February 2018
#
# Project: sqlfat
# File: client.py
# Description: client for sqlfat parallel database system

import socket
import pickle

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

    def _recv_response_and_data(self):
        result = self.sock.recv(1024)
        self.response, self.data = pickle.loads(result)
        print("Client: {}".format(self.response))
        print("Client: {}".format(self.data))


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


