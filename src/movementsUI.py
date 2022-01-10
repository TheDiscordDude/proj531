from displayUI import *
from utilsUI import * 
## returns the input if the input is within the boundaries of the board
def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True

## Basically, check black and white pawns separately and checks the square above them. If its free that space gets an "x" and if it is occupied by a piece of the opposite team then that piece becomes killable.
def pawn_moves_b(index, board):
    if index[0] == 1:
        if board[index[0] + 2][index[1]] == '  ' and board[index[0] + 1][index[1]] == '  ':
            board[index[0] + 2][index[1]] = 'x '
    bottom3 = [[index[0] + 1, index[1] + i] for i in range(-1, 2)]

    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'b':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board

def check_team(moves, index, board):
    row, col = index
    if moves%2 == 0:
        if board[row][col].team == 'w':
            return True
    else:
        if board[row][col].team == 'b':
            return True


def pawn_moves_w(index, board):
    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'w':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board


## This just checks a 3x3 tile surrounding the king. Empty spots get an "x" and pieces of the opposite team become killable.
def king_moves(index, board):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        board[index[0] - 1 + y][index[1] - 1 + x].killable = True
    return board



## Same as the rook but this time it creates 4 lists for the diagonal directions and so the list comprehension is a little bit trickier.
def bishop_moves(index, board):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                [[index[0] + i, index[1] - i] for i in range(1, 8)],
                [[index[0] - i, index[1] + i] for i in range(1, 8)],
                [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board



## Checks a 5x5 grid around the piece and uses pythagoras to see if if a move is valid. Valid moves will be a distance of sqrt(5) from centre
def knight_moves(index, board):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    return board

## This creates 4 lists for up, down, left and right and checks all those spaces for pieces of the opposite team. The list comprehension is pretty long so if you don't get it just msg me.
def rook_moves(index, board):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
            [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
            [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
            [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board

## applies the rook moves to the board then the bishop moves because a queen is basically a rook and bishop in the same position.
def queen_moves(index, board):
    board = rook_moves(index, board)
    board = bishop_moves(index, board)
    return board


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