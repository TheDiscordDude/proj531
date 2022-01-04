#import random

import pygame.transform
from display import *
#from attack import *
from pygame import *
from consts import *
import chess.svg
import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP
#import copy
#import pickle 
#from collections import defaultdict 
#from collections import Counter 
#import threading 

def main():
    #board = Board('1nb1kbn1/1pPPppp1/7r/p6p/8/8/PPP2PPP/RNBQKBNR b KQ - 0 8')
    board = Board()
    
    print(" Voulez-vous jouer en mode graphique ou console ?  ")
    print("1: Mode graphique")
    print("2: Mode console")
    
    choix=input("Votre choix ?")
    while not(re.fullmatch(r'[1-2]', choix)):
        choix=input("Votre choix ?")
    choix = int(choix)
    if choix==1:
        graphicalGame(board)
    else:
        consoleGame(board)

def graphicalGame(board:Board):
    pygame.init()
    #Load the screen with any arbitrary size for now:
    screen = pygame.display.set_mode((640,640))

    running = True
    background = pygame.image.load('images/board.png').convert()
    size_of_bg = background.get_rect().size
    pieces_image = pygame.image.load('images/Chess_Pieces_Sprite.png').convert_alpha()
    
    #Get size of the individual squares
    square_width = size_of_bg[0]/8
    square_height = size_of_bg[1]/8
    pieces_image = pygame.transform.scale(pieces_image,(int(square_width*6),int(square_height*2)))


    pygame.display.set_caption('Sigma\'s chess')
    while running :

        pygame.display.flip() 
        screen.blit(background,[0,0])
    #Load the background chess board image:
    #Load an image with all the pieces on it:
   

def consoleGame(board:Board):
    turn = 0
    while not(board.is_checkmate()):
        display_board(board)
        print("A votre tour " + ("Joueur 1" if turn%2==0 else "Joueur 2" ))
        if board.is_check():
            print("Attention l'échéquier est en échec")
        pieceDepart = ""
        pieceArrivee = ""

        while not(re.fullmatch(r'[a-h][1-8]', pieceDepart)) or not(checkPiece(board, pieceDepart)):
            pieceDepart = input("Donnez les coordonnees de la piece que vous souhaitez bouger ( par exemple: a5): ")

        clearConsole()

        display_board(board, getPiece(pieceDepart))

        gestion_attack_pion(pieceDepart)

        while not(re.fullmatch(r'[a-h][1-8]', pieceArrivee)) or not(checkMove(board, pieceDepart, pieceArrivee)):
            pieceArrivee = input("Ou doit aller cette piece ?")
        move = Move.from_uci(pieceDepart+pieceArrivee)

        board.push(move)

        clearConsole()
        print("check:",board.is_check(), "checkmate:", board.is_checkmate())
        print( board.fen())
        turn+=1
        

if __name__ == "__main__":
    main()