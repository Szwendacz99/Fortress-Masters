import uuid

import pygame
import pygame.mouse
import os
import math

from pygame.surface import Surface
from pygame.math import Vector2
from core.team import Team


def img_load(path, size_x, size_y):
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size_x, size_y)).convert_alpha()


class Bullet:
    default_width: int = 1536
    default_height: int = 864

    def __init__(self, game, start_pos, target, damage, path_blue, path_red,
                 speed: float = 1.66, team: Team = Team.RED, img_size_x: int = 13, img_size_y: int = 13):
        self.__game = game
        self.__team: Team = team

        self.__damage: int = damage
        self.__speed: float = speed

        self.__img_size_x = img_size_x
        self.__img_size_y = img_size_y
        self.__pos: pygame.math.Vector2 = pygame.Vector2(start_pos)
        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = 0

        self.__target = target
        self.uuid = uuid.uuid4()

        self.__img_blue: Surface = img_load(path_blue, self.__img_size_x, self.__img_size_y)
        self.__img_red: Surface = img_load(path_red, self.__img_size_x, self.__img_size_y)

    def move(self, bullets: dict):
        self.calc_vector(self.__target)
        self.__pos += self.__vector
        if self.calc_dist(self.__target) <= self.__target.get_size()/2:
            bullets.pop(self.uuid)
            self.__target.lose_hp(self.__damage)

    def draw(self, player_team):
        if player_team == self.__team:
            temp = self.scaled_img(self.__img_blue, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.w(self.get_x()) - temp.get_width() // 2,
                                            self.h(self.get_y()) - temp.get_height() // 2))
        else:
            temp = self.scaled_img(self.__img_red, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.w(self.get_x()) - temp.get_width() // 2,
                                            self.h(self.get_y()) - temp.get_height() // 2))

    def action(self, bullets, player_team):
        self.move(bullets)
        self.draw(player_team)

    def calc_vector(self, target):
        self.__vector = pygame.math.Vector2(
            target.get_x() - self.get_x(),
            target.get_y() - self.get_y())
        temp_vector = pygame.math.Vector2(
            self.w(target.get_x() - self.get_x()),
            self.h(target.get_y() - self.get_y()))
        if self.__vector:
            pygame.math.Vector2.scale_to_length(self.__vector, self.__speed)

        # get angle between vector of going straight up and our vector
        self.__angle = temp_vector.angle_to(pygame.math.Vector2(0, -1))

    def calc_dist(self, target):
        return math.hypot(self.get_x() - target.get_x(), self.get_y() - target.get_y())

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h: int):
        return int(h / self.default_height * self.__game.get_window_height())

    def h_revert(self, h: int):
        return int(h / self.__game.get_window_height() * self.default_height)

    def w(self, w: int):
        return int(w / self.default_width * self.__game.get_window_width())

    def w_revert(self, w: int):
        return int(w / self.__game.get_window_width() * self.default_width)

    def scaled_img(self, img: pygame.Surface, angle):
        return pygame.transform.rotate(pygame.transform.scale(
            img, (self.w(self.__img_size_x), self.h(self.__img_size_y))), angle)

    def get_x(self):
        return self.__pos.x

    def get_y(self):
        return self.__pos.y

    def get_team(self):
        return self.__team
