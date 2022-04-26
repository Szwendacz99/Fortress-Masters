import logging

from src.Game import Game

logging.basicConfig(format='%(levelname)s :: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    game: Game = Game()
    game.curr_menu.display_menu()
