import pygame


class TextInput:
	def __init__(self, pos, font, font_color):
		self.pos: tuple = pos
		self.clicked: bool = False
		self.background_color: tuple = (255, 255, 255)
		self.font: pygame.font.Font = font
		self.font_color: str = font_color
		self.input_text: str = "test"
		self.text: pygame.Surface = self.font.render(self.input_text, True, self.font_color)
		self.text_rect: pygame.Rect = self.text.get_rect(center=(self.pos[0], self.pos[1]))

	def update(self, screen):
		# TODO: Draw rectangle around text, probably font size is needed
		pygame.draw.rect(screen, self.background_color, (self.pos[0] - 100, self.pos[1]- 50, 200, 100))
		self.text = self.font.render(self.input_text, True, self.font_color)
		screen.blit(self.text, self.text_rect)

	def cursor_hovers(self, position) -> bool:
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			return True
		return False

	def set_clicked(self, clicked):
		self.clicked = clicked