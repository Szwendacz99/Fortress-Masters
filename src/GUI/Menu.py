import pygame

import src.Game as libGame


class Menu:
    def __init__(self, game):

        self.title_font_size: int = int(game.get_window_width()/20)
        self.text_font_size: int = int(game.get_window_width()/30)

        self.mouse_pos: tuple = None

        self.game: libGame.Game = game
        self.mid_w, self.mid_h = self.game.get_window_width() / 2, self.game.get_window_height() / 2
        self.run_display: bool = True

    def blit_screen(self):
        self.game.get_display().blit(self.game.get_display(), (0, 0))
        pygame.display.update()

    def display_menu(self):
        pass
