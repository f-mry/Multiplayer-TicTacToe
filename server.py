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

    def resetGame(self):
        self.board = ["-", "-", "-",
                      "-", "-", "-",
                      "-", "-", "-"]
        self.gameStatus = True
        self.winner = None
        self.currentPlayer = "X"

#-------------------------------------------
# class gameRoomServer:
#     def __init__(self, ):
#         self.game = gameBoard()
#         self.playerList = []
#         self.playerConn = []
#         self.gameRun = True
#         self.barrier = threading.Barrier(2)

    # def returnGameBoard(self):
    #     return self.game

    
# ------------------------------------------

#Game server function
def sendResponse(conn,data):
    try:
        send = pickle.dumps(data)
        conn.send(send)
    except socket.error as e:
        print(str(e))
    print("Data dikirim: ",data)

# def sendPlayerInfo(conn,opp):
    


def bcGameInfo(data):
    for pl in playerList:
        sendResponse(pl[0],data)

# def getPlayerName(conn):
#     playerName = pickle.loads(conn.recv(BUFFER_SIZE))

def restartGame(conn,b):
    print("restart game func")

    global restartRequest
    clientCommand = pickle.loads(conn.recv(BUFFER_SIZE))
    locker.acquire()
    print("lock acquire")
    print(clientCommand)
    try:
        if clientCommand == "restart":
            restartRequest.append(True)
            print(restartRequest)
        elif clientCommand == "stop":
            restartRequest.append(False)
            print(restartRequest)
        else:
            print("error command")
    except:
        print("ada error")

    if len(restartRequest) == 2:
        if restartRequest[0] and restartRequest[1]:
            bcGameInfo("restart")
            game.resetGame()
            bcGameInfo(game.makeGameInfo())
        else:
            bcGameInfo("stop")
    else:
        print("belum 2 request")
    locker.release()
    print("lock dilepas")
    b.wait()
    restart = restartRequest[0] and restartRequest[1]
    restartRequest = []
    print("Restart Game Func Finished")
    return restart


def clientPlayThread(conn,sym,b):
    global vs
    playerSym = sym
    print("clientPlayThread run: ",playerSym)
    sendResponse(conn,"ready")
    #-----------------
    # getPlayerName(conn)
    playerName = pickle.loads(conn.recv(BUFFER_SIZE))
    vs.append(playerName)
    print(vs)
    b.wait()
    sendResponse(conn,vs)
    #-----------------
    time.sleep(0.2)
    sendResponse(conn,game.makeGameInfo())
    while True:
        try:
            # data = conn.recv(BUFFER_SIZE)
            # data = pickle.loads(data)
            data = pickle.loads(conn.recv(BUFFER_SIZE))
            print(data)
            if data[0] == "gameInfo":
                print("gameinfo: ")
                data = data[1]
                print(data)
                game.parseGameInfo(data)
                print(game.makeGameInfo())
                bcGameInfo(data)
            elif data == "endgame":
                restart = restartGame(conn,b)
                if not restart:
                    break
                    
            else:
                print("Error: ",data)
        except: 
            continue
    print("Game selesai")


def playGame():
    b = threading.Barrier(2)
    for pl in playerList:
        start_new_thread(clientPlayThread, (pl[0],pl[1],b))
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
vs = []
restartRequest = []
locker = threading.Lock()
print(locker)
game = gameBoard()
# gameRoom = gameRoomServer()
# print(game.makeGameInfo()[0])

playerList = []
acceptClient()
    
    # start_new_thread(clientThread, (conn,addr,))
    
