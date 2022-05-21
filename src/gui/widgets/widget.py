import pygame


class Widget:
    def __init__(self, pos: tuple, font: pygame.font.Font, color: str):
        self.pos: tuple = pos
        self.font: pygame.font.Font = font
        self.color: str = color

    def update(self, screen: pygame.Surface, mouse_pos: tuple):
        pass

    def cursor_hovers(self, mouse_position: tuple):
        pass
