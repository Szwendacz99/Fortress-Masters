import pygame
import pygame.mouse
import os
import math

from pygame.rect import Rect
from pygame.surface import Surface
from game.building import Building
from pygame.math import Vector2


def img_load(path, size):
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size, size)).convert_alpha()


class Unit:

    def __init__(self, game, start_pos, speed: float = 0.3, atk_range: int = 60, team: int = 0, left: bool = True):
        self.__game = game
        self.__team: int = team
        self.__left: bool = left
        # stats of unit
        # TODO add hp, attack speed
        self.__speed: float = speed
        self.__atk_range: int = atk_range
        self.__atk_speed: float = 0
        self.__seeing_range: int = 200

        self.__img_size: int = 50
        self.__rect: Rect = None
        self.__pos: pygame.math.Vector2 = pygame.math.Vector2(start_pos)
        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = 0

        self.__target = None
        self.__target_in_atk_range: bool = False

        self.__img: Surface = img_load('resources/img/spaceship.png', self.__img_size)
        if team == 1:
            self.__img = pygame.transform.rotate(self.__img, 180)
        self.__rect: Rect = pygame.Rect(self.get_x(), self.get_y(), self.__img_size, self.h(self.__img_size, game))

    def find_target(self, buildings: list[Building], units: list['Unit']):
        if self.__target is not None and self.__target_in_atk_range:
            # TODO attack enemy
            """ for unit in units:
                if unit == self:
                    units.remove(unit)
            for building in buildings:
                if building.get_target() == self:
                    building.set_target(None)
            """
            pass

        else:
            current_closest_target_dist = 9999999
            current_closest_target = None
            current_target_in_atk_range: bool = False
            for building in buildings:
                if building.get_team() != self.__team:
                    dist_to_building = self.calc_dist(building) - building.get_size()/2
                    if dist_to_building <= current_closest_target_dist:
                        current_closest_target = building
                        current_closest_target_dist = dist_to_building
                        if dist_to_building < self.__atk_range:
                            current_target_in_atk_range = True

            for unit in units:
                if unit.get_team() != self.__team:
                    dist_to_unit = self.calc_dist(unit)
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
            self.__rect.x += self.__vector.x
            self.__rect.y += self.__vector.y

    def draw(self):
        # TODO rotate img
        temp = pygame.transform.rotate(self.__img, self.__angle)
        self.__game.get_display().blit(temp,
                                       (self.get_x() - self.__img.get_width() // 2,
                                        self.get_y() - self.__img.get_height() // 2))

    def action(self, buildings, units):
        self.find_target(buildings, units)
        self.move()
        self.draw()

    def calc_vector(self, target):
        self.__vector = pygame.math.Vector2(target.get_x() - self.get_x(), target.get_y() - self.get_y())
        if self.__vector:
            pygame.math.Vector2.scale_to_length(self.__vector, self.__speed)
        # get angle between vector of going straight up and our vector
        self.__angle = self.__vector.angle_to(pygame.math.Vector2(0, -1))

    def calc_dist(self, unit):
        return math.hypot(self.get_x() - unit.get_x(), self.get_y() - unit.get_y())

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h: int, game):
        return int(h / 992 * game.get_window_height())

    def get_x(self):
        return self.__pos.x

    def get_y(self):
        return self.__pos.y

    def get_team(self):
        return self.__team
