import pygame
import pygame.mouse
import os
import math


from pygame.surface import Surface
from game.laser import Laser
from game.bullet import Bullet


def img_load(path, size, angle: float = 0):
    if angle:
        return pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load(os.path.normpath(path)), (size, size)), angle)
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size, size)).convert()


class Building:
    x0: int = 0
    bg_width: int = 564

    def __init__(self, game, big: bool = False, team: int = 0, left: bool = True):
        self.__game = game
        self.__team: int = team
        self.__left: bool = left
        # big turret or small one
        self.__big: bool = big
        self.__x = None
        self.__y = None

        if big:
            self.__full_hp: int = 3500
        else:
            self.__full_hp: int = 1500
        self.__hp: int = self.__full_hp
        self.__atk_range: int = 150
        self.__atk_damage: int = 75
        self.__atk_speed: int = 60
        self.__cooldown: int = self.__atk_speed
        self.__target = None

        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = 0
        self.__alive: bool = True

        if big:
            self.__building_size = 110
        else:
            self.__building_size = 90
        self.__blue_img: Surface = img_load('resources/img/blue_turret.png', self.__building_size, -45)
        self.__red_img: Surface = img_load('resources/img/red_turret.png', self.__building_size, 135)
        self.__blue_img_dead: Surface = img_load('resources/img/blue_turret_dead.png', self.__building_size, -45)
        self.__red_img_dead: Surface = img_load('resources/img/red_turret_dead.png', self.__building_size, -45)

    def find_target(self, units, bullets):
        if self.__cooldown < self.__atk_speed:
            self.__cooldown += 1
        if self.__target is not None and self.__target.is_alive():
            if self.__cooldown == self.__atk_speed:
                self.attack(bullets)
        else:
            current_closest_target_dist = 9999999
            current_closest_target = None
            for unit in units:
                if unit.get_team() != self.__team and unit.is_alive():
                    dist_to_unit = self.calc_dist(unit) - self.get_size() / 2
                    if dist_to_unit <= current_closest_target_dist and dist_to_unit <= self.__atk_range:
                        current_closest_target = unit
                        current_closest_target_dist = dist_to_unit
                        if dist_to_unit < self.__atk_range:
                            # TODO attacking or shit knows
                            pass
            if current_closest_target is not None:
                self.__target = current_closest_target
                self.calc_vector(current_closest_target)

    def draw(self, player_team: int = 0):
        if not self.__alive:
            if self.__team == player_team:
                temp = pygame.transform.rotate(self.__blue_img_dead, self.__angle)
                self.__game.get_display().blit(temp, (self.__x - temp.get_width() // 2, self.__y - temp.get_height() // 2))
            else:
                temp = pygame.transform.rotate(self.__red_img_dead, 180 + self.__angle)
                self.__game.get_display().blit(temp, (self.__x - temp.get_width() // 2, self.__y - temp.get_height() // 2))
        # Displaying blue turret
        elif self.__team == player_team:
            temp = pygame.transform.rotate(self.__blue_img, self.__angle)
            self.__game.get_display().blit(temp, (self.__x - temp.get_width() // 2, self.__y - temp.get_height() // 2))
        # Displaying red turret
        else:
            temp = pygame.transform.rotate(self.__red_img, 180 + self.__angle)
            self.__game.get_display().blit(temp, (self.__x - temp.get_width() // 2, self.__y - temp.get_height() // 2))

    def action(self, units, bullets, player_team: int = 0):
        if self.__alive:
            self.find_target(units, bullets)
        self.draw(player_team)

    def attack(self, bullets: list[Bullet]):
        self.__cooldown = 0
        bullet_pos = pygame.Vector2(self.__x, self.__y) + 56 * self.__vector
        bullets.append(Laser(self.__game, bullet_pos, self.__target, self.__atk_damage, team=self.__team))

    def calc_dist(self, unit):
        return math.hypot(self.get_x() - unit.get_x(), self.get_y() - unit.get_y())

    def calc_vector(self, target):
        self.__vector = pygame.math.Vector2(target.get_x() - self.get_x(), target.get_y() - self.get_y())
        pygame.math.Vector2.scale_to_length(self.__vector, 1)
        # get angle between vector of going straight up and our vector
        self.__angle = self.__vector.angle_to(pygame.math.Vector2(0, -1))

    def set_coordinates(self, player_team: int = 0, x0: int = 0):
        if x0:
            self.x0 = x0
        big_x = 200
        small_x = 117

        # Establishing blue turret's coordinates
        if self.__team == player_team:
            if self.__big:
                self.__y = self.h(918)
                if self.__left:
                    self.__x = self.x0 + big_x
                else:
                    self.__x = self.x0 + self.bg_width - 200
            else:
                self.__y = self.h(800)
                if self.__left:
                    self.__x = self.x0 + small_x
                else:
                    self.__x = self.x0 + self.bg_width - small_x

        # Establishing red turret's coordinates
        else:
            if self.__big:
                self.__y = self.h(74)
                if self.__left:
                    self.__x = self.x0 + big_x
                else:
                    self.__x = self.x0 + self.bg_width - 200
            else:
                self.__y = self.h(192)
                if self.__left:
                    self.__x = self.x0 + small_x
                else:
                    self.__x = self.x0 + self.bg_width - small_x

    def lose_hp(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.die()

    def die(self):
        self.__alive = False

    def is_alive(self):
        return self.__alive

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h: int):
        return int(h / 992 * self.__game.get_window_height())

    def get_team(self):
        return self.__team

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_size(self):
        return self.__building_size
