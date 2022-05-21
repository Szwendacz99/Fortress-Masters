import pygame


class UnitSelectionButton():
    def __init__(self, x, y, image, scale, is_visible=True):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.is_visible = is_visible

    def update(self, screen: pygame.Surface):
        if self.clicked:
            self.image.set_alpha(220)
        if self.is_visible:
            screen.blit(self.image, self.rect)

    def cursor_hovers(self, mouse_position: tuple):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top,
                                                                                                      self.rect.bottom):
            return True
        return False

    def set_clicked(self, clicked):
        self.clicked = clicked
