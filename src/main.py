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

showBoard(board)