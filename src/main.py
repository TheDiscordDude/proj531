#import random

import pygame.transform
from console.display import *
from displayUI import *
from movementsUI import *
import pygame
import ast

import time

import sys

from pygame import *
from consts import *
import chess.svg

board = Board()

#import copy
#import pickle
#from collections import defaultdict 
#from collections import Counter 
#import threading 

from AI.ai import play_ai
def main(board:Board):
    #board = Board('1nb1kbn1/1pPPppp1/7r/p6p/8/8/PPP2PPP/RNBQKBNR b KQ - 0 8')
    #board = Board("3rr1k1/pp3p2/1q2p2p/3pPbb1/2pP1p2/P1P2B1P/1P1NQPP1/3RR1K1 w - - 5 28")

    
    print(" Voulez-vous jouer en mode graphique ou console ?  ")
    print("1: Mode graphique")
    print("2: Mode console")
    print("3: Mode puzzle")
    
    choice=""
    while not(re.fullmatch(r'[1-3]', choice)):
        choice=input("Votre choix ? ")
    choice = int(choice)

    sigmaChoice = ""
    if choice == 1:
        print("Voulez vous le mode Sigma ?\n"\
                "1. Oui\n"\
                "2. Non")
        while not(re.fullmatch(r'[1-2]', sigmaChoice)):
            sigmaChoice = input("Votre choix ?")
        
        sigmaChoice = int(sigmaChoice)

    print("\nVoulez-vous jouer contre une IA ou contre un joueur ? \n"\
        "1: Contre un Joueur \n"\
        "2: Contre une IA \n"\
        "3: Puzzle \n")
    opponentChoice = ""
    while not(re.fullmatch(r'[1-3]', opponentChoice)):
        opponentChoice = input("Votre choix ? ")
    opponentChoice = int(opponentChoice)

    ia_level=""
    if opponentChoice==2:
        print("Quelle niveau de difficulté ?")
        print("1: Facile")
        print("2: Moyen")
        print("3: Difficile")
        print("4: Expert")
        while not(re.fullmatch(r'[1-4]', ia_level)):
            ia_level = input("Votre choix ? ")
        ia_level = int(ia_level)

    if choice==1:
        graphicalGame(board, sigmaChoice)
    elif choice == 2 :
        consoleGame(board, opponentChoice,ia_level)
    elif choice == 3 :
        puzzleGame()



def graphicalGame(board:Board, sigmaChoice:bool):
    board = [['  ' for i in range(8)] for i in range(8)]

    ## Creates instances of chess pieces, so far we got: pawn, king, rook and bishop
    ## The first parameter defines what team its on and the second, what type of piece it is
    """
    bp = PieceG('b', 'p', 'bp.png')
    wp = PieceG('w', 'p', 'wp.png')
    bk = PieceG('b', 'k', 'bK.png')
    wk = PieceG('w', 'k', 'wK.png')
    br = PieceG('b', 'r', 'bR.png')
    wr = PieceG('w', 'r', 'wR.png')
    bb = PieceG('b', 'b', 'bB.png')
    wb = PieceG('w', 'b', 'wB.png')
    bq = PieceG('b', 'q', 'bQ.png')
    wq = PieceG('w', 'q', 'wQ.png')
    bkn = PieceG('b', 'kn', 'bN.png')
    wkn = PieceG('w', 'kn', 'wN.png')

    if sigmaChoice==1:
        bp = PieceG('b', 'p', 'ryan60.jpg')
        wp = PieceG('w', 'p', 'andrew.jpg')
        bk = PieceG('b', 'k', 'rami.png')
        wk = PieceG('w', 'k', 'loic.jpg')
        br = PieceG('b', 'r', 'calvin.png')
        wr = PieceG('w', 'r', 'etienne.jpg')
        bb = PieceG('b', 'b', 'william.png')
        wb = PieceG('w', 'b', 'axel.jpg')
        bq = PieceG('b', 'q', 'laurianne.jpg')
        wq = PieceG('w', 'q', 'ouijdame.png')
        bkn = PieceG('b', 'kn', 'damien.png')
        wkn = PieceG('w', 'kn', 'adam.png')"""

    starting_order = initImages(sigmaChoice) 

    WIN = pygame.display.set_mode((WIDTH, WIDTH))

    pygame.display.set_caption("Chess")
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    YELLOW = (204, 204, 0)
    BLUE = (50, 255, 255)
    BLACK = (0, 0, 0)

    def Do_Move(OriginalPos, FinalPosition, WIN):
        starting_order[FinalPosition] = starting_order[OriginalPos]
        starting_order[OriginalPos] = None

    board = create_board(board)
    
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    while True:
        pygame.time.delay(int((1/MAX_FPS)*100)) ##stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = find_Node(pos, WIDTH)
                if selected == False:
                    try:
                        possible = select_moves((board[x][y]), (x,y), moves, board)
                        print(type(board))
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x,y#modifier sa pour que l'ia lui envoie sont x,y
                        selected = True
                    except:
                        piece_to_move = []
                        print('Can\'t select')

                else:
                    try:
                        if board[x][y].killable == True:
                            row, col = piece_to_move ## coords of original piece
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect(board)
                            remove_highlight(grid)
                            Do_Move((col, row), (y, x), WIN)
                            moves += 1
                            print("sigma :",convert_to_readable(board))
                        else:
                            deselect(board)
                            remove_highlight(grid)
                            selected = False
                            print("Deselected")
                    except:
                        if board[x][y] == 'x ':
                            row, col = piece_to_move
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect(board)
                            remove_highlight(grid)
                            Do_Move((col, row), (y, x), WIN)
                            moves += 1
                            print('x :',x)#la chose a utiliserr pour l'ia
                            print('y :',y)
                            print()
                            print('col :',col)
                            print('row :',row)
                            print(convert_to_readable(board))
                        else:
                            deselect(board)
                            remove_highlight(grid)
                            selected = False
                            print("Invalid move")
                    selected = False

            update_display(WIN, grid, 8, WIDTH, starting_order)

