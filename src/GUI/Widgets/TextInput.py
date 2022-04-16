import pygame


class TextInput:
	def __init__(self, background_color, pos, font, font_color):
		self.pos: tuple = pos
		self.clicked: bool = False
		self.background_color: str = background_color
		self.font: pygame.font.Font = font
		self.font_color: str = font_color
		self.input_text: str = None
		self.text: pygame.Surface = self.font.render(self.label_text, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect: pygame.Rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
		self.text_rect: pygame.Rect = self.text.get_rect(center=(self.pos[0], self.pos[1]))

	def update(self, screen):
		screen.blit(self.text, self.text_rect)

	def cursor_hovers(self, position) -> bool:
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False