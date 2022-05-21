import pygame
import pygame.mouse
import os
import math

from pygame.rect import Rect
from pygame.surface import Surface
from game.building import Building
from pygame.math import Vector2


class Unit:
    __x0: int = 0
    __bg_width: int = 564
    __rect: Rect = None
    __vector: pygame.Vector2 = pygame.Vector2(0, 0)
    __target = None
    __target_in_atk_range: bool = False
    __seeing_range: int = 50

    def __init__(self, game, start_pos, speed: int = 2, atk_range: int = 20, team: int = 0, left: bool = True):
        self.__angle: int = 0
        self.__speed: int = speed
        self.__atk_range: int = atk_range
        self.__team: int = team
        self.__left: bool = left
        self.__img_size: int = 50
        self.__pos: pygame.math.Vector2 = pygame.math.Vector2(start_pos)
        self.__game = game

        self.__img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/spaceship.png')), (self.__img_size, self.__img_size))

        self.__rect: Rect = pygame.Rect(self.get_x(), self.get_y(), self.__img_size, self.h(self.__img_size, game))

    def find_target(self, buildings: list[Building], units: list, player_team):
        current_closest_target_dist = 9999999
        current_closest_target = None
        current_target_in_atk_range: bool = False
        current_vector: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        if self.__target is not None and self.__target_in_atk_range:
            # TODO attack enemy
            # self.attack(self.__target)
            pass
        else:
            for building in buildings:
                if building.get_team() != player_team:
                    dist_to_building = self.rect_dist(building.get_rect())
                    if dist_to_building <= current_closest_target_dist:
                        current_closest_target = building
                        current_closest_target_dist = dist_to_building
                        print(current_closest_target_dist)
                        if dist_to_building < self.__atk_range:
                            current_target_in_atk_range = True

            for unit in units:
                if unit.get_team() != player_team:
                    dist_to_unit = self.unit_dist(unit)
                    if dist_to_unit <= current_closest_target_dist and dist_to_unit <= self.__seeing_range:
                        current_closest_target = unit
                        current_closest_target_dist = dist_to_unit
                        if dist_to_unit < self.__atk_range:
                            current_target_in_atk_range = True

            self.__target = current_closest_target
            self.__target_in_atk_range = current_target_in_atk_range
            self.calc_vector(current_closest_target)

    def move(self):
        if not self.__target_in_atk_range:
            self.__pos += self.__vector
            self.__rect.x += self.get_x()
            self.__rect.y += self.get_y()

    def draw(self):
        self.__game.get_display().blit(self.__img,
                                       (self.get_x() - self.__img.get_width() // 2,
                                        self.get_y() - self.__img.get_height() // 2))

    def action(self, buildings, units, player_team):
        self.find_target(buildings, units, player_team)
        self.move()
        self.draw()

    def calc_vector(self, target):
        print(target.__class__.__name__)
        self.__vector = pygame.math.Vector2(target.get_x() - self.get_x(), target.get_y() - self.get_y())
        pygame.math.Vector2.scale_to_length(self.__vector, self.__speed)
        print(self.__vector)

    def unit_dist(self, unit):
        return math.hypot(self.get_x() - unit.get_x(), self.get_y() - unit.get_y())

    def rect_dist(self, rect):
        x1, y1 = self.__rect.topleft
        x1b, y1b = self.__rect.bottomright
        x2, y2 = rect.topleft
        x2b, y2b = rect.bottomright
        left = x2b < x1
        right = x1b < x2
        top = y2b < y1
        bottom = y1b < y2
        if bottom and left:
            return math.hypot(x2b - x1, y2 - y1b)
        elif left and top:
            return math.hypot(x2b - x1, y2b - y1)
        elif top and right:
            return math.hypot(x2 - x1b, y2b - y1)
        elif right and bottom:
            return math.hypot(x2 - x1b, y2 - y1b)
        elif left:
            return x1 - x2b
        elif right:
            return x2 - x1b
        elif top:
            return y1 - y2b
        elif bottom:
            return y2 - y1b
        else:
            return 0.

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h: int, game):
        return int(h / 992 * game.get_window_height())

    def get_x(self):
        return self.__pos.x

    def get_y(self):
        return self.__pos.y

    def get_team(self):
        return self.__team
