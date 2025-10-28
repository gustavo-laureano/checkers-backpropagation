
from enum import Enum

class Player(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

class Piece:
    
    def __init__(self, player: Player):

        self.player = player
        self.is_king = False

    def make_king(self):
        self.is_king = True

    def __repr__(self) -> str:
        """        
        W = Peça Branca (WHITE)
        WK = Dama Branca (WHITE KING)
        B = Peça Preta (BLACK)
        BK = Dama Preta (BLACK KING)
        """
        if self.player == Player.WHITE:
            return "WK" if self.is_king else "W"
        else:
            return "BK" if self.is_king else "B"