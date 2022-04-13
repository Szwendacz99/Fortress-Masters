import pygame
from pygame.locals import *


class Game:

    def __init__(self):
        pygame.init()

        flags = DOUBLEBUF
        self.display_surface = display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption('Fortress Masters')

        self.clock = pygame.time.Clock()

        # TODO: create resource manager class
        self.image1: pygame.image = pygame.image.load(r'../resources/img/background.png')
        self.image2: pygame.image = pygame.image.load(r'../resources/img/obj.png')
        self.angle1 = 1
        self.angle2 = 1

    def loop(self):
        while True:
            self.clock.tick(60)
            self.handleEvents()

            # Draws the surface object to the screen.
            white: tuple = (255, 255, 255)
            self.display_surface.fill(white)
            self.display_surface.blit(pygame.transform.rotate(self.image1, self.angle1), (0, 0))
            self.display_surface.blit(pygame.transform.rotate(self.image2, self.angle2), (0, 0))
            self.angle1 = (self.angle1 + 1) % 360
            self.angle2 = (self.angle2 + 2) % 360

            pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.quit()

    def quit(self):
        pygame.quit()
        quit()