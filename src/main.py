import random

import chess

class COLORS:
    WHITE = '\033[96m'
    BLACK = '\033[94m'
    ENDC = '\033[0m'

board = chess.Board()

def showBoard(board):
    nstr = ""
    for i in str(board):
        if i in [".", "\n", " "]:
            nstr+=i
        elif i.islower():
            nstr+=COLORS.BLACK + i + COLORS.ENDC
        elif i.isupper():
            nstr+=COLORS.WHITE + i + COLORS.ENDC
    
    print(nstr)
#print(board.legal_moves)
move = chess.Move(chess.A2, chess.A3)
board.push(move)
print(board.turn)
showBoard(board)


