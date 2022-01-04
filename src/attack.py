import random
from display import *
from chess import *
from utils import *
"""
remove_piece_at => remove piece
set_piece_at=> inverse

is_checkmate()


"""
def gestion_attack_pion(pieceDepart):
    if getPiece(pieceDepart):
        return True