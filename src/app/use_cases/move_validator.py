from src.core.board import Board
from src.core.piece import Piece, Player
from typing import TypedDict, Optional, Literal

class Move(TypedDict):
    """
    Define um movimento completo.
    'from_pos': Posição inicial da peça que se move.
    'to_pos': Posição final da peça após todos os saltos.
    'captures': Lista de posições (row, col) de todas as peças capturadas
               NESTA CADEIA de movimento.
    """
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]
    captures: list[tuple[int, int]]


class MoveValidator:

    def get_all_legal_moves_for_player(self, board: Board, player: Player) -> list[Move]:

        all_capture_chains = []
        all_simple_moves = []
        
        for r in range(board.ROWS):
            for c in range(board.COLS):
                piece = board.get_piece(r, c)
                
                if piece and piece.player == player:
                    chains = self._find_chains_for_piece(board, piece, r, c)
                    all_capture_chains.extend(chains)
                    
                    if not chains:
                        simples = self._get_simple_moves(board, piece, r, c)
                        all_simple_moves.extend(simples)

        if all_capture_chains:
            max_captures = max(len(chain["captures"]) for chain in all_capture_chains)
            final_moves = [chain for chain in all_capture_chains if len(chain["captures"]) == max_captures]
            return final_moves
        
        return all_simple_moves

    def _get_simple_moves(self, board: Board, piece: Piece, row: int, col: int) -> list[Move]:
        moves = []

        if piece.is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                for i in range(1, board.ROWS):
                    new_row, new_col = row + dr * i, col + dc * i

                    if not board.is_within_bounds(new_row, new_col):
                        break
                    
                    if board.get_piece(new_row, new_col) is None:
                        moves.append({
                            "from_pos": (row, col),
                            "to_pos": (new_row, new_col),
                            "captures": []
                        })
                    else:
                        break
        else:
            move_dir = -1 if piece.player == Player.WHITE else 1
            directions = [(move_dir, -1), (move_dir, 1)]

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if board.is_within_bounds(new_row, new_col) and board.get_piece(new_row, new_col) is None:
                    moves.append({
                        "from_pos": (row, col),
                        "to_pos": (new_row, new_col),
                        "captures": []
                    })
        return moves

    def _find_chains_for_piece(self, board: Board, piece: Piece, start_row: int, start_col: int) -> list[Move]:

        all_chains = []
        
        stack: list[tuple[int, int, list[tuple[int, int]]]] = [(start_row, start_col, [])]
        
        while stack:
            curr_row, curr_col, captures_so_far = stack.pop()
            
            potential_jumps = self._find_single_jumps(board, piece, curr_row, curr_col, captures_so_far)
            
            if not potential_jumps:
                if captures_so_far:
                    all_chains.append({
                        "from_pos": (start_row, start_col),
                        "to_pos": (curr_row, curr_col),
                        "captures": captures_so_far
                    })
            else:
                for jump in potential_jumps:
                    new_pos = jump["to_pos"]
                    captured_pos = jump["captures"][0]
                    
                    new_capture_list = captures_so_far + [captured_pos]
                    
                    stack.append((new_pos[0], new_pos[1], new_capture_list))
        
        return all_chains

    def _find_single_jumps(self, board: Board, piece: Piece, row: int, col: int, 
                           already_captured: list[tuple[int, int]]) -> list[Move]:
        jumps = []

        if piece.is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                opponent_to_capture = None
                
                for i in range(1, board.ROWS):
                    scan_row, scan_col = row + dr * i, col + dc * i
                    if not board.is_within_bounds(scan_row, scan_col):
                        break
                    
                    scanned_piece = board.get_piece(scan_row, scan_col)
                    
                    if opponent_to_capture is None:
                        if scanned_piece:
                            if scanned_piece.player == piece.player:
                                break
                            else:
                                if (scan_row, scan_col) not in already_captured:
                                    opponent_to_capture = (scan_row, scan_col)
                    else:
                        if scanned_piece:
                            break
                        else:
                            jumps.append({
                                "from_pos": (row, col),
                                "to_pos": (scan_row, scan_col),
                                "captures": [opponent_to_capture]
                            })
        else:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                mid_row, mid_col = row + dr, col + dc
                dest_row, dest_col = row + 2 * dr, col + 2 * dc
                
                if not board.is_within_bounds(dest_row, dest_col):
                    continue
                    
                opponent_piece = board.get_piece(mid_row, mid_col)
                
                if opponent_piece and opponent_piece.player != piece.player and \
                   board.get_piece(dest_row, dest_col) is None:
                    
                    if (mid_row, mid_col) not in already_captured:
                        jumps.append({
                            "from_pos": (row, col),
                            "to_pos": (dest_row, dest_col),
                            "captures": [(mid_row, mid_col)]
                        })
        return jumps