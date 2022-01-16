import pygame.transform
from console.display import *
from displayUI import *
from movementsUI import *
from movementsUI import do_Move
import pygame
import ast
import time
import sys
from pygame import *
from consts import *
from AI.ai import play_ai


def main(board:Board):
    """
    The Main operative function

    :param board: the current game board
    """

    print(" Voulez-vous jouer en mode graphique ou console ?  ")
    print("1: Mode graphique")
    print("2: Mode console")
    print("3: Mode puzzle")
    
    choice=""
    sigmaChoice = ""
    opponentChoice = 1
    ia_level=""

    while not(re.fullmatch(r'[1-3]', choice)):
        choice=input("Votre choix ? ")
    choice = int(choice)

    if choice == 1:
        print("Voulez vous le mode Sigma ?\n"\
                "1. Oui\n"\
                "2. Non")
        while not(re.fullmatch(r'[1-2]', sigmaChoice)):
            sigmaChoice = input("Votre choix ?")
        
        sigmaChoice = int(sigmaChoice)
    if choice != 3:
        print("\nVoulez-vous jouer contre une IA ou contre un joueur ? \n"\
            "1: Contre un Joueur \n"\
            "2: Contre une IA \n")
        opponentChoice = ""
        while not(re.fullmatch(r'[1-3]', opponentChoice)):
            opponentChoice = input("Votre choix ? ")
        opponentChoice = int(opponentChoice)

    
    if opponentChoice ==2 and choice != 3:
        print("Quelle niveau de difficulté ?")
        print("1: Facile")
        print("2: Moyen")
        print("3: Difficile")
        print("4: Expert")
        while not(re.fullmatch(r'[1-4]', ia_level)):
            ia_level = input("Votre choix ? ")
        ia_level = int(ia_level)

    if choice==1:
        graphicalGame(board, sigmaChoice, opponentChoice, ia_level)
    elif choice == 2 :
        consoleGame(board, opponentChoice,ia_level)
    elif choice == 3 :
        puzzleGame()

def graphicalGame(board:Board, sigmaChoice:bool, opponentChoice:int, ia_level=1):
    """ Creates instances of chess pieces,
    The first parameter defines what the team color its on and the second, the type of piece it is
    """
    
    starting_order = initImages(sigmaChoice) 
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Chess")

    gridBoard = create_board()
    """
    The main loop for the game in graphicalGame against 1 friend
    """

    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    while not(board.is_checkmate()):
        pygame.time.delay(int((1/MAX_FPS)*100)) ##stops cpu dying
        print(moves,board.turn)
        if opponentChoice==2 and board.turn == False and moves%2 != 0 : 
            do_move_AI(board, ia_level, starting_order, gridBoard)
            
        else : 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    y, x = find_Node(pos, WIDTH)
                    if selected == False:
                        try:
              
                            possibleMoves = select_moves(WIN,opponentChoice,starting_order,(gridBoard[x][y]), (x,y), moves, gridBoard, board,grid,WIDTH)
                            print(type(gridBoard))
                            print(possibleMoves)
                            if possibleMoves is None:
                                moves=moves+1
                                board.turn=True
                            else:
                                for positions in possibleMoves:
                                    row, col = positions
                                    grid[row][col].color = BLUE
                                piece_to_move = x,y # modifier sa pour que l'ia lui envoie sont x,y
                                selected = True

                        except:
                            piece_to_move = []
                            print('No possible moves for piece at', x, y)

                    else:
                        try:
                            if gridBoard[x][y].killable == True:
                                row, col = piece_to_move ## coords of original piece
                                gridBoard[x][y] = gridBoard[row][col]
                                gridBoard[row][col] = '  '
                                deselect(gridBoard)
                                remove_highlight(grid)
                                starting_order = do_Move((col, row), (y, x), starting_order, WIN, board)
                                moves += 1

                                if DEV_MODE:
                                    print("sigma :",convert_to_readable(gridBoard))

                            else:
                                deselect(gridBoard)
                                remove_highlight(grid)
                                selected = False
                                if DEV_MODE:
                                    print("Deselected")
                        except :
                            if gridBoard[x][y] == 'x ':
                                row, col = piece_to_move
                                gridBoard[x][y] = gridBoard[row][col]
                                gridBoard[row][col] = '  '
                                deselect(gridBoard)
                                remove_highlight(grid)
                                starting_order = do_Move((col, row), (y, x), starting_order, WIN, board)
                                moves += 1
                                if DEV_MODE:
                                    print('x :',x)#la chose a utiliserr pour l'ia
                                    print('y :',y)
                                    print()
                                    print('col :',col)
                                    print('row :',row)
                                    print(convert_to_readable(gridBoard))
                            else:
                                deselect(gridBoard)
                                remove_highlight(grid)
                                selected = False
                                if DEV_MODE:
                                    print("Invalid move")
                        selected = False
            
            update_display(WIN, grid, 8, WIDTH, starting_order)
            
           
    print("L'équipe", ("Noir" if  board.turn else "Blanc"), "a gagné")

