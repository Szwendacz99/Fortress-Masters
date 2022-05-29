from uuid import UUID

import pygame
import pygame.mouse
import os
import math

from pygame.surface import Surface

from core.team import Team
import game.building as libBuilding
from game.bullet import Bullet
from pygame.math import Vector2


def img_load(path, size):
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size, size)).convert_alpha()


class Unit:
    default_width: int = 1536
    default_height: int = 864
    img_blue = None
    img_red = None
    img_blue_dead = None
    img_red_dead = None

    def __init__(self, uuid: UUID, game, start_pos, hp, atk_damage, atk_speed, atk_range, speed, team, left,
                 path_blue, path_red, path_blue_dead, path_red_dead, unit_size, bullet_type):
        self.__game = game
        self.__team: Team = team
        self.__left: bool = left

        self.__hp_full: int = hp
        self.__hp: int = self.__hp_full
        self.__atk_damage: int = atk_damage
        self.__atk_speed: int = atk_speed
        self.__cooldown: int = atk_speed
        self.__atk_range: int = atk_range
        self.__speed: float = speed
        self.__seeing_range: int = 200

        self.__target = None
        self.__target_in_atk_range: bool = False

        self.__alive: bool = True
        self.__opacity: int = 253

        self.uuid: UUID == uuid

        self.__pos: pygame.math.Vector2 = pygame.math.Vector2(
            (self.w_revert(start_pos[0]), self.h_revert(start_pos[1])))
        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = 0
        self.__unit_size: int = unit_size
        self.__bullet_type: Bullet = bullet_type

        if self.img_blue is None:
            self.img_blue: Surface = img_load(path_blue, self.__unit_size)
            self.img_red: Surface = img_load(path_red, self.__unit_size)
            self.img_blue_dead = img_load(path_blue_dead, self.__unit_size)
            self.img_red_dead = img_load(path_red_dead, self.__unit_size)

    def find_target(self, buildings: dict, units: dict[UUID, 'Unit'], bullets: dict[UUID, Bullet]):

        # attacking
        if self.__cooldown < self.__atk_speed:
            self.__cooldown += 1
        if self.__target is not None and self.__target_in_atk_range and self.__target.is_alive():
            if self.calc_dist(self.__target) > self.__atk_range:
                self.__target_in_atk_range = False
            elif self.__cooldown == self.__atk_speed:
                self.attack(bullets)

        # looking for closest target
        else:
            current_closest_target_dist = 9999999
            current_closest_target = None
            current_target_in_atk_range: bool = False
            for building in buildings.values():
                if building.get_team() != self.__team and building.is_alive():
                    dist_to_building = self.calc_dist(building)
                    if dist_to_building <= current_closest_target_dist:
                        current_closest_target = building
                        current_closest_target_dist = dist_to_building
                        if dist_to_building <= self.__atk_range:
                            current_target_in_atk_range = True

            for unit in units.values():
                if unit.get_team() != self.__team and unit.is_alive():
                    dist_to_unit = self.calc_dist(unit)
                    if dist_to_unit <= current_closest_target_dist and dist_to_unit <= self.__seeing_range:
                        current_closest_target = unit
                        current_closest_target_dist = dist_to_unit
                        if dist_to_unit <= self.__atk_range:
                            current_target_in_atk_range = True

            self.__target = current_closest_target
            self.__target_in_atk_range = current_target_in_atk_range
            self.calc_vector(current_closest_target)

    def attack(self, bullets: dict[UUID, Bullet]):
        self.__cooldown = 0
        bullet_pos = self.__pos + 80 * self.__vector
        bullet = self.__bullet_type(self.__game, bullet_pos, self.__target, self.__atk_damage, team=self.__team)
        bullets[bullet.uuid] = bullet

    def move(self):
        if not self.__target_in_atk_range:
            self.__pos += self.__vector

    def draw(self, player_team, units: dict):
        if self.__opacity <= 12:
            units.pop(self.uuid)
        elif not self.__alive:
            self.__opacity -= 1
            if player_team == self.__team:
                temp = self.scaled_img(self.img_blue_dead, self.__angle)
                temp.set_alpha(self.__opacity)
                self.__game.get_display().blit(temp,
                                               (self.w(self.get_x()) - temp.get_width() // 2,
                                                self.h(self.get_y()) - temp.get_height() // 2))
            else:
                temp = self.scaled_img(self.img_red_dead, self.__angle)
                temp.set_alpha(self.__opacity)
                self.__game.get_display().blit(temp,
                                               (self.w(self.get_x()) - temp.get_width() // 2,
                                                self.h(self.get_y()) - temp.get_height() // 2))

        elif player_team == self.__team:
            temp = self.scaled_img(self.img_blue, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.w(self.get_x()) - temp.get_width() // 2,
                                            self.h(self.get_y()) - temp.get_height() // 2))
        else:
            temp = self.scaled_img(self.img_red, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.w(self.get_x()) - temp.get_width() // 2,
                                            self.h(self.get_y()) - temp.get_height() // 2))

    def action(self, buildings, units, bullets, player_team):
        if self.__alive:
            self.find_target(buildings, units, bullets)
            self.move()
            self.draw(player_team, units)
        else:
            self.draw(player_team, units)

    def lose_hp(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.die()

    def die(self):
        self.__alive = False

    def calc_vector(self, target=None):
        if target is None:
            target = self.__target
        self.__vector = pygame.math.Vector2(target.get_x() - self.get_x(), target.get_y() - self.get_y())
        temp_vector = pygame.math.Vector2(self.w(target.get_x() - self.get_x()), self.h(target.get_y() - self.get_y()))
        if self.__vector:
            pygame.math.Vector2.scale_to_length(self.__vector, self.__speed)

        # get angle between vector of going straight up and our vector
        self.__angle = temp_vector.angle_to(pygame.math.Vector2(0, -1))

    def calc_dist(self, target):
        if target.__class__ == libBuilding.Building:
            return math.hypot(self.get_x() - target.get_x(), self.get_y() - target.get_y()) - target.get_size() / 2
        return math.hypot(self.get_x() - target.get_x(), self.get_y() - target.get_y())

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h):
        return int(h / self.default_height * self.__game.get_window_height())

    def h_revert(self, h: int):
        return int(h / self.__game.get_window_height() * self.default_height)

    def w(self, w):
        return int(w / self.default_width * self.__game.get_window_width())

    def w_revert(self, w: int):
        return int(w / self.__game.get_window_width() * self.default_width)

    def scaled_img(self, img: pygame.Surface, angle):
        return pygame.transform.rotate(pygame.transform.scale(
            img, (self.w(self.__unit_size), self.h(self.__unit_size))), angle)

    def get_x(self):
        return self.__pos.x

    def get_y(self):
        return self.__pos.y

    def get_team(self):
        return self.__team

    def get_size(self):
        return self.__unit_size

    def is_alive(self):
        return self.__alive

    def get_pos(self) -> Vector2:
        return self.__pos

    def set_pos(self, pos: Vector2):
        self.__pos = pos
