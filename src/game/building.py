import uuid
from uuid import UUID

import pygame
import pygame.mouse
import os
import math

from pygame.surface import Surface

from game.team import Team
from game.laser import Laser
from game.units.unit import Unit
from network.messages.new_bullet_message import NewBulletMessage


def img_load(path, size, angle: float = 0):
    if angle:
        return pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load(os.path.normpath(path)), (size, size)), angle)
    return pygame.transform.scale(pygame.image.load(
        os.path.normpath(path)), (size, size)).convert()


class Building:
    x0: int = 0
    default_width: int = 1536
    default_height: int = 864
    bg_width: int = 564

    def __init__(self, game, big: bool = False, team: Team = None, left: bool = True):
        self.__game = game
        self.__team: Team = team
        self.__left: bool = left

        # big turret or small one
        self.__big: bool = big
        self.__x = None
        self.__y = None
        self.uuid = uuid.uuid4()

        if big:
            self.__full_hp: int = 2150
            self.__atk_damage: int = 60
            self.__atk_speed: int = 48

            self.__currency: int = 150
            self.__currency_income: int = 10
        else:
            self.__full_hp: int = 1250
            self.__atk_damage: int = 45
            self.__atk_speed: int = 54

        self.__hp: int = self.__full_hp
        self.__atk_range: int = 155
        self.__cooldown: int = self.__atk_speed
        self.__target = None

        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = 0
        self.__alive: bool = True

        if big:
            self.__building_size = 120
        else:
            self.__building_size = 100
        self.__blue_img: Surface = img_load('resources/img/blue_turret.png', self.__building_size, -45)
        self.__red_img: Surface = img_load('resources/img/red_turret.png', self.__building_size, -45)
        self.__blue_img_dead: Surface = img_load('resources/img/blue_turret_dead.png', self.__building_size, -45)
        self.__red_img_dead: Surface = img_load('resources/img/red_turret_dead.png', self.__building_size, -45)

    def find_target(self, units: dict[UUID, Unit]):

        # attacking
        if self.__cooldown < self.__atk_speed:
            self.__cooldown += 1

        if self.__target is not None and self.__target.is_alive() and \
                self.calc_dist(self.__target) - self.get_size() / 2 <= self.__atk_range:
            if self.__cooldown == self.__atk_speed:
                self.attack()

        # looking for closest target
        else:
            current_closest_target_dist = 9999999
            current_closest_target = None
            for unit in units.values():
                if unit.get_team() != self.__team and unit.is_alive():
                    dist_to_unit = self.calc_dist(unit) - self.get_size() / 2
                    if dist_to_unit <= current_closest_target_dist and dist_to_unit <= self.__atk_range:
                        current_closest_target = unit
                        current_closest_target_dist = dist_to_unit

            if current_closest_target is not None:
                self.__target = current_closest_target
                self.calc_vector(current_closest_target)

    def draw(self, player_team: Team):

        if not self.__alive:
            # Displaying dead lower turrets
            if self.__team == player_team:
                if self.__team == Team.RED:
                    temp = self.scaled_img(self.__red_img_dead, self.__angle)
                else:
                    temp = self.scaled_img(self.__blue_img_dead, self.__angle)
                self.__game.get_display().blit(temp,
                                               (self.w(self.__x) - temp.get_width() // 2,
                                                self.h(self.__y) - temp.get_height() // 2))
            # Displaying dead upper turrets
            else:
                if self.__angle == 0:
                    self.__angle = 180
                if self.__team == Team.RED:
                    temp = self.scaled_img(self.__red_img_dead, self.__angle)
                else:
                    temp = self.scaled_img(self.__blue_img_dead, self.__angle)

                self.__game.get_display().blit(temp,
                                               (self.w(self.__x) - temp.get_width() // 2,
                                                self.h(self.__y) - temp.get_height() // 2))

        # Displaying lower turrets
        elif self.__team == player_team:
            if self.__team == Team.RED:
                temp = self.scaled_img(self.__red_img, self.__angle)
            else:
                temp = self.scaled_img(self.__blue_img, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.w(self.__x) - temp.get_width() // 2,
                                            self.h(self.__y) - temp.get_height() // 2))
        # Displaying upper turrets
        else:
            if self.__angle == 0:
                self.__angle = 180
            if self.__team == Team.RED:
                temp = self.scaled_img(self.__red_img, self.__angle)
            else:
                temp = self.scaled_img(self.__blue_img, self.__angle)

            self.__game.get_display().blit(temp,
                                           (self.w(self.__x) - temp.get_width() // 2,
                                            self.h(self.__y) - temp.get_height() // 2))

        if self.is_alive():
            self.render_hp_bar()

    def action(self, units, player_team: Team = 0):
        if self.__alive:
            self.find_target(units)
        self.draw(player_team)

    def attack(self):
        self.__cooldown = 0
        if not self.__game.client.get_is_server():
            return

        msg = NewBulletMessage(
            self.uuid,
            self.__class__,
            team=self.__team,
            target_type=self.__target.__class__,
            target_uuid=self.__target.uuid
        )
        msg.set_building_source_id(self.__game.client.buildings.index(self))
        self.__game.client.send_message(msg)

    def shoot_target(self, target):
        if self.__big:
            distance_of_bullet = 55
        else:
            distance_of_bullet = 46
        bullet_pos = pygame.Vector2(self.__x, self.__y) + distance_of_bullet * self.__vector
        laser = Laser(self.__game, bullet_pos, target, self.__atk_damage, team=self.__team)
        self.__game.client.bullets[laser.uuid] = laser

    def set_coordinates(self, player_team: Team):

        self.x0 = self.default_width // 2 - self.bg_width // 2

        big_x = 200
        small_x = 117
        small_h = 167
        big_h = 64

        # Establishing player's turrets coordinates
        if self.__team == player_team:
            if self.__big:
                self.__y = self.default_height - big_h
                if self.__left:
                    self.__x = self.x0 + big_x
                else:
                    self.__x = self.x0 + self.bg_width - big_x
            else:
                self.__y = self.default_height - small_h
                if self.__left:
                    self.__x = self.x0 + small_x
                else:
                    self.__x = self.x0 + self.bg_width - small_x

        # Establishing enemies' turrets coordinates
        else:
            if self.__big:
                self.__y = big_h
                if self.__left:
                    self.__x = self.x0 + self.bg_width - big_x
                else:
                    self.__x = self.x0 + big_x
            else:
                self.__y = small_h
                if self.__left:
                    self.__x = self.x0 + self.bg_width - small_x
                else:
                    self.__x = self.x0 + small_x

    def lose_hp(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.__hp = 0
            self.die()

    def die(self):
        self.__alive = False

    def calc_dist(self, target):
        return math.hypot(self.get_x() - target.get_x(), self.get_y() - target.get_y())

    def calc_vector(self, target):
        self.__vector = pygame.math.Vector2(
            target.get_x() - self.get_x(), target.get_y() - self.get_y())
        pygame.math.Vector2.scale_to_length(self.__vector, 1)

        # get angle between vector of going straight up and our vector
        self.__angle = self.__vector.angle_to(pygame.math.Vector2(0, -1))

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h: int):
        return int(h / self.default_height * self.__game.get_window_height())

    def w(self, w: int):
        return int(w / self.default_width * self.__game.get_window_width())

    def scaled_img(self, img: pygame.Surface, angle):
        return pygame.transform.rotate(pygame.transform.scale(
            img, (self.w(self.__building_size), self.h(self.__building_size))), angle)

    def subtract_currency(self, amount: int):
        self.__currency -= amount

    def add_currency(self, amount: int = 0):
        if self.is_alive():
            if amount:
                self.__currency += amount
            else:
                self.__currency += self.__currency_income

    def render_hp_bar(self):

        if self.__hp != self.__full_hp:
            hp_bar_length: int = 48
            hp_bar_height: int = 6
            current_hp_percentage: float = float(self.__hp) / float(self.__full_hp)
            pygame.draw.rect(self.__game.get_display(), (255, 0, 0),
                             (self.w(self.get_x() - hp_bar_length / 2),
                              self.h(self.get_y() - 40 - hp_bar_height),
                              self.w(hp_bar_length), self.h(hp_bar_height)))
            pygame.draw.rect(self.__game.get_display(), (0, 0, 0),
                             (self.w(math.ceil(self.get_x() - hp_bar_length / 2 + hp_bar_length * current_hp_percentage)),
                              self.h(self.get_y() - 40 - hp_bar_height),
                              self.w(hp_bar_length - math.floor(hp_bar_length * current_hp_percentage)),
                              self.h(hp_bar_height)))

    def is_alive(self):
        return self.__alive

    def get_team(self):
        return self.__team

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_size(self):
        return self.__building_size

    def get_big(self) -> bool:
        return self.__big

    def get_left(self) -> bool:
        return self.__left

    def get_currency(self):
        return self.__currency

    def get_hp(self):
        return self.__hp

    def get_full_hp(self):
        return  self.__full_hp
