import socket

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def use(self, db):
        message = "_use/" + db
        self.sock.send(message.encode())

    def quit(self):
        self.sock.send("_quit".encode())

    def transaction(self, statement):
        message = "_ddl/" + statement
        self.sock.send(message.encode())
        self.sock.close()

    def execute(self, query):
        self.sock.send(query.encode())




