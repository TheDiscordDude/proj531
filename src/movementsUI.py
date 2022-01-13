from displayUI import *
from utilsUI import * 
from consts import DEV_MODE
from AI.ai import play_ai

def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True


def pawn_moves_b(index, gridBoard):
    """
    pawn_moves_b is the function allowing to move the pawn in the black team
    :param index: type list is the position of the pawn
    :param gridboard: type list is the board
    :returns: the new gridboard
    """
    if index[0] == 1:
        if gridBoard[index[0] + 2][index[1]] == '  ' and gridBoard[index[0] + 1][index[1]] == '  ':
            gridBoard[index[0] + 2][index[1]] = 'x '
    bottom3 = [[index[0] + 1, index[1] + i] for i in range(-1, 2)]

    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if gridBoard[positions[0]][positions[1]].team != 'b':
                        gridBoard[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if gridBoard[positions[0]][positions[1]] == '  ':
                    gridBoard[positions[0]][positions[1]] = 'x '
    return gridBoard



def check_team(moveCounter, index, gridBoard):
    """
    check_team is the function checking if the move is possible
    :param index: type list is the position of the piece
    :param moveCounter: number of moves from the begining
    :param gridBoard: type list is the board represneted by 2 dimensionnal list
    :returns: a boolean if it is the turn of the index's team 
    """
    row, col = index
    if moveCounter%2 == 0:
        return gridBoard[row][col].team == 'w'
    else:
        return gridBoard[row][col].team == 'b'
       

def pawn_moves_w(index, gridBoard):
    """
    pawn_moves_w is the function allowing to move the pawn in the white team
    :param index: type list is the position of the pawn
    :param gridboard: type list is the board
    :returns: the new gridboard
    """
    if index[0] == 6:
        if gridBoard[index[0] - 2][index[1]] == '  ' and gridBoard[index[0] - 1][index[1]] == '  ':
            gridBoard[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if gridBoard[positions[0]][positions[1]].team != 'w':
                        gridBoard[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if gridBoard[positions[0]][positions[1]] == '  ':
                    gridBoard[positions[0]][positions[1]] = 'x '
    return gridBoard

def king_moves(index, gridBoard):
    """
    king_moves is the function allowing to move the king
    :param index: type list is the position of the king
    :param gridboard: type list is the board
    :returns: the new gridboard
    """
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if gridBoard[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    gridBoard[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if gridBoard[index[0] - 1 + y][index[1] - 1 + x].team != gridBoard[index[0]][index[1]].team:
                        gridBoard[index[0] - 1 + y][index[1] - 1 + x].killable = True
    return gridBoard




def bishop_moves(index, gridBoard):
    """
    bishop_moves is the function allowing to move the bishop
    :param index: type list is the position of the bishop
    :param gridBoard: type list is the board
    :returns: the new gridboard
    """
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                [[index[0] + i, index[1] - i] for i in range(1, 8)],
                [[index[0] - i, index[1] + i] for i in range(1, 8)],
                [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if gridBoard[positions[0]][positions[1]] == '  ':
                    gridBoard[positions[0]][positions[1]] = 'x '
                else:
                    if gridBoard[positions[0]][positions[1]].team != gridBoard[index[0]][index[1]].team:
                        gridBoard[positions[0]][positions[1]].killable = True
                    break
    return gridBoard




def knight_moves(index, gridBoard):
    """
    knight_moves is the function allowing to move the knight
    :param index: type list is the position of the knight
    :param gridboard: type list is the board
    :returns: the new gridboard
    """
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if gridBoard[index[0] + i][index[1] + j] == '  ':
                        gridBoard[index[0] + i][index[1] + j] = 'x '
                    else:
                        if gridBoard[index[0] + i][index[1] + j].team != gridBoard[index[0]][index[1]].team:
                            gridBoard[index[0] + i][index[1] + j].killable = True
    return gridBoard


def rook_moves(index, gridBoard):
    """
    rook_moves is the function allowing to move the rook
    :param index: type list is the position of the rook
    :param gridBoard: type list is the board
    :returns: the new gridboard
    """
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
            [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
            [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
            [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if gridBoard[positions[0]][positions[1]] == '  ':
                    gridBoard[positions[0]][positions[1]] = 'x '
                else:
                    if gridBoard[positions[0]][positions[1]].team != gridBoard[index[0]][index[1]].team:
                        gridBoard[positions[0]][positions[1]].killable = True
                    break
    return gridBoard


def queen_moves(index, gridBoard):
    """
    queen_moves is the function allowing to move the queen
    :param index: type list is the position of the queen
    :param gridBoard: type list is the board
    :returns: the new gridboard
    """
    gridBoard = rook_moves(index, gridBoard)
    gridBoard = bishop_moves(index, gridBoard)
    return gridBoard


def select_moves(WIN,opponentChoice,starting_order,piece, index, moves, gridBoard,board,grid,WIDTH):
    """
    select_moves is the function highlighting the move possible for each piece
    :param index: type list is the position of the piece
    :param gridBoard: type list is the board
    :param piece: type str is the piece
    :returns: the gridboard with highlighted move  for piece choosen
    
    """
    if check_team(moves, index, gridBoard):
        if piece.type == 'p':
            if piece.team == 'b':
                return highlight(pawn_moves_b(index, gridBoard))
            else:
                return highlight(pawn_moves_w(index, gridBoard))

        if piece.type == 'k':
            return highlight(king_moves(index, gridBoard))

        if piece.type == 'r':
            return highlight(rook_moves(index, gridBoard))

        if piece.type == 'b':
            return highlight(bishop_moves(index, gridBoard))

        if piece.type == 'q':
            return highlight(queen_moves(index, gridBoard))

        if piece.type == 'kn':
            return highlight(knight_moves(index, gridBoard))
            

def do_Move(OriginalPos, FinalPosition, starting_order, WIN, board):
    if DEV_MODE:
        print("Move : ", OriginalPos, FinalPosition)
    starting_order[FinalPosition] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None
    uciMove = convert_custom_move_to_uci([OriginalPos, FinalPosition])
    board.push_uci(uciMove)
    if DEV_MODE:
        print(board)
        print(board.fen())
    return starting_order

def do_move_AI(board, ia_level, starting_order, gridBoard):
    
    move = play_ai(board, ia_level)

    customMove = convert_uci_move_to_custom_list(move)

    starting_order[customMove[1]] = starting_order[customMove[0]]
    starting_order[customMove[0]] = None

    gridBoard[customMove[1][1]][customMove[1][0]] = gridBoard[customMove[0][1]][customMove[0][0]] 
    gridBoard[customMove[0][1]][customMove[0][0]] = '  '

    board.push(move)
    

    return starting_order