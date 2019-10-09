#ticTacToe.py
import pandas as pd

class TicTacToe():
    def __init__(self):
        self.board = self.reset_board()
        self.humans = ""
        
    def start_game(self):
        while self.humans != 1 and self.humans !=2:
            self.humans = int(input("1 or 2 players?\n"))
        
    def reset_board(self):
        board = {i: " " for i in range(3)}
        for i in range(3): board[i] = {i:" "}
        return board
    
    def play_game(self, playerX, playerO):
        
    
    def check_for_win(self, player_symbol):
        
        # Check downright diagonal
        if False not in [self.board[i][i] == player_symbol for i in range(3)]:
            print("Player",player_symbol, "wins")
            print(pd.DataFrame(self.board))
            exit()
        # Check upright diagonal
        if False not in [self.board[i][i] == player_symbol for i in range(2,-1,-1)]:
            print("Player",player_symbol, "wins")
            exit()
        for i in range (3):
            # check vertical lines
            if False not in [self.board[i][j] == player_symbol for j in range(3)]:
                print("Player", player_symbol, "wins")
                exit()
            if False not in [self.board[j][i] == player_symbol for j in range(3)]:
                print("Player", player_symbol, "wins")
                exit()
game = TicTacToe()
