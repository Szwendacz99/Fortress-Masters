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

from network.messages.new_bullet_message import NewBulletMessage


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

    def __init__(self, uuid: UUID, game, start_pos, hp, atk_damage, atk_speed, atk_range, speed, team, client_team,
                 left, path_blue, path_red, path_blue_dead, path_red_dead, unit_size, bullet_type):
        self.__game = game
        self.__team: Team = team
        self.__left: bool = left

        # TODO get info from server, which team is server on
        self.__server_team: Team = Team.RED

        self.__enemy_of_server: bool = (client_team != self.__server_team)

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

        self.__pos: Vector2 = Vector2(0, 0)
        new_enemy_unit: bool = (team != client_team)
        self.set_pos(start_pos, new_enemy_unit=new_enemy_unit, new_my_unit=not new_enemy_unit)
        self.__vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = 0

        # print(f"{client_team}  {self.__server_team}  {self.__enemy_of_server}")
        # print(f"{client_team}  {team}  {new_enemy_unit}")

        self.__unit_size: int = unit_size
        self.__bullet_type: Bullet = bullet_type

        if self.img_blue is None:
            self.img_blue: Surface = img_load(path_blue, self.__unit_size)
            self.img_red: Surface = img_load(path_red, self.__unit_size)
            self.img_blue_dead = img_load(path_blue_dead, self.__unit_size)
            self.img_red_dead = img_load(path_red_dead, self.__unit_size)

    def find_target(self, buildings: list, units: dict[UUID, 'Unit']):

        # attacking
        if self.__cooldown < self.__atk_speed:
            self.__cooldown += 1
        if self.__target is not None and self.__target_in_atk_range and self.__target.is_alive():
            if self.calc_dist(self.__target) > self.__atk_range:
                self.__target_in_atk_range = False
            elif self.__cooldown == self.__atk_speed:
                self.attack()

        # looking for closest target
        else:
            current_closest_target_dist = 9999999
            current_closest_target = None
            current_target_in_atk_range: bool = False
            for building in buildings:
                if building.get_team() != self.__team and building.is_alive():
                    dist_to_building = self.calc_dist(building)
                    # print(f"{building.get_team()} {building.get_x()} {building.get_y()}")
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
            if current_closest_target is not None:
                self.calc_vector(current_closest_target)

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
        if self.__target.__class__ == libBuilding.Building:
            msg.set_building_target_id(self.__game.client.buildings.index(self.__target))
        self.__game.client.send_message(msg)

    def shoot_target(self, target):
        bullet_pos = self.__pos + 80 * self.__vector
        bullet = self.__bullet_type(self.__game, bullet_pos, target, self.__atk_damage, team=self.__team)
        self.__game.client.bullets[bullet.uuid] = bullet

    def move(self):
        if not self.__target_in_atk_range:
            self.__pos += self.__vector

    def draw(self, player_team, units: dict):

        # print(f"{self.get_x()}  {self.get_y()}")
        if self.__opacity <= 12:
            units.pop(self.uuid)
        elif not self.__alive:
            self.__opacity -= 1

            # Displaying dead units of player's team
            if player_team == self.__team:
                if self.__team == Team.RED:
                    temp = self.scaled_img(self.img_red_dead, self.__angle)
                else:
                    temp = self.scaled_img(self.img_blue_dead, self.__angle)
                temp.set_alpha(self.__opacity)
                self.__game.get_display().blit(temp,
                                               (self.w(self.get_x()) - temp.get_width() // 2,
                                                self.h(self.get_y()) - temp.get_height() // 2))
            # Displaying dead units of enemies' team
            else:
                if self.__team == Team.RED:
                    temp = self.scaled_img(self.img_red_dead, self.__angle)
                else:
                    temp = self.scaled_img(self.img_blue_dead, self.__angle)
                temp.set_alpha(self.__opacity)
                self.__game.get_display().blit(temp,
                                               (self.w(self.get_x()) - temp.get_width() // 2,
                                                self.h(self.get_y()) - temp.get_height() // 2))

        # Displaying units of the player's team
        elif player_team == self.__team:
            if self.__team == Team.RED:
                temp = self.scaled_img(self.img_red, self.__angle)
            else:
                temp = self.scaled_img(self.img_blue, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.w(self.get_x()) - temp.get_width() // 2,
                                            self.h(self.get_y()) - temp.get_height() // 2))
        # Displaying units of the enemies' team
        else:
            if self.__team == Team.RED:
                temp = self.scaled_img(self.img_red, self.__angle)
            else:
                temp = self.scaled_img(self.img_blue, self.__angle)
            self.__game.get_display().blit(temp,
                                           (self.w(self.get_x()) - temp.get_width() // 2,
                                            self.h(self.get_y()) - temp.get_height() // 2))

    def action(self, buildings, units, player_team):
        if self.__alive:
            self.find_target(buildings, units)
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

    def calc_dist(self, target):
        if target.__class__ == libBuilding.Building:
            return math.hypot(self.get_x() - target.get_x(),
                              self.get_y() - target.get_y()) - target.get_size() / 2
        return math.hypot(self.get_x() - target.get_x(),
                          self.get_y() - target.get_y())

    def calc_vector(self, target=None):
        if target is None:
            target = self.__target
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

    def set_pos(self, pos, new_enemy_unit: bool = False, new_my_unit: bool = False):
        if new_enemy_unit or (self.__enemy_of_server and not new_my_unit):
            x = self.default_width - pos[0]
            y = self.default_height - pos[1]
            self.__pos = pygame.Vector2(x, y)
        else:
            self.__pos = pygame.Vector2(pos)

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
