import pygame


class Button:
	def __init__(self, image, pos, label_text, font, base_color, hovering_color):
		self.image: pygame.Surface = image
		self.pos: tuple = pos
		self.font: pygame.font.Font = font
		self.base_color: str = base_color
		self.hovering_color: str = hovering_color
		self.label_text: str = label_text
		self.text: pygame.Surface = self.font.render(self.label_text, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect: pygame.Rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
		self.text_rect: pygame.Rect = self.text.get_rect(center=(self.pos[0], self.pos[1]))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.label_text, True, self.hovering_color)
		else:
			self.text = self.font.render(self.label_text, True, self.base_color)