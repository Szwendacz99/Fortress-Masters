import pygame

import gui.widgets.widget as libWidget


class Button(libWidget.Widget):
    def __init__(self, pos, font, color, label_text, hovering_color, is_visible=True):
        super().__init__(pos=pos, font=font, color=color)
        self.label_text: str = label_text
        self.hovering_color: str = hovering_color
        self.is_visible = is_visible

        self.text: pygame.Surface = self.font.render(self.label_text, True, self.color)
        self.rect: pygame.Rect = self.text.get_rect(center=(self.pos[0], self.pos[1]))

    def update(self, screen: pygame.Surface, mouse_position: tuple):
        if self.is_visible:
            if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top,
                                                                                                          self.rect.bottom):
                self.text = self.font.render(self.label_text, True, self.hovering_color)
            else:
                self.text = self.font.render(self.label_text, True, self.color)


            screen.blit(self.text, self.rect)

    def cursor_hovers(self, mouse_position: tuple):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top,
                                                                                                      self.rect.bottom):
            return True
        return False

    def set_visible(self, is_visible):
        self.is_visible = is_visible
