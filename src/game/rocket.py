import pygame
import pygame.mouse
import os
import math

from pygame.rect import Rect
from pygame.surface import Surface
from game.building import Building
from game.bullet import Bullet
from pygame.math import Vector2


class Rocket(Bullet):
    path_blue = 'resources/img/rocket_blue.png'
    path_red = 'resources/img/rocket_red.png'

    def __init__(self, game, start_pos, target, damage, speed: float = 1.66, team: int = 0):
        Bullet.__init__(self, game, start_pos, target, damage, self.path_blue, self.path_red, speed, team)
