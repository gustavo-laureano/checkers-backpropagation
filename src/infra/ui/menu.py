
import pygame
from .config import WIDTH, HEIGHT, COLOR_SQUARE_DARK, COLOR_SQUARE_LIGHT, COLOR_WHITE

class GameMenu:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Menu de Jogo - Damas UEMG")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('Arial', 50, bold=True)
        self.font_button = pygame.font.SysFont('Arial', 30)
        

        self.buttons = {
            'HUMAN_VS_HUMAN': pygame.Rect(WIDTH//4, HEIGHT//2 - 60, WIDTH//2, 50),
            'HUMAN_VS_AI': pygame.Rect(WIDTH//4, HEIGHT//2, WIDTH//2, 50),
            'AI_VS_AI': pygame.Rect(WIDTH//4, HEIGHT//2 + 60, WIDTH//2, 50)
        }

    def _draw_menu(self):

        self.screen.fill(COLOR_SQUARE_DARK)

        title_text = self.font_title.render("Jogo de Damas - IA", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        for mode, rect in self.buttons.items():

            text_str = mode.replace('_', ' ')
            text = self.font_button.render(text_str, True, COLOR_WHITE)
            text_rect = text.get_rect(center=rect.center)
            

            pygame.draw.rect(self.screen, COLOR_SQUARE_LIGHT, rect)
            self.screen.blit(text, text_rect)

    def run(self) -> str:

        running = True
        while running:
            self.clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for mode, rect in self.buttons.items():
                        if rect.collidepoint(pos):
                            print(f"Modo selecionado: {mode}")
                            return mode 
            
            self._draw_menu()
            pygame.display.flip()