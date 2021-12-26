import random
from sys import platform

import chess
from display import *
from chess import *



board = Board()
#print(board.legal_moves)

playing = True
while playing:
    display_board(board)
    print("Bonjour Joueur 1 !")
    piece = ""
    while not(re.fullmatch(r'[a-h][1-8]', piece)):
        piece = input("Donnez les coordonnees de la piece que vous souhaitez bouger ( par exemple: a5): ")    
    display_board(board, (ord(piece[0])-97)+(int(piece[1:])-1)*8)

Nf3 = Move.from_uci("a2a4")
Nf4 = Move.from_uci("a7a6")
display_board(board, "a2")

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