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
class gameRoomServer:
    def __init__(self,roomName ):
        self.roomName = roomName
        self.game = gameBoard()
        self.playerList = []
        self.playerConn = []
        self.gameRunning = True
        self.barrier = threading.Barrier(2)
        self.locker = threading.Lock()
        self.playerInRoom = 0

    def playerJoinRoom(self,playerConn,playerName):
        if self.playerInRoom < 2:
            self.playerList.append(playerName)
            self.playerConn.append(playerConn)
            self.playerInRoom += 1
            return True
        else:
            print("Room Full")
            return False

    def checkPlayerReady(self):
        if self.playerInRoom == 2:
            return True
        else:
            return False

#------------------------------------------

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

def playNew(conn,gameRoom):
    print("WIP")



def waitOpp(conn,gameroom):
    print("WIP waitopp")
    print(gameroom.playerList," ",gameroom.roomName)
    b = gameroom.barrier
    b.wait()
    if gameroom.checkPlayerReady():
        sendResponse(conn,"ready")
    print("WaitOpp success")


def createRoom(conn):
    print("CreateRoom")
    try:
        playerName = pickle.loads(conn.recv(BUFFER_SIZE))
        print(playerName)
        roomName = pickle.loads(conn.recv(BUFFER_SIZE))
        gameRoom = gameRoomServer(roomName)
        gameRoom.playerJoinRoom(conn,playerName)
        roomServer.append(gameRoom)
        # print(roomServer[roomServer.index(gameRoom)].roomName)
        sendResponse(conn, True)
        if waitOpp(conn,gameRoom):
            playNew(conn)
    except Exception as e:
        print("Error : ",e)
        sendResponse(conn, False)

def findRoom(conn):
    try:
        playerName = pickle.loads(conn.recv(BUFFER_SIZE))
        print(playerName)
        roomNameList = []
        for room in roomServer:
            roomName = room.roomName
            roomPlayer = room.playerInRoom
            if roomPlayer < 2:
                roomNameList.append(roomName)
        sendResponse(conn,roomNameList)
        roomChoice = pickle.loads(conn.recv(BUFFER_SIZE))
        print("room: ",roomChoice)
        for room in roomServer:
            if room.playerInRoom <2:
                if room.roomName == roomChoice:
                    if room.playerJoinRoom(conn,playerName):
                        print("room name = ",room.roomName)
                        roomChoice = room
                        sendResponse(conn,True)
                        break
        roomChoice.barrier.wait()
    except Exception as e:
        print("Error : ",e)


def initClient(conn):
    print("Client Thread Init Connect")
    sendResponse(conn,"Connected to server")
    try:
        clientCommand = pickle.loads(conn.recv(BUFFER_SIZE))
        if clientCommand == "mode":
            mode = pickle.loads(conn.recv(BUFFER_SIZE))
            if mode == "crtRoom":
                createRoom(conn)
            elif mode == "fndRoom":
                findRoom(conn)
    except socket.error as e:
        print(str(e))
    except Exception as e:
        print(str(e))
    print("Conn Closed")
    conn.close()


def acceptClient():
   while True:
        try:
            conn,addr = sock.accept()
            print(addr, " connected")
            start_new_thread(initClient , (conn,))
        except KeyboardInterrupt:
            sock.close()
            break

#------------------------------------
#Main
roomServer = []
acceptClient()
    
    # start_new_thread(clientThread, (conn,addr,))
    
