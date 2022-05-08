import pygame

import GUI.Widgets.Widget as libWidget


class TextInput(libWidget.Widget):
    def __init__(self, pos, font, color, background_color, clicked_color, input_text, input_label, input_label_color):
        super().__init__(pos=pos, font=font, color=color)
        self.clicked: bool = False
        self.background_color: tuple = background_color
        self.clicked_color: str = clicked_color
        self.input_text: str = input_text
        self.input_label: str = input_label
        self.input_label_color: str = input_label_color

        self.font_width: int = self.font.size(self.input_text)[0]
        self.font_height: int = self.font.size(self.input_text)[1]

        self.text: pygame.Surface = self.font.render(self.input_text, True, self.color)
        self.label: pygame.Surface = self.font.render(self.input_label, True, self.color)

        self.input_rect: pygame.Rect = self.text.get_rect(midleft=(self.pos[0], self.pos[1]))
        self.label_rect: pygame.Rect = self.label.get_rect(center=(self.pos[0] - self.font_width - 20, self.pos[1]))

    def update(self, screen: pygame.Surface, mouse_position: tuple):
        self.font_width, self.font_height = self.font.size(self.input_text)
        self.font_width = self.font_width + 20
        self.font_height = self.font_height + 20
        if self.clicked:
            pygame.draw.rect(screen, self.clicked_color, (self.pos[0], self.pos[1] - self.font_height/2, self.font_width, self.font_height))
        else:
            pygame.draw.rect(screen, self.background_color, (self.pos[0], self.pos[1] - self.font_height/2, self.font_width, self.font_height))

        self.label = self.font.render(self.input_label, True, self.input_label_color)
        self.text = self.font.render(self.input_text, True, self.color)
        screen.blit(self.label, self.label_rect)
        screen.blit(self.text, self.input_rect)

    def cursor_hovers(self, mouse_position) -> bool:
        self.text: pygame.Surface = self.font.render(self.input_text, True, self.color)
        self.input_rect: pygame.Rect = self.text.get_rect(midleft=(self.pos[0], self.pos[1]))

        if mouse_position[0] in range(self.input_rect.left, self.input_rect.right) and mouse_position[1] in range(self.input_rect.top,                                                                                                      self.input_rect.bottom):
            return True
        return False

    def set_clicked(self, clicked):
        self.clicked = clicked

    def is_clicked(self):
        return self.clicked

    def delete_last_input_letter(self):
        self.input_text = self.input_text[:-1]
        if self.input_text == "":
            self.input_text = " "

    def append_input(self, letter: str):
        self.input_text += letter

    def get_input_text(self):
        if self.input_text[0] == " ":
            return self.input_text[1:]
        return self.input_text
