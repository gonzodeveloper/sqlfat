import socket

class Client:

    def __init__(self, host, port=50000):
        self.host = host
        self.port = int(port)
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def use(self, db):
        message = "_use/" + db
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode()

    def quit(self):
        self.sock.send("_quit".encode())
        response =  self.sock.recv(1024).decode()
        return response

    def transaction(self, statement):
        message = "_ddl/" + statement
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode()

    def execute(self, query):
        self.sock.send(query.encode())
        return self.sock.recv(1024).decode()




