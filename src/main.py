import sys

import pygame
from pygame.locals import *

# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.

pygame.init()

# define the RGB value
# for white colour
white = (255, 255, 255)

# assigning values to X and Y variable
X = 700
Y = 700

# create the display surface object
# of specific dimension..e(X, Y).
flags = DOUBLEBUF
display_surface = pygame.display.set_mode((X, Y), flags, 16, vsync=1)

# set the pygame window name
pygame.display.set_caption('Image')

image1 = pygame.image.load(r'../resources/background.png')
image2 = pygame.image.load(r'../resources/obj.png')

clock = pygame.time.Clock()

angle1 = 1
angle2 = 1
# infinite loop
while True:
    clock.tick(60)
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

    # Draws the surface object to the screen.
    display_surface.fill(white)
    display_surface.blit(pygame.transform.rotate(image1, angle1), (0, 0))
    display_surface.blit(pygame.transform.rotate(image2, angle2), (0, 0))
    angle1 = (angle1+1) % 360
    angle2 = (angle2 + 2) % 360

    pygame.display.flip()
