import pygame

from game.unit_type import UnitType


class UnitSelectionButton:
    def __init__(self, x, y, image, scale, font, unit_type, price=10, is_visible=True, clicked=False):
        width: int = image.get_width()
        height: int = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect: pygame.Surface = self.image.get_rect()
        self.rect.topleft: tuple = (x, y)
        self.font: pygame.font.Font = font
        self.price: int = price
        self.unit_type: UnitType = unit_type

        self.text: pygame.Surface = self.font.render(str(self.price), True, "Black")
        self.text_rect: pygame.Rect = self.text.get_rect(topleft=self.rect.topleft)

        self.clicked = clicked
        self.is_visible = is_visible

    def update(self, screen: pygame.Surface):
        if self.clicked:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(125)
        if self.is_visible:
            self.text = self.font.render(str(self.price), True, "Black")
            screen.blit(self.image, self.rect)
            screen.blit(self.text, self.rect)

    def cursor_hovers(self, mouse_position: tuple) -> bool:
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top,
                                                                                                      self.rect.bottom):
            return True
        return False

    def set_clicked(self, clicked):
        self.clicked = clicked

    def is_clicked(self) -> bool:
        return self.clicked

    def get_unit_type(self) -> UnitType:
        return self.unit_type