def consoleGame(board:Board, opponentChoice:int,ia_level:int):
    """
    The main loop for the game in console 
    :param board: the current game board
    :param opponentChoice: choice between pvp (1) or pve (2)
    :param ia_level: the level of the ia
    """
   
    while not(board.is_checkmate()):
        if opponentChoice==2 and board.turn==False:
            move_ai=play_ai(board,ia_level)
            display_board(board)
            board.push(move_ai)
            
            if not(DEV_MODE):
                clearConsole()
        else :
            
            display_board(board)
            print("A votre tour", ("Joueur 1" if board.turn else "Joueur 2" ))
            if board.is_check():
                print("Attention vous êtes en échec")
            
            startPosition = getStartingPosition(board)
            
            if not(DEV_MODE):
                clearConsole()
            
            if DEV_MODE:
                getBoardInfo(board)

            display_board(board, getPiece(startPosition))

            newPosition = getNewPosition(board, startPosition)
            move = startPosition+newPosition
            board.push(Move.from_uci(move))
            
            if not(DEV_MODE):
                clearConsole()

            if DEV_MODE:
                getBoardInfo(board)
            
            
    print(("Joueur 1" if board.turn else "Joueur 2" ), "est en échec et mat,", ("Joueur 2" if board.turn else "Joueur 1" ), "a gagné" )

def puzzleGame():
  file = open('src/level.txt', 'r').read().splitlines()
  level = [ast.literal_eval(i) for i in file]
  count = 1
  print("Bienvenue dans le Mode Puzzle !")
  print("Au travers de différents problèmes, votre but va être de mettre l'adversaire echec et mat en un seul coup.")
  print("Bonne Chance !!!")
  for i in level:
    board = Board()
    print("\nPuzzle " + str(count) + " (MAT en 1) : ")
    print('Vous jouez les "Foncé".') if i[2] == ' w ' else print('Vous jouez les "Clairs".')
    while not(board.is_checkmate()) and board.fen() != i[1]:
      board = puzzleBoard(i[0], i[2])
      display_board(board)
      startPosition = getStartingPosition(board)
      display_board(board, getPiece(startPosition))
      newPosition = getNewPosition(board, startPosition)
      move = startPosition+newPosition
      board.push(Move.from_uci(move))
      if board.is_checkmate() and board.fen().split(" ")[0] == i[1] and i != level[-1]:
        print("Bien joué ! On passe au prochain puzzle ...")
      elif board.is_checkmate() and board.fen().split(" ")[0] == i[1] and i == level[-1]:
        print("Vous avez réussi tout les puzzles ! Bien joué !")
      else:
        print("Essayer une nouvelle fois !")
    count += 1
  return True
  
def puzzleBoard(color:str, level:str):
  return Board(color + level)

if __name__ == "__main__":
    main(board)