from datetime import datetime

from chess import *
import random as rd
import chess.pgn
import chess.engine
from chess.polyglot import open_reader, MemoryMappedReader


#Gives a grid containing the best positions of the pieces
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def evaluate_turn(board):
    """
    This function returns an evaluation of the pieces.
    params: board of the game
    returns: the summation  of the material scores and the individual score for white (positive) and black (negative), in
    case we want to play AI against AI
    """

    # Returns the number of pieces (white or black) present in the chessboard
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    # Material score
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    # individual pieces score
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])

    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

    if board.turn:
        return eval
    else:
        return -eval



def move_selection(depth, board):
    """
    It will select the best move possible according to the parameters
    :params depth: the level of descent in the tree of possible moves
    :params board: the current chess board
    :returns: the best move to play 
    """
    try:
        #Read a book wich contains a lot of opening move
        move = MemoryMappedReader("/binfile/move.bin").weighted_choice(board).move
        return move
    except:
        #If none of the move in the book are suitable,we will have to calculate the best
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000

        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1,board)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            board.pop()
        return bestMove


def alphabeta(alpha, beta, depthleft,board):
    """
    :params alpha: Number that will allow the best move to be calculated
    :params beta: Number that will allow the best move to be calculated
    :params depthleft: Allows to restrict the move search
    :params board: the current chess board

    :returns: the best iteration according to the parameters
    """
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta, board)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1,board)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore


def quiesce(alpha, beta,board):
    """
    :params alpha: Number that will allow the best move to be calculated
    :params beta: Number that will allow the best move to be calculated
    :params board: the current chess board

    :returns: the most "useful" iterations
    """
    stand_pat = evaluate_turn(board)
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat
    for moves in board.legal_moves:
        if board.is_capture(moves):
            board.push(moves)
            score = -quiesce(-beta, -alpha,board)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def random_move_selection(board):
    """
    :params board: the current chess board

    :returns: a random move
    """
    list_leg_move = list(board.legal_moves)#Turns the object into a list
    move = rd.choice(list_leg_move)
    return move


def fct_ia_expert(board):
    """
    :params board:the current chess board
    
    :returns: the best move
    """
    global move
    if (evaluate_turn(board) <= 16) and (evaluate_turn(board) > 13):
        move = move_selection(3, board)
    elif (evaluate_turn(board) <= 13) and (evaluate_turn(board) > 10):
        move = move_selection(4, board)
    elif (evaluate_turn(board) <= 10) and (evaluate_turn(board) > 5):
        move = move_selection(5, board)
    elif (evaluate_turn(board) <= 5) and (evaluate_turn(board) > 0):
        move = move_selection(6, board)
    return move

def fct_ia_dif_moy(board,lvl):
    """
    :params board: the current chess board
    :params lvl: boolean which separates the medium from the hard difficulty

    :returns: the best move
    """
    if(lvl):
        move = move_selection(3, board)
    else:
        move = move_selection(1, board) 
    return move

def play_ai(board,ia_level):
    """
    :params board: the current chess board
    :params ia_level: which separates the medium from the hard difficulty

    :returns: the best move according to the level of difficulty
    """
    if(ia_level == 4):
        move = fct_ia_expert(board)
    elif(ia_level == 3):
        move = fct_ia_dif_moy(board,True)#difficile
    elif(ia_level == 2):
        move = fct_ia_dif_moy(board,False)#niveau moyen
    else:
        move = random_move_selection(board)#
    return move
