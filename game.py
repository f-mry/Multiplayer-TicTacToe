class TicTacToe:
    def __init__(self,):
        
        self.board = ["-", "-", "-",
                      "-", "-", "-",
                      "-", "-", "-"]
        self.gameStatus = True
        self.winner = None
        self.currentPlayer = "X"

        #gameInfo = [board,gameStatus,winner,currentPlayer]
        #gamePlayer = {'X': 'player1', 'O': 'player2'}

    def showBoard(self):
        print("\n")
        print(board[0] + " | " + board[1] + " | " + board[2] + "     1 | 2 | 3")
        print(board[3] + " | " + board[4] + " | " + board[5] + "     4 | 5 | 6")
        print(board[6] + " | " + board[7] + " | " + board[8] + "     7 | 8 | 9")
        print("\n")

    def checkRows(self):
        for i in [ 0,3,6 ]:
            row = self.board[i] == self.board[i+1] == self.board[i+2] != "-"
            if row:
                self.gameStatus = False
                return self.board[i]
                break
        if not row:
            return None
        
    def checkColumns(self):
        for i in [ 0,1,2 ]:
            row = self.board[i] == self.board[i+3] == self.board[i+6] != "-"
            if row:
                self.gameStatus = False
                return self.board[i]
                break
        if not row:
            return None

    def checkDiagonal(self):
        diag1 = self.board[0] == self.board[4] == self.board[8] != "-" 
        diag2 = self.board[2] == self.board[4] == self.board[6] != "-" 

        if diag1 or diag2:
            self.gameStatus = False
        
        if diag1:
            return[0]
        elif diag2:
            return[2]
        else:
            return None

    def checkTie(self):
        if "-" not in self.board:
            self.gameStatus = False
            return True
        else:
            return False
    
    def flipPlayer(self):
        if self.currentPlayer == "X":
            self.currentPlayer = "O"
        elif self.currentPlayer == "O":
            self.currentPlayer = "X"

    def checkWinner(self):
        rowWinner = checkRows
        columnsWinner = checkColumns
        diagonalWinner = checkDiagonal
        
        if rowWinner:
            self.winner = rowWinner
        elif columnsWinner:
            self.winner = columnsWinner
        elif diagonalWinner:
            self.winner = diagonalWinner
        else:
            self.winner = None

    def gameCond(self):
        checkWinner()
        checkTie()

    def handleTurn(self,player):
        print("Giliran ",player)
        position = input("Pilih posisi dari 1-9: ")

        valid = False
        while not valid:
            while int(position) not in range(0,10):
                position = input("Pilih posisi dari 1-9: ")

        position = int(position)

        if self.board[position] == "-":
            valid = True
        else:
            print("Pilih posisi lain!")

        self.board[position] = player

        showBoard()


    def parseGameInfo(self, gameInfo):
        #gameInfo = [board,gameStatus,winner,currentPlayer]
        #gamePlayer = {'X': 'player1', 'O': 'player2'}

        self.board = gameInfo[0]
        self.gameStatus = gameInfo[1]
        self.winner = gameInfo[2]
        self.currentPlayer = gameInfo[3]

        


        



