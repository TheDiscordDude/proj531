import random
from display import *
import chess
board = chess.Board()
#print(board.legal_moves)
Nf3 = chess.Move.from_uci("a2a4")
Nf4 = chess.Move.from_uci("a7a6")
display_board(board)

#move = chess.Move(chess.A3, chess.A3)
#board.push(move)
board.push(Nf3)
print('is cap :', board.is_capture(Nf3))
board.push(Nf4)
board.turn = False
print('board turn :', board.turn)
print(board.legal_moves.count())
display_board(board)

# random comment