from network import Network
from game import TicTacToe
import os
import time

net = Network()
game = TicTacToe()
playerSym = ''
banner = """
 _____  _  ____    _____  ____  ____    _____  ____  _____
/__ __\/ \/   _\  /__ __\/  _ \/   _\  /__ __\/  _ \/  __/
  / \  | ||  /      / \  | / \||  /      / \  | / \||  \  
  | |  | ||  \_     | |  | |-|||  \_     | |  | \_/||  /_ 
  \_/  \_/\____/    \_/  \_/ \|\____/    \_/  \____/\____\
"""


def play():
    global game
    print("WIP play")
    print(playerSym)
    send = playerSym
    net.send(send)
    while game.gameStatus:
        gameinfo = net.recv()
        game.parseGameInfo(gameinfo)
        game.gameCond()
        if game.gameStatus:
            if game.currentPlayer == playerSym:
                game.showBoard()
                game.handleTurn()
                game.flipPlayer()
                net.send(game.makeGameInfo())
            else:
                print("Tunggu Giliran")
        else:
            break
    print("Game selesai")


def menu():
    # os.system('cls' if os.name == 'nt' else 'clear')
    global playerSym
    print(banner)
    if net.connect():
        net.send("play")
        playerSym = net.recv()
        respond = net.recv()
        if respond == "wait":
            print("Menunggu pemain lain")
            if net.waitRecv("ready"):
                play()
        elif respond == "ready":
            play()
        elif respond == "full":
            print("Room full")
            net.client.close()


def chooseMode():
    inp = '0'
    while int(inp) not in range(1,4):
        print("1.\tBuat Room\n2.\tCari Room\n3\tExit")
        inp = input("Pilih Mode: ")

    if inp == '1':
        net.send("crtRoom")
        return 1
    elif inp == '2':
        net.send("fndRoom")
        return 2
    else:
        net.send("stop")
        print("See you")
        return 0



def newRoom():
    print("WIP newGame")
    playerName = input("Masukkan Nama Player: ")
    net.send(playerName)
    roomName = input("Buat Nama Room: ")
    net.send(roomName)
    roomCreated = net.recv()
    if roomCreated:
        print("Room berhasil dibuat")
        return True
    else:
        print("Gagal")
        return False

def playGame():
    print("WIP playGame")

def waitOpp():
    print("Menunggu pemain lain")
    playerReady = net.waitRecv("ready")
    if playerReady:
        playGame()
    else:
        print("Gagal menghubungkan dengan pemain Lain")


def findGame():
    playerName = input("Masukkan Nama Player: ")
    net.send(playerName)

    print("WIP find Game")
    roomList = net.recv()
    for room in enumerate(roomList):
        print(room)
        
    room = input("Pilih room: ")
    room = int(room)
    net.send(roomList[room])
    joinRoom = net.recv()




def menuNew():
    while True:
        try:
            print(banner)
            if net.connect():
                net.send("mode")
                inp = chooseMode()
                if inp == 1:
                    roomCreated = newRoom()
                    if roomCreated:
                        waitOpp()
                elif inp == 2:
                    findGame()
        except KeyboardInterrupt:
            net.client.close()
        break

menuNew()




    



