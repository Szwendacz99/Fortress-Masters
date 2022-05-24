import pygame
import pygame.mouse
import os
import math


from pygame.surface import Surface
from game.building import Building
from game.rocket import Rocket
from game.bullet import Bullet
from pygame.math import Vector2


def img_load(path, size):
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size, size)).convert_alpha()


class Unit:
    img_blue = None
    img_red = None
    img_blue_dead = None
    img_red_dead = None
    img_size = 45

    def __init__(self, game, start_pos, speed: float = 0.3, atk_range: int = 100, team: int = 0, left: bool = True):
        self.__game = game
        self.__team: int = team
        self.__left: bool = left

        self.__hp_full: int = 255
        self.__hp: int = self.__hp_full
        self.__speed: float = speed
        self.__atk_range: int = atk_range
        self.__seeing_range: int = 200
        self.__atk_damage: int = 50
        self.__atk_speed: int = 110
        self.__cooldown: int = self.__atk_speed

        self.__target = None
        self.__target_in_atk_range: bool = False

        self.__alive: bool = True
        self.__opacity: int = 244

        self.__pos: pygame.math.Vector2 = pygame.math.Vector2(start_pos)
        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = 0

        if self.img_blue is None:
            self.img_blue: Surface = img_load('resources/img/ship_blue.png', self.img_size)
            self.img_red: Surface = img_load('resources/img/ship_red.png', self.img_size)
            self.img_blue_dead = img_load('resources/img/ship_blue_dead.png', self.img_size)
            self.img_red_dead = img_load('resources/img/ship_red_dead.png', self.img_size)

    def find_target(self, buildings: list[Building], units: list['Unit'], bullets: list[Rocket]):
        if self.__cooldown < self.__atk_speed:
            self.__cooldown += 1
        if self.__target is not None and self.__target_in_atk_range and self.__target.is_alive():
            if self.__cooldown == self.__atk_speed:
                self.attack(bullets)

        else:
            current_closest_target_dist = 9999999
            current_closest_target = None
            current_target_in_atk_range: bool = False
            for building in buildings:
                if building.get_team() != self.__team and building.is_alive():
                    dist_to_building = self.calc_dist(building) - building.get_size() / 2
                    if dist_to_building <= current_closest_target_dist:
                        current_closest_target = building
                        current_closest_target_dist = dist_to_building
                        if dist_to_building < self.__atk_range:
                            current_target_in_atk_range = True

            for unit in units:
                if unit.get_team() != self.__team and unit.is_alive():
                    dist_to_unit = self.calc_dist(unit)
                    if dist_to_unit <= current_closest_target_dist and dist_to_unit <= self.__seeing_range:
                        current_closest_target = unit
                        current_closest_target_dist = dist_to_unit
                        if dist_to_unit < self.__atk_range:
                            current_target_in_atk_range = True

            self.__target = current_closest_target
            self.__target_in_atk_range = current_target_in_atk_range
            self.calc_vector(current_closest_target)

    def attack(self, bullets: list[Bullet]):
        self.__cooldown = 0
        bullet_pos = self.__pos + 80 * self.__vector
        bullets.append(Rocket(self.__game, bullet_pos, self.__target, self.__atk_damage, team=self.__team))

    def move(self):
        if not self.__target_in_atk_range:
            self.__pos += self.__vector

    def draw(self, player_team, units):
        if self.__opacity <= 20:
            units.remove(self)
        elif not self.__alive:
            self.__opacity -= 1
            if player_team == self.__team:
                temp = pygame.transform.rotate(self.img_blue_dead, self.__angle)
                temp.set_alpha(self.__opacity)
                self.__game.get_display().blit(temp,
                                               (self.get_x() - temp.get_width() // 2,
                                                self.get_y() - temp.get_height() // 2))
            else:
                temp = pygame.transform.rotate(self.img_red_dead, self.__angle)
                temp.set_alpha(self.__opacity)
                self.__game.get_display().blit(temp,
                                               (self.get_x() - temp.get_width() // 2,
                                                self.get_y() - temp.get_height() // 2))

        elif player_team == self.__team:
            temp = pygame.transform.rotate(self.img_blue, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.get_x() - temp.get_width() // 2,
                                            self.get_y() - temp.get_height() // 2))
        else:
            temp = pygame.transform.rotate(self.img_red, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.get_x() - temp.get_width() // 2,
                                            self.get_y() - temp.get_height() // 2))

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

    def get_size(self):
        return self.img_size

    def is_alive(self):
        return self.__alive
