# Kyle Hart
# 3 February 2018
#
# Project: sqlfat
# File: client.py
# Description: client for sqlfat parallel database system

import socket

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

    def use(self, db):
        '''
        Tell sqlfat to use the given database. If the given database does not exist then one will be automatically created
        :param db: string, database file name
        :return: status message from master node
        '''
        message = "_use/" + db
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode()

    def quit(self):
        '''
        Quit connection with master node sqlfat database
        :return: status message from master node
        '''
        self.sock.send("_quit".encode())
        # response =  self.sock.recv(1024).decode()
        return "Quit"

    def transaction(self, statement):
        '''
        Send ddl statement to sqlfat master node for execution
        :param statement: ddl statement
        :return: status message from master node
        '''
        message = "_ddl/" + statement
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode()

    def execute(self, query):
        '''
        Send SQL statement to sqlfat master node for execution
        :param query: sql statement
        :return: status message from master node
        '''
        self.sock.send(query.encode())
        return self.sock.recv(1024).decode()




