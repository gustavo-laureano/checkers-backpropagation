import pygame
import os

ROWS, COLS = 8, 8
SQUARE_SIZE = 75  # Tamanho de cada casa (em pixels)
WIDTH, HEIGHT = COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE

# --- Cores (RGB) ---
COLOR_WHITE = (255, 255, 255)  # Peças
COLOR_BLACK = (0, 0, 0)        # Peças
COLOR_SQUARE_LIGHT = (234, 233, 210)  # Casas claras
COLOR_SQUARE_DARK = (75, 115, 153)    # Casas escuras

COLOR_HIGHLIGHT = (100, 200, 100, 150)  # movimentos
COLOR_SELECTED = (255, 0, 0)            # borda da peça selecionada


CROWN_IMG = pygame.transform.scale(pygame.image.load("assets/crown.png"), (44, 25))