def consoleGame(board:Board, opponentChoice:int,ia_level:int):
    """
    The main loop for the game in console 
    
    :param board: the current game board
    :param opponentChoice: choice between PvP (1) or PvE (2)
    :param ia_level: the level of the ia
    """
   
    while not(board.is_checkmate()):
        if opponentChoice==2 and board.turn==False:
            print("L\'IA réfléchie ...")
            move_ai=play_ai(board,ia_level)
            display_board(board)
            board.push(move_ai)
            
            if not(DEV_MODE):
                clearConsole()
        else :
            display_board(board)
            print("A votre tour", ("Joueur 1" if board.turn else "Joueur 2" ))
            if board.is_check():
                print("Attention vous êtes en échec")
            
            startPosition = getStartingPosition(board)
            
            if not(DEV_MODE):
                clearConsole()
            
            if DEV_MODE:
                getBoardInfo(board)

            display_board(board, getPiece(startPosition))

            newPosition = getNewPosition(board, startPosition)
            move = startPosition+newPosition
            board.push(Move.from_uci(move))
            
            if not(DEV_MODE):
                clearConsole()

            if DEV_MODE:
                getBoardInfo(board)
            
            
    print(("Joueur 1" if board.turn else "Joueur 2" ), "est en échec et mat,", ("Joueur 2" if board.turn else "Joueur 1" ), "a gagné" )

def puzzleGame():
    file = open('src/level.txt', 'r').read().splitlines()
    level = [ast.literal_eval(i) for i in file]
    count = 1
    print("Bienvenue dans le Mode Puzzle !")
    print("Au travers de différents problèmes, votre but va être de mettre l'adversaire echec et mat en un seul coup.")
    print("Bonne Chance !!!")

    for i in level:
        board = Board()
        print("\nPuzzle " + str(count) + " (MAT en 1) : ")
        print('Vous jouez les "Foncé".') if i[2] == ' w ' else print('Vous jouez les "Clairs".')

        while not(board.is_checkmate()) and board.fen() != i[1]:
            board = puzzleBoard(i[0], i[2])
            display_board(board)
            startPosition = getStartingPosition(board)
            display_board(board, getPiece(startPosition))
            newPosition = getNewPosition(board, startPosition)
            move = startPosition+newPosition
            board.push(Move.from_uci(move))

            if board.is_checkmate() and board.fen().split(" ")[0] == i[1] and i != level[-1]:
                print("Bien joué ! On passe au prochain puzzle ...")

            elif board.is_checkmate() and board.fen().split(" ")[0] == i[1] and i == level[-1]:
                print("Vous avez réussi tout les puzzles ! Bien joué !")
                
            else:
                print("Essayer une nouvelle fois !")
        count += 1
    return True
  
def puzzleBoard(color:str, level:str):
    return Board(color + level)

if __name__ == "__main__":
    board = Board()
    main(board)