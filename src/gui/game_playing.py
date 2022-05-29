from uuid import uuid4

import pygame
import pygame.mouse
import os

from pygame.surface import Surface

from core.client import Client
from core.team import Team
from game.unit_type import UnitType
from gui.menu import Menu
from game.building import Building
from game.spaceship import Spaceship
from game.unit_selection_bar import UnitSelectionBar
from network.messages.new_unit_message import NewUnitMessage


class GamePlaying(Menu):
    default_width: int = 1536
    default_height: int = 864

    def __init__(self, game):
        Menu.__init__(self, game)
        # TODO establishing on which team is a player
        self.__fps: int = 60
        self.__background_img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/map_bg.png')), (self.w(564), self.h(864))).convert()

        self.__unit_selection_bar = UnitSelectionBar(game, self.game.get_window_width() / 2 + 564 / 2,
                                                     self.game.get_window_height() / 10)

    def resize(self):
        self.__background_img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/map_bg.png')),
            (self.w(564), self.h(864))).convert()
        for unit in Client.units.values():
            unit.calc_vector()

    def display_menu(self):
        clock = pygame.time.Clock()
        self.run_display = True
        self.create_buildings()
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            clock.tick(self.__fps)
            self.draw()

            self.__unit_selection_bar.update()

            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def draw(self):
        self.game.get_display().fill(self.game.BLACK)
        self.game.get_display().blit(self.__background_img,
                                     (self.game.get_window_width()/2 - self.__background_img.get_width() // 2, 0))

        # iterating this way to prevent
        # RuntimeError: dictionary changed size during iteration
        for building in [f for f in Client.buildings.values()]:
            building.action(Client.units, Client.bullets, self.game.client.get_identity().get_team())
        for bullet in [f for f in Client.bullets.values()]:
            bullet.action(Client.bullets, self.game.client.get_identity().get_team())
        for unit in [f for f in Client.units.values()]:
            unit.action(Client.buildings, Client.units, Client.bullets, self.game.client.get_identity().get_team())

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bar_clicked = False
                selection_buttons = self.__unit_selection_bar.get_selection_buttons()
                for button in selection_buttons:
                    if button.cursor_hovers(mouse_position=self.mouse_pos):
                        for button_1 in selection_buttons:
                            button_1.set_clicked(False)
                        button.set_clicked(True)
                        bar_clicked = True
                if not bar_clicked:
                    # TODO send message to server that unit is being placed
                    if event.button == 1 or event.button == 5:
                        self.game.client.send_message(NewUnitMessage(uuid4(),
                                                                     unit_type=UnitType.SPACESHIP,
                                                                     pos=self.mouse_pos,
                                                                     team=Team.RED))
                        # Client.units.append(Spaceship(self.game, self.mouse_pos))
                    else:
                        self.game.client.send_message(NewUnitMessage(uuid4(),
                                                                     unit_type=UnitType.SPACESHIP,
                                                                     pos=self.mouse_pos,
                                                                     team=Team.BLU))
                        # Client.units.append(Spaceship(self.game, self.mouse_pos, team=1))

    def create_buildings(self):
        Client.add_building(Building(self.game, True, Team.RED))
        Client.add_building(Building(self.game, True, Team.RED, False))
        Client.add_building(Building(self.game, True, Team.BLU))
        Client.add_building(Building(self.game, True, Team.BLU, False))
        Client.add_building(Building(self.game, False, Team.RED))
        Client.add_building(Building(self.game, False, Team.RED, False))
        Client.add_building(Building(self.game, False, Team.BLU))
        Client.add_building(Building(self.game, False, Team.BLU, False))
        # if self.game.client is not None:
        for building in Client.buildings.values():
            building.set_coordinates(self.game.client.get_identity().get_team())

    def h(self, h: int):
        return int(h / self.default_height * self.game.get_window_height())

    def w(self, w: int):
        return int(w / self.default_width * self.game.get_window_width())
