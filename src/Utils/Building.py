import pygame
import pygame.mouse
import os
import math

from pygame.rect import Rect
from pygame.surface import Surface


def img_load(path, size, angle = 0):
    if angle:
        return pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load(os.path.normpath(path)), (size, size)), angle)
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size, size)).convert()


class Building:
    __x0: int = 0
    __bg_width: int = 564
    __rect: Rect = None
    __x: int = None
    __y: int = None

    def __init__(self, big: bool = False, team: int = 0, left: bool = True):

        self.__team: int = team
        self.__left: bool = left
        self.__big: bool = big

        self.__atk_range: int = 60
        self.__atk_speed: float = 0
        self.__angle: float = 0
        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)

        self.__target = None

        if big:
            self.__building_size = 110
        else:
            self.__building_size = 90

        self.__blue_img: Surface = img_load('resources/img/blue_turret.png', self.__building_size, -45)
        self.__red_img: Surface = img_load('resources/img/red_turret.png', self.__building_size, 135)

    def find_target(self, units):
        current_closest_target_dist = 9999999
        current_closest_target = None
        if self.__target is not None:
            # TODO calc distance, if dist<atk_range then TODO attack unit
            # self.attack(self.__target)
            pass
        else:
            for unit in units:
                if unit.get_team() != self.__team:
                    dist_to_unit = self.calc_dist(unit) - self.get_size()/2
                    if dist_to_unit <= current_closest_target_dist and dist_to_unit <= self.__atk_range:
                        current_closest_target = unit
                        current_closest_target_dist = dist_to_unit
                        if dist_to_unit < self.__atk_range:
                            # TODO attacking or shit knows
                            pass
            if current_closest_target is not None:
                self.__target = current_closest_target
                self.calc_vector(current_closest_target)

    def draw(self, game, player_team: int = 0):
        if self.__rect is None:
            self.__rect = pygame.Rect(self.__x, self.__y, self.__building_size, self.h(self.__building_size, game))
        # Displaying blue turret
        if self.__team == player_team:
            temp = pygame.transform.rotate(self.__blue_img, self.__angle)
            game.get_display().blit(temp, (self.__x-temp.get_width()//2, self.__y-temp.get_height()//2))
        # Displaying red turret
        else:
            temp = pygame.transform.rotate(self.__red_img, 180+self.__angle)
            game.get_display().blit(temp, (self.__x-temp.get_width()//2, self.__y-temp.get_height()//2))

    def action(self, game, units, player_team: int = 0):
        self.find_target(units)
        self.draw(game, player_team)

    def calc_dist(self, unit):
        return math.hypot(self.get_x() - unit.get_x(), self.get_y() - unit.get_y())

    def calc_vector(self, target):
        self.__vector = pygame.math.Vector2(target.get_x() - self.get_x(), target.get_y() - self.get_y())
        pygame.math.Vector2.scale_to_length(self.__vector, 1)
        # get angle between vector of going straight up and our vector
        self.__angle = self.__vector.angle_to(pygame.math.Vector2(0, -1))

    def set_coordinates(self, game, player_team: int = 0, x0: int = 0):
        if x0:
            self.__x0 = x0
        big_x = 200
        small_x = 117
        # Establishing blue turret's coordinates
        if self.__team == player_team:
            if self.__big:
                self.__y = self.h(918, game)
                if self.__left:
                    self.__x = self.__x0 + big_x
                else:
                    self.__x = self.__x0 + self.__bg_width - 200
            else:
                self.__y = self.h(800, game)
                if self.__left:
                    self.__x = self.__x0 + small_x
                else:
                    self.__x = self.__x0 + self.__bg_width - small_x
        # Establishing red turret's coordinates
        else:
            if self.__big:
                self.__y = self.h(74, game)
                if self.__left:
                    self.__x = self.__x0 + big_x
                else:
                    self.__x = self.__x0 + self.__bg_width - 200
            else:
                self.__y = self.h(192, game)
                if self.__left:
                    self.__x = self.__x0 + small_x
                else:
                    self.__x = self.__x0 + self.__bg_width - small_x

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h: int, game):
        return int(h / 992 * game.get_window_height())

    def get_rect(self):
        return self.__rect

    def get_team(self):
        return self.__team

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_size(self):
        return self.__building_size

    def get_target(self):
        return self.__target

    def set_target(self, target):
        self.__target = target