from chess import Board, Move, SquareSet

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
            p = str(i)[2:]
            legal_places.add(getPiece(p))
    return legal_places

def checkPiece(board:Board, coords:str) -> bool:
    """
    Checks if there is a movable piece at the coords
    :param board: The current game board
    :param coord: The coords of the piece we want to move
    :returns: a boolean : True if the piece is movable, False if not 
    """
    piece = getPiece(coords)
    for move in board.legal_moves :
        if move.from_square == piece:
            return True
    return False

def checkMove(board:Board, from_:str, to_:str) -> bool:
    """
    Checks if the move is possible
    :param board: the current game board
    :param from_: the starting square where the piece is 
    :param to_: the ending square where the piece will be
    :returns: a boolean : True if the move is possible, False if not
    """
    return board.is_legal(Move.from_uci(from_+to_))
