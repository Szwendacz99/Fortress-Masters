import pygame, sys
from pygame.locals import *


class Menu:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Fortress Masters')

        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.mainClock = pygame.time.Clock()

        #pygame.display.set_mode((500, 500), 0, 32)
        self.display_surface = display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.font_size: int = 60
        self.font = pygame.font.SysFont(None, self.font_size)
        self.click = False

        self.main_menu()


    def draw_text(self, text, color, surface, x, y):
        textobj = self.font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


    def main_menu(self):
        while True:
            self.display_surface.fill((0, 0, 0))
            self.draw_text('main menu', (255, 255, 255), self.display_surface, self.screen_width/2 - self.font_size, self.screen_height/16)

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            if button_1.collidepoint((mx, my)):
                if click:
                    self.game()
            if button_2.collidepoint((mx, my)):
                if click:
                    self.options()
            pygame.draw.rect(self.display_surface, (255, 0, 0), button_1)
            pygame.draw.rect(self.display_surface, (255, 0, 0), button_2)

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.mainClock.tick(60)


    def game(self):
        running = True
        while running:
            self.display_surface.fill((0, 0, 0))

            self.draw_text('game', (255, 255, 255), self.display_surface, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            self.mainClock.tick(60)


    def options(self):
        running = True
        while running:
            self.display_surface.fill((0, 0, 0))

            self.draw_text('options', (255, 255, 255), self.display_surface, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            self.mainClock.tick(60)
