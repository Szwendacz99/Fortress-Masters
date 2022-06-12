import pygame
import pygame.mouse
import os

from game.team import Team
from game.bullet import Bullet


def img_load(path, size):
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size, size)).convert_alpha()


class Laser(Bullet):
    path_blue = 'resources/img/laser_blue.png'
    path_red = 'resources/img/laser_red.png'

    def __init__(self, game, start_pos, target, damage, speed: float = 2.11, team: Team = None):
        Bullet.__init__(self, game, start_pos, target, damage, self.path_blue,
                        self.path_red, speed, team, img_size_x=7, img_size_y=14)

