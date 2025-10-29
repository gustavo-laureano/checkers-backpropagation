import pygame
from src.app.use_cases.game_manager import GameManager
from src.core.piece import Piece, Player
from src.app.use_cases.move_validator import Move
from .config import * 
from typing import Optional
from src.infra.ai.random_player import RandomPlayer

class PygameView:
    
    def __init__(self, game: GameManager, game_mode: str):
        self.game = game
        self.game_mode = game_mode 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Damas com IA - Projeto UEMG")
        self.clock = pygame.time.Clock()
        
        # --- Configuração dos Agentes ---
        # Se o agente for 'None', significa que é um Humano.
        # Se for um objeto (ex: RandomPlayer), é uma IA.
        self.ai_agent_white = None
        self.ai_agent_black = None

        if self.game_mode == 'HUMAN_VS_AI':
            # Humano (Brancas) vs IA (Pretas)
            # (Futuramente, o menu pode perguntar qual modelo de IA)
            self.ai_agent_black = RandomPlayer(Player.BLACK)
        
        elif self.game_mode == 'AI_VS_AI':
            # IA (Brancas) vs IA (Pretas)
            # (Aqui você pode testar IAs diferentes)
            self.ai_agent_white = RandomPlayer(Player.WHITE)
            self.ai_agent_black = RandomPlayer(Player.BLACK)
        
        elif self.game_mode == 'HUMAN_VS_HUMAN':
            # Humano vs Humano: Ambos agentes são None
            pass
        
        # Estado da UI:
        self.selected_piece_pos: Optional[tuple[int, int]] = None
        self.highlighted_moves: list[tuple[int, int]] = []

    def run(self):
        running = True
        running = True
        
        while running:
            self.clock.tick(60)
            
            current_player = self.game.get_current_player()
            current_agent = None
            
            if current_player == Player.WHITE:
                current_agent = self.ai_agent_white
            else:
                current_agent = self.ai_agent_black
            
            is_human_turn = (current_agent is None)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and is_human_turn:
                    pos = pygame.mouse.get_pos()
                    row, col = self._get_row_col_from_mouse(pos)
                    self._handle_click(row, col)


            if not is_human_turn and not self.game.get_winner():
                pygame.time.wait(500) 
                
                move = current_agent.get_move(
                    self.game.get_board(),
                    self.game.get_legal_moves()
                )
                
                if move:
                    self.game.make_move(move) 
            
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
                        self.screen.blit(CROWN_IMG, (center_x - CROWN_IMG.get_width() // 2, center_y - CROWN_IMG.get_height() // 2))

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