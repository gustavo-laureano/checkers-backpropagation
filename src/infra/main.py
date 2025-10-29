import pygame
from src.app.use_cases.game_manager import GameManager
from src.infra.ui.pygame_view import PygameView

def main():
    pygame.init()   

    game = GameManager()
    view = PygameView(game)
    

    view.run()

if __name__ == "__main__":
    main()