import pygame
from src.app.use_cases.game_manager import GameManager
from src.infra.ui.pygame_view import PygameView
from src.infra.ui.menu import GameMenu # <-- NOVA IMPORTAÇÃO

def main():

    pygame.init()
    
    menu = GameMenu()
    
    game_mode = menu.run()   

    game = GameManager()
    
    view = PygameView(game, game_mode) 
    
    view.run()

if __name__ == "__main__":
    main()