import random

import pygame.transform

from display import *
from chess import *
from attack import *
from pygame import *
WIDTH=HEIGHT=400
DIMENSION=8
SQ_SIZE=HEIGHT/DIMENSION
MAX_FPS=15
IMAGES={}


def loadImages():
    pieces=["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bK","bQ"]
    for piece in pieces:
        IMAGES[piece]= pygame.transform.scale(pygame.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))


def drawGame(screen):
    drawBoard(screen)
    drawPieces(screen)

def drawBoard(screen):
    colors=[pygame.Color("white"),pygame.Color("gray")]
    for w in range(DIMENSION):
        for h in range(DIMENSION):
            color=colors[((w+h)%2)]
            pygame.draw.rect(screen,color,pygame.Rect(h*SQ_SIZE,w*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for w in range(DIMENSION):
        for h in range(DIMENSION):

def main():
    board = Board()
    playing = True
    print(" Voulez-vous jouer en mode graphique ou console ?  ")
    print("1: Mode graphique")
    print("2: Mode console")

    choix=input("Votre choix ?")
    if choix==1:
        pygame.init()
        screen=pygame.display.set_mode((WIDTH,HEIGHT))
        screen.fill(pygame.color("white"))
        loadImages()
        run=True
        while run:
            for ev in pygame.event.get():
                if ev.type==pygame.quit():
                    run=False

            pygame.display.flip()
    else:

        while playing:
            display_board(board)
            print("Bonjour Joueur 1 !")
            pieceDepart = ""
            pieceArrivee = ""

            while not(re.fullmatch(r'[a-h][1-8]', pieceDepart)) or not(checkPiece(board, pieceDepart)):
                pieceDepart = input("Donnez les coordonnees de la piece que vous souhaitez bouger ( par exemple: a5): ")

            #clearConsole()
            display_board(board, getPiece(pieceDepart))

            gestion_attack_pion(pieceDepart)

            while not(re.fullmatch(r'[a-h][1-8]', pieceArrivee)) or not(checkMove(board, pieceDepart, pieceArrivee)):
                pieceArrivee = input("Ou doit aller cette piece ?")
            move = Move.from_uci(pieceDepart+pieceArrivee)

            board.push(move)

            #clearConsole()

"""
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
"""
# random comment

if __name__ == "__main__":
    main()