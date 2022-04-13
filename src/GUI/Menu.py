import pygame
from pygame.rect import Rect

import src.Game as libGame


class Menu:
    def __init__(self, game):

        self.title_font_size: int = int(game.get_window_width()/20)
        self.text_font_size: int = int(game.get_window_width()/30)

        self.game: libGame.Game = game
        self.mid_w, self.mid_h = self.game.get_window_width() / 2, self.game.get_window_height() / 2
        self.run_display: bool = True
        self.cursor_rect: Rect = pygame.Rect(0, 0, 20, 20)
        self.offset: int = -300

    def draw_cursor(self):
        self.game.draw_text('*', 25, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.get_window().blit(self.game.get_display(), (0, 0))
        pygame.display.update()
        self.game.reset_keys()
