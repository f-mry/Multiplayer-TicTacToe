import socket 
import pickle

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = socket.gethostbyname("NKOTH")
        self.port = 5555
        self.addr = (self.host,self.port)
        self.BUFFER_SIZE = 2048
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            print(self.recv())
            return True
        except socket.error as e:
            print(str(e))
            return False

    def send(self,data):
        data = pickle.dumps(data)
        try:
            self.client.send(data)
        except socket.error as e:
            print(str(e))

    def recv(self):
        try:
            data = self.client.recv(self.BUFFER_SIZE)
            data = pickle.loads(data)
        except Exception as e:
            print(str(e))
        return data    

    def waitRecv(self,keyword):
        bool = False
        data = ""
        while True:
            try:
                data = pickle.loads(self.client.recv(self.BUFFER_SIZE))
                if data == keyword:
                    bool = True
                    break
            except KeyboardInterrupt:
                break
            except:
                continue
        return bool

if __name__ == "__main__":
    n = Network()
    n.connect()
    while True:
        msg = input("Pesan ke server: ")
        n.send(msg)
        if msg == "reply":
            print(n.recv())
        if msg == "stop":
            n.client.close()
            break
