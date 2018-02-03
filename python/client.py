import socket as socket
from threading import Thread
import re

class Client:

    def __init__(self, config):
        with open(config) as file:
            read_data = file.read()
        read_data = re.split('\n\n', read_data)

        addrPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')
        ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        address = re.findall(addrPattern, read_data[0])[0]

        self.configserver = re.split(':', address)[0]
        port = re.split(':', address)[1]

        self.datanodes = []
        for lines in read_data[2:]:
            ip = re.search(ipPattern, lines)[0]
'''         
    def connect(self):
        for nodes in datanodes:
            Tread
'''
if __name__ == '__main__':
    client = Client("config_test")




