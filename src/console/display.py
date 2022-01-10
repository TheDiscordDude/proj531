import enum
from console.movements import *

class COLORS:
    WHITE = '\033[96m'
    BLACK = '\033[94m'
    LEGAL_PLACES = '\033[1;32m' 
    CHOSEN_PIECE = '\033[1;33m'
    ENDC = '\033[0m'

def clearConsole():
    print('\033[H\033[J', end='')

def display_board(board: Board, chosen_piece:int=None):
    """
    Displays the board
    :param board: the current chess Board used
    :param chosen_piece: all the possible moves for this piece will be displayed
    :returns: nothing
    """
    str_board = [[] for i in range(9)]
    legal_places = SquareSet()
    positionY = 7
    positionX = 0
    nbLigne = 0
    print("chosen_piece None ?", chosen_piece)
    if not(chosen_piece is None) :
        legal_places = getLegalPlaces(chosen_piece, board)

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
        
        elif positionX+positionY*8 == chosen_piece:
            str_board[nbLigne].append(COLORS.CHOSEN_PIECE + caractere + COLORS.ENDC)
            positionX+=1

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