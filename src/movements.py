from chess import Board, Move, SquareSet
import re

def getPiece(coords:str) -> int:
    """
    Changes the format of the coord from uci to int
    :param coords: the coordinate of the piece (a5 for example)
    :returns: an integer representing the piece
    """
    return (ord(coords[0])-97)+(int(coords[1:])-1)*8

def getLegalPlaces(piece, board):
    legal_places = SquareSet()
    for i in board.legal_moves:
        if i.from_square == piece:
            p = str(i)[2:4]
            legal_places.add(getPiece(p))
    return legal_places

def checkPiece(board:Board, coords:str) -> bool:
    """
    Checks if there is a movable piece at the coords
    :param board: The current game board
    :param coord: The coords of the piece we want to move
    :returns: a boolean : True if the piece is movable, False if not 
    """
    if not(re.fullmatch(r'[a-h][1-8]', coords)):
        return False

    piece = getPiece(coords)
    for move in board.legal_moves :
        if move.from_square == piece:
            return True
    return False

def checkMove(board:Board, from_:str, to_:str) -> bool:
    """
    Checks if the move is possible.
    It doesn't check if the piece needs to be changed.
    :param board: the current game board
    :param from_: the starting square where the piece is 
    :param to_: the ending square where the piece will be
    :returns: a boolean : True if the move is possible, False if not
    """

    if not(re.fullmatch(r'[a-h][1-8]', to_)):
        return False

    return board.is_legal(Move.from_uci(from_+to_)) or board.is_legal(Move.from_uci(from_+to_+"r"))

def getStartingPosition(board:Board) -> str:
    startingPosition=""
    while not(checkPiece(board, startingPosition)):
        startingPosition = input("Donnez les coordonnees de la piece que vous souhaitez bouger ( par exemple: a5): ")
    return startingPosition

def getNewPosition(board:Board, startingPosition:str) -> str:
    newPiece = ""
    newPosition=""

    while not(checkMove(board, startingPosition, newPosition)):
        newPosition = input("Ou doit aller cette piece ?")

    if not(board.is_legal(Move.from_uci(startingPosition+newPosition))):
        while not(re.fullmatch(r'[q|r|b|n]', newPiece)):
            newPiece = input("Vous pouvez transformer cette piece en une autre.\nQuelle est la nouvelle piece que vous voulez : \nReine : q\nTour : r\nFou : b\nCavalier : n\n")
    return newPosition+newPiece
    
def getBoardInfo(board:Board):
    print("check:",board.is_check(), "checkmate:", board.is_checkmate(), "turn", board.turn)
    print( board.fen())