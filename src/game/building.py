import pygame
import pygame.mouse
import os

from pygame.rect import Rect
from pygame.surface import Surface


class Building:
    __x0: int = 0
    __bg_width: int = 564
    __rect: Rect = None
    __x: int = None
    __y: int = None

    def __init__(self, big: bool = False, team: int = 0, left: bool = True):
        self.__angle: int = 0
        self.__team: int = team
        self.__left: bool = left
        self.__big: bool = big
        if big:
            self.__building_size = 110
        else:
            self.__building_size = 90

        self.__blue_img: Surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/blue_turret.png')), (self.__building_size, self.__building_size)), -45)
        self.__red_img: Surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/red_turret.png')), (self.__building_size, self.__building_size)), 135)

    def draw(self, game, player_team: int = 0):
        self.__angle += 1

        if self.__rect is None:
            self.__rect = pygame.Rect(self.__x, self.__y, self.__building_size, self.h(self.__building_size, game))
        # Displaying blue turret
        if self.__team == player_team:
            temp = pygame.transform.rotate(self.__blue_img, self.__angle)
            game.get_display().blit(temp, (self.__x-temp.get_width()//2, self.__y-temp.get_height()//2))
        # Displaying red turret
        else:
            temp = pygame.transform.rotate(self.__red_img, self.__angle)
            game.get_display().blit(temp, (self.__x-temp.get_width()//2, self.__y-temp.get_height()//2))

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
