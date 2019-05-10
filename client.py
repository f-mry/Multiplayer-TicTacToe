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
            
            # while 1:
            #     if net.recv() == "ready":
            #         print("Ready")
            #         play()
            #     else:
            #         print(".",sep='.')
            

menu()




    



