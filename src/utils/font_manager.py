import pygame

import utils.singleton as libSingleton


class FontManager(metaclass=libSingleton.SingletonMeta):
    def __init__(self, font_path: str):
        self.font_path = font_path
        self.title_font_size = int(pygame.display.Info().current_h//15)
        self.regular_font_size = int(pygame.display.Info().current_h//22)

    def get_font_name(self) -> str:
        return self.font_path

    def get_title_font_size(self) -> int:
        return self.title_font_size

    def get_regular_font_size(self) -> int:
        return self.regular_font_size

    def set_title_font_size(self, new_font_size):
        self.title_font_size = new_font_size

    def set_regular_font_size(self, new_font_size):
        self.regular_font_size = new_font_size
