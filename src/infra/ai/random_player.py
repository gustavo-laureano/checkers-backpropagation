
import random
from src.core.board import Board
from src.core.piece import Player
from src.app.use_cases.move_validator import Move

class RandomPlayer:

    
    def __init__(self, player: Player):

        self.player = player

    def get_move(self, board: Board, legal_moves: list[Move]) -> Move | None:
      
        if not legal_moves:
            return None
            
        chosen_move = random.choice(legal_moves)
        
        print(f"[AI Player] Movendo de {chosen_move['from_pos']} para {chosen_move['to_pos']}")
        
        return chosen_move