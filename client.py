from network import Network
from game import TicTacToe
import os
import time

net = Network()
game = TicTacToe()
score = ''
playerSym = ''
banner = """
 _____  _  ____    _____  ____  ____    _____  ____  _____
/__ __\/ \/   _\  /__ __\/  _ \/   _\  /__ __\/  _ \/  __/
  / \  | ||  /      / \  | / \||  /      / \  | / \||  \  
  | |  | ||  \_     | |  | |-|||  \_     | |  | \_/||  /_ 
  \_/  \_/\____/    \_/  \_/ \|\____/    \_/  \____/\____\
"""

def restartGame():
    restart = ''
    while 1:
        restart = input("Main Lagi?(Y/n: )")
        if restart == "Y" or restart == "n":
            break
    if restart == 'n':
        net.send("stop")
        return False
    elif restart == 'Y':
        net.send("restart")
        response = net.recv()
        if response == "stop":
            print("Lawan sudah berhenti")
            return False
        else:
            return True



def play():
    global game
    global score
    # print("WIP play")
    # print(playerSym)
    # send = playerSym
    plName = input("Masukkan Nama player: ")
    net.send(plName)
    data = net.recv()
    for op in data:
        if op != plName:
            opp = op
    print("Lawan: ",opp)
    score = {plName: 0, opp: 0}
    play = True
    while play:
        while True:
            gameinfo = net.recv()
            game.parseGameInfo(gameinfo)
            game.gameCond()
            if game.gameStatus:
                if game.currentPlayer == playerSym:
                    print("{} -{}-- VS --{}-  {}".format(plName,score[plName],score[opp],opp))
                    game.showBoard()
                    game.handleTurn()
                    game.flipPlayer()
                    net.send(["gameInfo",game.makeGameInfo()])
                else:
                    print("Tunggu Giliran")
            else:
                break
        print("Game selesai")
        if game.winner == playerSym:
            score[plName] += 1
        else:
            score[opp] += 1

        print("Score: \n{}: {}\n{}: {}".format(plName,score[plName],opp,score[opp]))
        net.send("endgame")
        play = restartGame()


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
            

menu()
