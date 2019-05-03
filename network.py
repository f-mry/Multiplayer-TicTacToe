import socket 
import pickle

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = socket.gethostbyname("NKOTH")
        self.port = 5555
        self.addr = (self.host,self.port)
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected to server")
        except socket.error as e:
            print(str(e))

    def send(self,data):
        data = pickle.dumps(data)
        try:
            self.client.send(data)
        except socket.error as e:
            print(str(e))

    def recv(self):
        
        try:
            data = self.client.recv(2048)
            data = pickle.loads(data)
        except socket.error as e:
            print(str(e))
        return data    
        

n = Network()
n.connect()
while True:
    msg = input("Pesan ke server: ")
    n.send(msg)
    if msg == "reply":
        print(n.recv())
    if msg == "stop":
        break




