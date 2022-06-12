import logging

from gui.game_window import GameWindow

logging.basicConfig(format='%(levelname)s :: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    game: GameWindow = GameWindow()
    game.curr_menu.display_menu()
