from datetime import datetime

from chess import *
import random as rd
#import chess.svg
import chess.pgn
import chess.engine
#from IPython.display import SVG
from chess.polyglot import open_reader, MemoryMappedReader


# evaluation of the different position of each piece
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


#This function 
def evaluate_turn(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    # renvoie le nombre de piece(blanc ou  noir) present dans l'echiquier
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
    try:
        move = MemoryMappedReader("/binfile/Perfect2021.bin").weighted_choice(board).move
        return move
    except:
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

#ia vraiment débile, autiste tier
def random_move_selection(board):
    move = rd.choice(board.legal_moves)
    return move

def evaluate_pieces(board):
    sum = 0
    #blanc
    wp = len(board.pieces(chess.PAWN, chess.WHITE))#Pion
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))#Roi
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))#Fou
    wr = len(board.pieces(chess.ROOK, chess.WHITE))#tour
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))#Reine
    #noir
    bp = len(board.pieces(chess.PAWN, chess.BLACK))#Pion
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))#Roi
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))#Fou
    br = len(board.pieces(chess.ROOK, chess.BLACK))#Tour
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))#Reine
    if(board.turn):#si true donc joueur blanc de jouer
        sum = wp+wn+wb+wr+wq
    else:#sinon joueur noir (burk)
        sum = bp+bn+bb+br+bq
    return sum

def fct_ia_expert(board):
    global move
    if (evaluate_pieces(board) <= 16) and (evaluate_pieces(board) > 13):
        move = move_selection(3, board)
    elif (evaluate_pieces(board) <= 13) and (evaluate_pieces(board) > 10):
        move = move_selection(4, board)
    elif (evaluate_pieces(board) <= 10) and (evaluate_pieces(board) > 5):
        move = move_selection(5, board)
    elif (evaluate_pieces(board) <= 5) and (evaluate_pieces(board) > 0):
        move = move_selection(6, board)
    return move

def fct_ia_dif_moy(board,lvl):
  if(lvl):
    move = move_selection(3, board)
  else:
    move = move_selection(1, board) 
    return move

def play_ai(board,ia_level):
    if(ia_level == "4"):
        move = fct_ia_expert(board)
    elif(ia_level == "3"):
        move = fct_ia_dif_moy(board,True)#difficile
    elif(ia_level == "2"):
      move = fct_ia_dif_moy(board,False)#niveau moyen
    else:
      pass
        #move = random_move_selection(board)#Autisme
    return move


"""
if board.is_checkmate():
    if board.turn:
        print("J1 GG")
    else:
        print("J2 GG")

if board.is_stalemate():
    print("match nul")
if board.is_insufficient_material():
    print("match nul")
print(game)
game.add_line(movehistory)
game.headers["Event"] = "Self Tournament 2020"
game.headers["Site"] = "Pune"

game.headers["Round"] = 1
game.headers["White"] = "Ai"
game.headers["Black"] = "Ai"
game.headers["Result"] = str(board.result(claim_draw=True))
"""

#SVG(chess.svg.board(board=board, size=400))

"""
if(game.headers["Result"] == "1/2-1/2"):
    print("match null")
elif(game.headers["Result"] == "1-0":
    print("White win")
else:
    print("Black win")
"""
