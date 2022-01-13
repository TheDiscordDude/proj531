from consts import *

import pygame
"""create a pieces class letting us know wich type of piece ,wich color,l'image , if killable is the piece"""

class PieceG:
    def __init__(self, team, type, image="", killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image

"""create a node class letting us know if eache node on the grid is occupied and the color of each node"""

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.color = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN, starting_order):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] == None:
                pass
            else:
                WIN.blit(starting_order[(self.row, self.col)], (self.x, self.y))



def convert_to_readable(gridBoard):
    """
    function allowing us to be able to read the grid
    :param gridBoard: type list
    :returns: the gridboard but readable 
    """
    output = ''

    for i in gridBoard:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output


## resets "x's" and killable pieces
def deselect(gridBoard):
    for row in range(len(gridBoard)):
        for column in range(len(gridBoard[0])):
            if gridBoard[row][column] == 'x ':
                gridBoard[row][column] = '  '
            else:
                try:
                    gridBoard[row][column].killable = False
                except:
                    pass
    return convert_to_readable(gridBoard)

def display_potential_moves(positions, grid):
    """
    function that put the potential move in blue case
    :param positions: type list 
    :param grid: type list
    """
    for i in positions:
        x, y = i
        grid[x][y].color = BLUE

def find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    if DEV_MODE:
        print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].color = GREY
    return grid

def convert_custom_move_to_uci(move:list):
    carac_change = [chr(i) for i in range(104, 96, -1)]
    firstPos = carac_change[7+move[0][0]*-1] + str(move[0][1]*-1+8)
    endPos = carac_change[7+move[1][0]*-1] + str(move[1][1]*-1+8)

    uciMove = firstPos+endPos
    if DEV_MODE:
        print("UCI Move:", uciMove)
    return uciMove


def convert_uci_move_to_custom_list(move):
    uciMove = move.uci()
    from_ = uciMove[0:2]
    to_ = uciMove[2:4]

    startPosition = (ord(from_[0])-97, 8 - int(from_[1]) )
    endPosition = (ord(to_[0])-97, 8 - int(to_[1]) )
    if DEV_MODE:
        print("custom :", [startPosition,endPosition])
    return [startPosition,endPosition]