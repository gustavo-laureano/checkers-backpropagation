
from src.core.board import Board
from src.core.piece import Piece, Player
from src.app.use_cases.move_validator import MoveValidator, Move
from typing import Optional, list

class GameManager:

    def __init__(self):
        self.board = Board()
        self.validator = MoveValidator()
        self.current_player = Player.WHITE 
        self.winner: Optional[Player] = None
        

        self.legal_moves: list[Move] = []
        
        self._setup_game()

    def _setup_game(self):
        self.board.setup_board()
        self._update_legal_moves()

    def _update_legal_moves(self):
        self.legal_moves = self.validator.get_all_legal_moves_for_player(
            self.board, self.current_player
        )
        
        if not self.legal_moves:
            self.winner = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE

    def _switch_turn(self):
        self.current_player = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE
        self._update_legal_moves()


    def make_move(self, selected_move: Move) -> bool:
        """
        Tenta executar um movimento. A UI ou a IA devem passar
        um dos objetos 'Move' da lista 'self.legal_moves'.
        """
        if selected_move not in self.legal_moves:
            print(f"Erro: Movimento {selected_move} não é legal.")
            return False
            
       
        from_pos = selected_move["from_pos"]
        to_pos = selected_move["to_pos"]
        captures = selected_move["captures"]
        
        piece = self.board.get_piece(from_pos[0], from_pos[1])
        
        self.board.move_piece(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
        
        for cap_pos in captures:
            self.board.remove_piece(cap_pos[0], cap_pos[1])
            
        if piece and not piece.is_king:
            
            if (piece.player == Player.WHITE and to_pos[0] == 0) or \
               (piece.player == Player.BLACK and to_pos[0] == self.board.ROWS - 1):
                
                
                piece.make_king()
        
      
        self._switch_turn()
        return True

    def get_board(self) -> Board:
       
        return self.board

    def get_current_player(self) -> Player:
        
        return self.current_player

    def get_legal_moves(self) -> list[Move]:

        return self.legal_moves
        
    def get_winner(self) -> Optional[Player]:
        return self.winner