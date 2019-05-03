import socket
from _thread import *
import pickle
from game import TicTacToe

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serverIP = socket.gethostbyname("NKOTH")
serverPort = 5555
BUFFER_SIZE = 2048

try:
    sock.bind((serverIP,serverPort))
except socket.error as e:
    print(str(e))

sock.listen()
print("Server Listening")

def sendResponse(conn,data):
    print("send respon")
    try:
        data = pickle.dumps(data)
        conn.send(data)
    except socket.error as e:
        print(str(e))
    return True


def clientThread(conn,addr):
    print("Client Thread created")
    while True:
        try:
            # print("Menunggu data")
            data = conn.recv(BUFFER_SIZE)
            data = pickle.loads(data)
            print("Data received from: ",addr ," ",data)
            # if data == "stop":
                # break
            # if data == "reply":
                # sendResponse(conn,"Data diterima")
        except :
            continue
    conn.close()
    print("Connection closed") 

while True:
    conn,addr = sock.accept()
    print(addr, " connected")

    start_new_thread(clientThread, (conn,addr,))
