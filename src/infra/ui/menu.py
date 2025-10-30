import pygame
import tkinter as tk
from tkinter import filedialog
from .config import WIDTH, HEIGHT, COLOR_WHITE
from typing import Optional, Dict, Any

# Dimensões do Menu
MENU_WIDTH = max(800, WIDTH)
MENU_HEIGHT = max(720, HEIGHT)


class GameMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
        pygame.display.set_caption("Menu de Jogo - Damas UEMG")
        self.clock = pygame.time.Clock()

        # Tipografias
        self.font_title = pygame.font.SysFont('Arial', 50, bold=True)
        self.font_button = pygame.font.SysFont('Arial', 30)
        self.font_subtitle = pygame.font.SysFont('Arial', 24, bold=True)

        self._setup_tkinter()

        # Botões principais (centralizados)
        bw = MENU_WIDTH // 2
        bx = MENU_WIDTH // 4
        self.main_buttons = {
            'HUMAN_VS_HUMAN': pygame.Rect(bx, MENU_HEIGHT // 2 - 70, bw, 50),
            'HUMAN_VS_AI': pygame.Rect(bx, MENU_HEIGHT // 2 - 10, bw, 50),
            'AI_VS_AI': pygame.Rect(bx, MENU_HEIGHT // 2 + 50, bw, 50)
        }

        # Cores e estilos
        self.bg_start = (61, 59, 48)
        self.bg_end = (77, 80, 80)
        self.button_color = (231, 226, 71)
        self.button_hover = (61, 59, 48)
        self.shadow_color = (0,126, 123, 16)
        self.button_radius = 12
        self.shadow_offset = (6, 6)


    def _setup_tkinter(self):
        self.tk_root = tk.Tk()
        self.tk_root.withdraw()

    def _ask_for_model_path(self) -> Optional[str]:
        self.tk_root.deiconify()
        self.tk_root.lift()
        self.tk_root.focus_force()

        file_path = filedialog.askopenfilename(
            title="Selecione o 'cérebro' da IA (.pth)",
            filetypes=[("Modelos PyTorch", "*.pth")]
        )

        self.tk_root.withdraw()
        return file_path if file_path else None

    def _lerp_color(self, c1, c2, t: float):
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t)
        )

    def _draw_gradient(self):
        for y in range(MENU_HEIGHT):
            t = y / MENU_HEIGHT
            color = self._lerp_color(self.bg_start, self.bg_end, t)
            pygame.draw.line(self.screen, color, (0, y), (MENU_WIDTH, y))

    def _draw_button(self, rect: pygame.Rect, text: str, hovered: bool):
        shadow_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        shadow_surf.fill(self.shadow_color)
        self.screen.blit(shadow_surf, (rect.x + self.shadow_offset[0], rect.y + self.shadow_offset[1]))

        color = self.button_hover if hovered else self.button_color
        pygame.draw.rect(self.screen, color, rect, border_radius=self.button_radius)

        text_render = self.font_button.render(text, True, COLOR_WHITE)
        text_rect = text_render.get_rect(center=rect.center)
        self.screen.blit(text_render, text_rect)

    def _draw_menu(self, title_text, buttons_dict):
        self._draw_gradient()

        circle_color = self._lerp_color(self.bg_end, (255, 255, 255), 0.03)
        pygame.draw.circle(self.screen, circle_color, (MENU_WIDTH // 2, MENU_HEIGHT // 6), 120)

        title = self.font_title.render(title_text, True, COLOR_WHITE)
        title_rect = title.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 6))
        self.screen.blit(self.font_title.render(title_text, True, (0, 0, 0, 80)), (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title, title_rect)

        sub = self.font_subtitle.render("Selecione o modo e configure as IAs", True, COLOR_WHITE)
        sub_rect = sub.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 6 + 50))
        self.screen.blit(sub, sub_rect)

        mouse_pos = pygame.mouse.get_pos()
        for key, rect in buttons_dict.items():
            text_str = key.replace('_', ' ')
            hovered = rect.collidepoint(mouse_pos)
            if hovered:
                hover_rect = rect.inflate(8, 6)
                hover_rect.center = rect.center
                self._draw_button(hover_rect, text_str, hovered=True)
            else:
                self._draw_button(rect, text_str, hovered=False)

        pygame.display.flip()

    def _select_agent(self, player_color: str) -> Optional[Dict[str, Any]]:
        bw = MENU_WIDTH // 2
        bx = MENU_WIDTH // 4
        sub_buttons = {
            'RANDOM_AI': pygame.Rect(bx, MENU_HEIGHT // 2 - 30, bw, 50),
            'NEURAL_NET_AI': pygame.Rect(bx, MENU_HEIGHT // 2 + 30, bw, 50)
        }
        title = f"Configurar IA: {player_color}"

        while True:
            self.clock.tick(30)
            self._draw_menu(title, sub_buttons)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for mode, rect in sub_buttons.items():
                        if rect.collidepoint(pos):
                            if mode == 'RANDOM_AI':
                                return {'type': 'RANDOM'}
                            if mode == 'NEURAL_NET_AI':
                                path = self._ask_for_model_path()
                                if path:
                                    return {'type': 'NN', 'path': path}

    def run(self) -> Optional[Dict[str, Any]]:
        while True:
            self.clock.tick(30)
            self._draw_menu("Jogo de Damas - IA", self.main_buttons)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for mode, rect in self.main_buttons.items():
                        if rect.collidepoint(pos):
                            if mode == 'HUMAN_VS_HUMAN':
                                return {'white': {'type': 'HUMAN'}, 'black': {'type': 'HUMAN'}}

                            if mode == 'HUMAN_VS_AI':
                                config_black = self._select_agent("PRETAS")
                                if config_black:
                                    return {'white': {'type': 'HUMAN'}, 'black': config_black}

                            if mode == 'AI_VS_AI':
                                config_white = self._select_agent("BRANCAS")
                                if not config_white:
                                    continue

                                config_black = self._select_agent("PRETAS")
                                if not config_black:
                                    continue

                                return {'white': config_white, 'black': config_black}