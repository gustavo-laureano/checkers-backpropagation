import pygame
from src.app.use_cases.game_manager import GameManager
from src.core.piece import Player
from src.app.use_cases.move_validator import Move
from .config import *
from typing import Optional
from src.infra.ai.random_player import RandomPlayer
from src.infra.ai.neural_net_player import NeuralNetPlayer


class PygameView:
    
    def __init__(self, game: GameManager, mode_config: dict | None):
        self.game = game
        self.mode_config = mode_config or {}
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Damas com IA - Projeto UEMG")
        self.clock = pygame.time.Clock()

        self.ai_agent_white = None
        self.ai_agent_black = None

        DEFAULT_MODEL_PATH = "checkers_model_v1.pth"

        def create_agent(cfg: dict | None, player: Player):
            if not cfg:
                return None
            t = cfg.get('type', '').upper()
            if t in ('HUMAN', ''):
                return None
            if t in ('RANDOM', 'RANDOM_AI'):
                return RandomPlayer(player)
            if t in ('NN', 'NEURAL_NET_AI', 'NEURAL'):
                path = cfg.get('path', DEFAULT_MODEL_PATH)
                return NeuralNetPlayer(player, path)
            return None

        # Build agents from config dict
        self.ai_agent_white = create_agent(self.mode_config.get('white'), Player.WHITE)
        self.ai_agent_black = create_agent(self.mode_config.get('black'), Player.BLACK)

        self.selected_piece_pos: Optional[tuple[int, int]] = None
        self.highlighted_moves: list[tuple[int, int]] = []

    def run(self):
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
                move = current_agent.get_move(self.game.get_board(), self.game.get_legal_moves())
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
            moves_for_piece = [m for m in self.game.get_legal_moves() if m['from_pos'] == (row, col)]
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
                    radius = max(8, SQUARE_SIZE // 2 - 10)

                    color = COLOR_WHITE if piece.player == Player.WHITE else COLOR_BLACK
                    pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

                    if piece.is_king and (CROWN_IMG is not None):
                        crown = CROWN_IMG
                        self.screen.blit(crown, (center_x - crown.get_width() // 2, center_y - crown.get_height() // 2))

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