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
    #board.fen()
    #board = Board("3rr1k1/pp3p2/1q2p2p/3pPbb1/2pP1p2/P1P2B1P/1P1NQPP1/3RR1K1 w - - 5 28")

    
    print(" Voulez-vous jouer en mode graphique ou console ?  ")
    print("1: Mode graphique")
    print("2: Mode console")
    
    choix=""
    while not(re.fullmatch(r'[1-2]', choix)):
        choix=input("Votre choix ? ")
    choix = int(choix)


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
    elif opponentChoice == 3:
      puzzleGame(board)

    if choix==1:
        graphicalGame(board)
    elif choix:
        consoleGame(board, opponentChoice,ia_level)

def graphicalGame(board:Board):
    board = [['  ' for i in range(8)] for i in range(8)]

    ## Creates instances of chess pieces, so far we got: pawn, king, rook and bishop
    ## The first parameter defines what team its on and the second, what type of piece it is
    
    bp = PieceG('b', 'p', 'ryan60.jpg')
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

    starting_order = initImages() 

    ## This takes in a piece object and its index then runs then checks where that piece can move using separately defined functions for each type of piece.
    def select_moves(piece, index, moves, board):
        if check_team(moves, index, board):
            if piece.type == 'p':
                if piece.team == 'b':
                    return highlight(pawn_moves_b(index, board))
                else:
                    return highlight(pawn_moves_w(index, board))

            if piece.type == 'k':
                return highlight(king_moves(index, board))

            if piece.type == 'r':
                return highlight(rook_moves(index, board))

            if piece.type == 'b':
                return highlight(bishop_moves(index, board))

            if piece.type == 'q':
                return highlight(queen_moves(index, board))

            if piece.type == 'kn':
                return highlight(knight_moves(index, board))

    WIN = pygame.display.set_mode((WIDTH, WIDTH))

    pygame.display.set_caption("Chess")
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    YELLOW = (204, 204, 0)
    BLUE = (50, 255, 255)
    BLACK = (0, 0, 0)

    def make_grid(rows, width):
        grid = []
        gap = WIDTH // rows
        print(gap)
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node = Node(j, i, gap)
                grid[i].append(node)
                if (i+j)%2 ==1:
                    grid[i][j].colour = GREY
        return grid

    def update_display(win, grid, rows, width):
        for row in grid:
            for spot in row:
                spot.draw(win)
                spot.setup(win, starting_order)
        draw_grid(win, rows, width)
        pygame.display.update()


    def Find_Node(pos, WIDTH):
        interval = WIDTH / 8
        y, x = pos
        rows = y // interval
        columns = x // interval
        return int(rows), int(columns)

    def display_potential_moves(positions, grid):
        for i in positions:
            x, y = i
            grid[x][y].colour = BLUE
         

    def Do_Move(OriginalPos, FinalPosition, WIN):
        starting_order[FinalPosition] = starting_order[OriginalPos]
        starting_order[OriginalPos] = None

    create_board(board)
    
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    while True:
        pygame.time.delay(50) ##stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)
                if selected == False:
                    try:
                        possible = select_moves((board[x][y]), (x,y), moves, board)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x,y
                        selected = True
                    except:
                        piece_to_move = []
                        print('Can\'t select')
                    #print(piece_to_move)

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
                            print(convert_to_readable(board))
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
                            print(convert_to_readable(board))
                        else:
                            deselect(board)
                            remove_highlight(grid)
                            selected = False
                            print("Invalid move")
                    selected = False

            update_display(WIN, grid, 8, WIDTH)

def consoleGame(board:Board, opponentChoice:int,ia_level:int):
    movehistory=[]
   
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

def puzzleGame(board):
  file = open('src/level.txt', 'r').read().splitlines()
  print(file)
  level = [ast.literal_eval(i) for i in file]
  pr
  count = 1
  for i in level:
    print("Puzzle " + str(count) + " (MAT en 1) : ")
    while not(board.is_checkmate()) and board.fen() != i[1]:
      board = puzzleBoard(i[0], i[2])
      display_board(board)
      startPosition = getStartingPosition(board)
      display_board(board, getPiece(startPosition))
      newPosition = getNewPosition(board, startPosition)
      move = startPosition+newPosition
      board.push(Move.from_uci(move))
      if board.is_checkmate() and board.fen().split(" ")[0] == i[1]:
        print("Good Job ! Next Puzzle...")
      else:
        print("Try Again !")
      count += 1
  
def puzzleBoard(color:str, level:str):
  return Board(color + level)

if __name__ == "__main__":
    main(board)