import pygame

import game_window as libGame
from utils.font_manager import FontManager


class Menu:
    def __init__(self, game):

        self.font_manager: FontManager = FontManager()

        self.mouse_pos: tuple = None

        self.game: libGame.GameWindow = game
        self.mid_w: float = self.game.get_window_width() / 2
        self.mid_h: float = self.game.get_window_height() / 2
        self.run_display: bool = True

    def resize(self):
        self.font_manager.set_title_font_size(int(self.game.get_window_height()/10))
        self.font_manager.set_regular_font_size(int(self.game.get_window_height()/20))
        self.mid_w: float = self.game.get_window_width() / 2
        self.mid_h: float = self.game.get_window_height() / 2

    def blit_screen(self):
        self.game.get_display().blit(self.game.get_display(), (0, 0))
        pygame.display.update()

    def display_menu(self):
        pass
