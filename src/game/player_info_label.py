import pygame


class PlayerInfoLabel:
    default_width: int = 1536
    default_height: int = 864

    def __init__(self, x, y, font, text, image=None):
        self.x: int = x
        self.y: int = y
        self.font: pygame.font.Font = font
        self.label_text: str = text
        self.image = image

        self.text: pygame.Surface = self.font.render(str(self.label_text), True, "White")
        self.rect: pygame.Rect = self.text.get_rect(topleft=(x, y))

    def update(self, screen: pygame.Surface, currency_amount = None, big_hp = None, little_hp = None, username=None):
        if username is not None:
            self.text = self.font.render(f"{username}", True, "White")
        elif currency_amount is not None:
            self.text = self.font.render(f"{self.label_text} {currency_amount}", True, "White")
        elif big_hp is not None:
            self.text = self.font.render(f"{self.label_text} {big_hp}", True, "White")
        elif little_hp is not None:
            self.text = self.font.render(f"{self.label_text} {little_hp}", True, "White")
        screen.blit(self.text, self.rect)
        pass

    def resize(self, screen, game):
        self.font = game.get_font(self.h(20, screen))
        self.text = self.font.render(str(self.label_text), True, "White")
        self.rect: pygame.Rect = self.text.get_rect()
        x_scaled = self.w(self.x, screen)
        y_scaled = self.h(self.y, screen)
        self.rect.topleft = (x_scaled, y_scaled)

    def h(self, h: int, screen):
        return int(h / self.default_height * screen.get_height())

    def w(self, w: int, screen):
        return int(w / self.default_width * screen.get_width())
