from src.core.piece import Piece, Player
from typing import Optional

ROWS, COLS = 8, 8

class Board:
   
    
    def __init__(self):
        self.grid: list[list[Optional[Piece]]] = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        if self.is_within_bounds(row, col):
            return self.grid[row][col]
        return None

    def add_piece(self, piece: Piece, row: int, col: int):
        if self.is_within_bounds(row, col):
            self.grid[row][col] = piece

    def remove_piece(self, row: int, col: int):
        if self.is_within_bounds(row, col):
            self.grid[row][col] = None

    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int):
        
        piece = self.get_piece(from_row, from_col)
        if piece:
            self.remove_piece(from_row, from_col)
            self.add_piece(piece, to_row, to_col)

    def is_within_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < ROWS and 0 <= col < COLS

    def setup_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                if (r + c) % 2 == 1:
                    if r < 3:
                        self.add_piece(Piece(Player.BLACK), r, c)
                    elif r > 4: 
                        self.add_piece(Piece(Player.WHITE), r, c)
                        
    def __repr__(self) -> str:
        board_str = "   " + "  ".join(str(i) for i in range(COLS)) + "\n" # Headers de coluna
        board_str += "  +" + "---" * COLS + "+\n"
        for r in range(ROWS):
            board_str += f"{r} |" 
            for c in range(COLS):
                piece = self.grid[r][c]
                if piece:
                    
                    board_str += f"{str(piece):^3}"
                else:
                    board_str += " . " 
            board_str += "|\n"
        board_str += "  +" + "---" * COLS + "+\n"
        return board_str