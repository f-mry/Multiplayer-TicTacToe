import socket
from _thread import *
import threading
import pickle
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serverIP = socket.gethostbyname("NKOTH")
serverPort = 5555
BUFFER_SIZE = 2048
#-----------VAR---------
# gameList = []
connList = []

try:
    sock.bind((serverIP,serverPort))
except socket.error as e:
    print(str(e))

sock.listen(2)
print("Server Listening")

# ------------------------------------------
# Class Game Board
class gameBoard:
    def __init__(self,):
        
        self.board = ["-", "-", "-",
                      "-", "-", "-",
                      "-", "-", "-"]
        self.gameStatus = True
        self.winner = None
        # self.Player = {}
        self.currentPlayer = "X"

    def parseGameInfo(self, gameInfo):
        #gameInfo = [board,gameStatus,winner,currentPlayer]
        #gamePlayer = {'X': 'player1', 'O': 'player2'}

        self.board = gameInfo[0]
        self.gameStatus = gameInfo[1]
        self.winner = gameInfo[2]
        self.currentPlayer = gameInfo[3]

    def makeGameInfo(self):
        gameInfo = [self.board, self.gameStatus, self.winner, self.currentPlayer]
        return gameInfo
    
# ------------------------------------------

def sendResponse(conn,data):
    try:
        send = pickle.dumps(data)
        conn.send(send)
    except socket.error as e:
        print(str(e))
    print("Data dikirim: ",data)

def bcGameInfo(data):
    for pl in playerList:
        sendResponse(pl[0],data)

def clientPlayThread(conn,sym):
    playerSym = sym
    print("clientPlayThread run: ",playerSym)
    sendResponse(conn,"ready")
    time.sleep(0.2)
    sendResponse(conn,game.makeGameInfo())
    while True:
        try:
            # data = conn.recv(BUFFER_SIZE)
            # data = pickle.loads(data)
            data = pickle.loads(conn.recv(BUFFER_SIZE))
            print(data)
            if len(data) == 4:
                game.parseGameInfo(data)
                bcGameInfo(data)
            print(data)
        except: 
            # print(str(e))
            continue


def playGame():
    for pl in playerList:
        start_new_thread(clientPlayThread, (pl[0],pl[1]))
        time.sleep(1)
    # playerList = [playerList[0][0], playerList[1][0]]


def clientThread(conn):
    print("Client Thread created")
    sendResponse(conn,"Connected to server")
    ex = False
    # while True:
    try:
        data = pickle.loads(conn.recv(BUFFER_SIZE))
        # print("Data received from: ",addr ," ",data)
        if data == "play":
            if len(playerList) == 0:
                sendResponse(conn,"X")
                sendResponse(conn,"wait")
                playerList.append([conn,"X"])
            elif len(playerList) == 1:
                sendResponse(conn,"O")
                playerList.append([conn,"O"])
                ex = True
            else:
                sendResponse(conn,"full")
        # elif data == "stop":
        #     break
        else:
            print(data)
            sendResponse(conn,"data diterima")
        print("Close clientThread")
        print(ex)
        if ex:
            playGame()
    except :
        print("stop")



def acceptClient():
   while True:
        try:
            conn,addr = sock.accept()
            print(addr, " connected")
            connList.append(conn)
            start_new_thread(clientThread,(conn,))
        except KeyboardInterrupt:
            for cn in connList:
                cn.close()
            sock.close()
            break

#------------------------------------
#Main
game = gameBoard()
print(game.makeGameInfo()[0])

playerList = []
acceptClient()
    
    # start_new_thread(clientThread, (conn,addr,))
    
