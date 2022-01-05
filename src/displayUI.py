from consts import *
from pygame import *
import pygame.transform
import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP

## Creates a chess piece class that shows what team a piece is on, what type of piece it is and whether or not it can be killed by another selected piece.
class PieceG:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image

def create_board(board):
    board[0] = [PieceG('b', 'r', 'bR.png'), PieceG('b', 'kn', 'bN.png'), PieceG('b', 'b', 'bB.png'), \
            PieceG('b', 'q', 'bQ.png'), PieceG('b', 'k', 'bK.png'), PieceG('b', 'b', 'bB.png'), \
            PieceG('b', 'kn', 'bN.png'), PieceG('b', 'r', 'bR.png')]

    board[7] = [PieceG('w', 'r', 'wR.png'), PieceG('w', 'kn', 'wN.png'), PieceG('w', 'b', 'wB.png'), \
            PieceG('w', 'q', 'wQ.png'), PieceG('w', 'k', 'wK.png'), PieceG('w', 'b', 'wB.png'), \
            PieceG('w', 'kn', 'wN.png'), PieceG('w', 'r', 'wR.png')]

    for i in range(8):
        board[1][i] = PieceG('b', 'p', 'bp.png')
        board[6][i] = PieceG('w', 'p', 'wp.png')
    return board

## returns a string that places the rows and columns of the board in a readable manner
def convert_to_readable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output

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