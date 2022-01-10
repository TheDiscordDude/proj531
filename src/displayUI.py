from consts import *
from pygame import *
import pygame.transform
import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP
from utilsUI import * 




def create_board(board):
    board[0] = [PieceG('b', 'r', 'bR.png'), PieceG('b', 'kn', 'bN.png'), PieceG('b', 'b', 'bB.png'), \
            PieceG('b', 'q', 'bQ.png'), PieceG('b', 'k', 'bK.png'), PieceG('b', 'b', 'bB.png'), \
            PieceG('b', 'kn', 'bN.png'), PieceG('b', 'r', 'bR.png')]

    board[7] = [PieceG('w', 'r', 'wR.png'), PieceG('w', 'kn', 'wN.png'), PieceG('w', 'b', 'wB.png'), \
            PieceG('w', 'q', 'wQ.png'), PieceG('w', 'k', 'wK.png'), PieceG('w', 'b', 'wB.png'), \
            PieceG('w', 'kn', 'wN.png'), PieceG('w', 'r', 'wR.png')]

    for i in range(8):
        board[1][i] = PieceG('b', 'p', 'ryan60.jpg')
        board[6][i] = PieceG('w', 'p', 'wp.png')
    return board



def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

"""
The nodes are all white so this we need to draw the grey lines that separate all the chess tiles
from each other and that is what this function does"""


## Takes in board as argument then returns 2d array containing positions of valid moves
def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                try:
                    if board[i][j].killable:
                        highlighted.append((i, j))
                except:
                    pass
    return highlighted


def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid
"""this takes in 2 co-ordinate parameters which you can get as the position of the piece and then the position of the node it is moving to
you can get those co-ordinates using my old function for swap"""


def initImages():
    images = {
        (0, 0): pygame.image.load('images/bR.png'), 
        (1, 0): pygame.image.load('images/bN.png'),
        (2, 0): pygame.image.load('images/bB.png'), 
        (3, 0): pygame.image.load('images/bQ.png'),
        (4, 0): pygame.image.load('images/bK.png'), 
        (5, 0): pygame.image.load('images/bB.png'),
        (6, 0): pygame.image.load('images/bN.png'), 
        (7, 0): pygame.image.load('images/bR.png'),
        (0, 1): pygame.image.load('images/ryan60.jpg'), 
        (1, 1): pygame.image.load('images/ryan60.jpg'),
        (2, 1): pygame.image.load('images/ryan60.jpg'), 
        (3, 1): pygame.image.load('images/ryan60.jpg'),
        (4, 1): pygame.image.load('images/ryan60.jpg'), 
        (5, 1): pygame.image.load('images/ryan60.jpg'),
        (6, 1): pygame.image.load('images/ryan60.jpg'), 
        (7, 1): pygame.image.load('images/ryan60.jpg'),
        (0, 2): None, 
        (1, 2): None, 
        (2, 2): None, 
        (3, 2): None,
        (4, 2): None, 
        (5, 2): None,
        (6, 2): None, 
        (7, 2): None,
        (0, 3): None, 
        (1, 3): None, 
        (2, 3): None, 
        (3, 3): None,
        (4, 3): None, 
        (5, 3): None, 
        (6, 3): None, 
        (7, 3): None,
        (0, 4): None, 
        (1, 4): None, 
        (2, 4): None, 
        (3, 4): None,
        (4, 4): None, 
        (5, 4): None, 
        (6, 4): None, 
        (7, 4): None,
        (0, 5): None, 
        (1, 5): None, 
        (2, 5): None, 
        (3, 5): None,
        (4, 5): None, 
        (5, 5): None, 
        (6, 5): None, 
        (7, 5): None,
        (0, 6): pygame.image.load('images/wp.png'), 
        (1, 6): pygame.image.load('images/wp.png'),
        (2, 6): pygame.image.load('images/wp.png'), 
        (3, 6): pygame.image.load('images/wp.png'),
        (4, 6): pygame.image.load('images/wp.png'), 
        (5, 6): pygame.image.load('images/wp.png'),
        (6, 6): pygame.image.load('images/wp.png'), 
        (7, 6): pygame.image.load('images/wp.png'),
        (0, 7): pygame.image.load('images/wR.png'), 
        (1, 7): pygame.image.load('images/wN.png'),
        (2, 7): pygame.image.load('images/wB.png'), 
        (3, 7): pygame.image.load('images/wQ.png'),
        (4, 7): pygame.image.load('images/wK.png'),
        (5, 7): pygame.image.load('images/wB.png'),
        (6, 7): pygame.image.load('images/wN.png'), 
        (7, 7): pygame.image.load('images/wR.png')}
    return (images)