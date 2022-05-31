import pygame

from game.units.unit_type import UnitType


class UnitSelectionButton:
    default_width: int = 1536
    default_height: int = 864

    def __init__(self, x, y, image, scale, font, unit_type, price=10, is_visible=True, clicked=False):
        self.width: int = image.get_width()
        self.height: int = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.scaled_image = self.image
        self.rect: pygame.Surface = self.image.get_rect()
        self.x = x
        self.y = y
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
            self.scaled_image.set_alpha(255)
        else:
            self.scaled_image.set_alpha(125)
        if self.is_visible:
            self.text = self.font.render(str(self.price), True, "Black")
            screen.blit(self.scaled_image, self.rect)
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

    def resize(self, screen):
        self.scaled_image = pygame.transform.scale(self.image,
                                                   (self.w(self.width, screen),
                                                    self.h(self.height, screen)))
        self.rect = self.scaled_image.get_rect()
        x_scaled = self.w(self.x, screen)
        y_scaled = self.h(self.y, screen)
        self.rect.topleft = (x_scaled, y_scaled)

    def h(self, h: int, screen):
        return int(h / self.default_height * screen.get_height())

    def w(self, w: int, screen):
        return int(w / self.default_width * screen.get_width())

