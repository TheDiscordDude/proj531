import enum
from utils import getPiece

class COLORS:
    WHITE = '\033[96m'
    BLACK = '\033[94m'
    LEGAL_PLACES = '\33[91m'
    ENDC = '\033[0m'

def display_board(board, chosen_piece=None):
    str_board = [[] for i in range(9)]
    legal_places = []
    positionY = 7
    positionX = 0
    nbLigne = 0
    if chosen_piece :
        for i in board.legal_moves:
            if i.from_square == chosen_piece:
                piece = str(i)[2:]
                legal_places.append(getPiece(piece))

    for caractere in str(board):
        if caractere == ".":
            if positionX+positionY*8 in legal_places:
                str_board[nbLigne].append(COLORS.LEGAL_PLACES + caractere + COLORS.ENDC)
            else : 
                str_board[nbLigne].append(caractere)
            positionX += 1

        elif caractere == " ":
            str_board[nbLigne].append(caractere)
            
        elif caractere == "\n":
            nbLigne+=1
            positionX=0
            positionY-=1

        elif caractere.islower():
            if positionX+positionY*8 in legal_places:
                str_board[nbLigne].append(COLORS.LEGAL_PLACES + caractere + COLORS.ENDC)
            else : 
                str_board[nbLigne].append(COLORS.BLACK + caractere + COLORS.ENDC)
            positionX+=1

        elif caractere.isupper():
            if positionX+positionY*8 in legal_places:
                str_board[nbLigne].append(COLORS.LEGAL_PLACES + caractere + COLORS.ENDC)
            else : 
                str_board[nbLigne].append(COLORS.WHITE + caractere + COLORS.ENDC)
            positionX+=1

    for i in range(0,8):
        str_board[i].insert(0, str(8-i) + " ")

    str_board[8]= ["  ", "a ", "b ", "c ", "d ", "e ", "f ", "g ", "h "]
    for ligne in str_board:
        for colone in ligne :
            print(colone, end="")
        print()