import pygame
from src.app.use_cases.game_manager import GameManager
from src.core.piece import Piece, Player
from src.app.use_cases.move_validator import Move
from .config import * # Importa todas as nossas constantes
from typing import Optional

class PygameView:

    
    def __init__(self, game: GameManager):
        self.game = game
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Damas com IA - Projeto UEMG")
        self.clock = pygame.time.Clock()
        
        # Estado da UI:
        self.selected_piece_pos: Optional[tuple[int, int]] = None
        self.highlighted_moves: list[tuple[int, int]] = []

    def run(self):
        running = True
        
        while running:
            self.clock.tick(60) 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self._get_row_col_from_mouse(pos)
                    self._handle_click(row, col)

            self._update_display()
            
            winner = self.game.get_winner()
            if winner:
                self._draw_winner(winner)
                pygame.display.flip()
                pygame.time.wait(5000) 
                running = False 

        pygame.quit()

    def _get_row_col_from_mouse(self, pos: tuple[int, int]) -> tuple[int, int]:
        
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def _handle_click(self, row: int, col: int):
       
        
        if (row, col) in self.highlighted_moves:
            move_obj = self._find_move(self.selected_piece_pos, (row, col))
            if move_obj:
                self.game.make_move(move_obj) 
            self._reset_selection()
            return

        self._reset_selection()
        
        piece = self.game.get_board().get_piece(row, col)
        if piece and piece.player == self.game.get_current_player():
            # Pede ao game os movimentos *para esta peça*
            moves_for_piece = [m for m in self.game.get_legal_moves() 
                               if m['from_pos'] == (row, col)]
            
            if moves_for_piece:
                self.selected_piece_pos = (row, col)
                self.highlighted_moves = [m['to_pos'] for m in moves_for_piece]

    def _find_move(self, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> Optional[Move]:
        for move in self.game.get_legal_moves():
            if move['from_pos'] == from_pos and move['to_pos'] == to_pos:
                return move
        return None

    def _reset_selection(self):
        self.selected_piece_pos = None
        self.highlighted_moves = []

    def _update_display(self):
        self._draw_board()
        self._draw_highlights()
        self._draw_pieces()
        pygame.display.flip() 

    def _draw_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = COLOR_SQUARE_LIGHT if (r + c) % 2 == 0 else COLOR_SQUARE_DARK
                pygame.draw.rect(self.screen, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def _draw_pieces(self):
        board = self.game.get_board()
        for r in range(ROWS):
            for c in range(COLS):
                piece = board.get_piece(r, c)
                if piece:
                    center_x = c * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = r * SQUARE_SIZE + SQUARE_SIZE // 2
                    radius = SQUARE_SIZE // 2 - 10 # Raio da peça
                    
                    color = COLOR_WHITE if piece.player == Player.WHITE else COLOR_BLACK
                    pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

                    if piece.is_king:
                        font = pygame.font.SysFont('Arial', 20, bold=True)
                        text_color = COLOR_BLACK if piece.player == Player.WHITE else COLOR_WHITE
                        text = font.render('K', True, text_color)
                        self.screen.blit(text, (center_x - text.get_width() // 2, center_y - text.get_height() // 2))

    def _draw_highlights(self):
        if self.selected_piece_pos:
            r, c = self.selected_piece_pos
            pygame.draw.rect(self.screen, COLOR_SELECTED, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5) # Borda de 5px

        for r, c in self.highlighted_moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(COLOR_HIGHLIGHT)
            self.screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            
    def _draw_winner(self, winner: Player):
        font = pygame.font.SysFont('Courier New', 50, bold=True)
        text = f"VENCEDOR: {winner.value}!"
        text_render = font.render(text, True, COLOR_SELECTED)
        
        text_rect = text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180)) 
        self.screen.blit(s, (0, 0))
        
        self.screen.blit(text_render, text_rect)