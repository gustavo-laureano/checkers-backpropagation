import torch
from src.core.board import Board
from src.core.piece import Piece, Player
from src.app.use_cases.move_validator import Move
from .model import CheckersNet, board_to_tensor
from typing import Optional

class NeuralNetPlayer:
    
    def __init__(self, player: Player, model_path: str):
        self.player = player
        self.model = CheckersNet()
        
        try:
            # Tenta carregar o modelo (CPU por padrão)
            self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            print(f"Modelo {model_path} carregado com sucesso.")
        except FileNotFoundError:
            print(f"Aviso: Arquivo de modelo {model_path} não encontrado. IA jogará com pesos aleatórios.")
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}. IA jogará com pesos aleatórios.")

        self.model.eval()

    def _simulate_move_on_board(self, board: Board, move: Move) -> Board:

        temp_board = board.deep_copy()
        
        from_pos = move["from_pos"]
        to_pos = move["to_pos"]
        captures = move["captures"]
        
        piece = temp_board.get_piece(from_pos[0], from_pos[1])
        temp_board.move_piece(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
        
        for cap_pos in captures:
            temp_board.remove_piece(cap_pos[0], cap_pos[1])
            
        # Checagem de Promoção
        if piece and not piece.is_king:
            if (piece.player == Player.WHITE and to_pos[0] == 0) or \
               (piece.player == Player.BLACK and to_pos[0] == temp_board.ROWS - 1):
                
                promoted_piece = temp_board.get_piece(to_pos[0], to_pos[1])
                if promoted_piece:
                    promoted_piece.make_king()
                    
        return temp_board

    @torch.no_grad() # 
    def get_move(self, board: Board, legal_moves: list[Move]) -> Optional[Move]:
        if not legal_moves:
            return None

        best_score = -float('inf')
        best_move = None
        
        for move in legal_moves:
            future_board = self._simulate_move_on_board(board, move)
            
            opponent = Player.BLACK if self.player == Player.WHITE else Player.WHITE
            board_tensor = board_to_tensor(future_board, opponent)
            score = self.model(board_tensor).item()

            current_move_score = -score
            
            if current_move_score > best_score:
                best_score = current_move_score
                best_move = move
        

        if best_move is None:
            best_move = legal_moves[0]
            
        print(f"[NN Player] Escolheu movimento com score: {best_score:.4f}")
        return best_move