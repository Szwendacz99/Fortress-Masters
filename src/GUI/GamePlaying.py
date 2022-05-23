import pygame
import pygame.mouse
import os

from pygame.rect import Rect
from pygame.surface import Surface

from GUI.Menu import Menu
from Utils.Building import Building
from Utils.Unit import Unit


class GamePlaying(Menu):
    __buildings: list[Building] = []
    __units: list[Unit] = []

    def __init__(self, game):
        Menu.__init__(self, game)
        # TODO establishing on which team is a player
        self.__player_team = 0
        self.__fps: int = 60
        self.__background_img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/map_bg.png')), (564, self.game.get_window_height())).convert()
        self.__x0: int = self.mid_w - self.__background_img.get_width() // 2
        self.create_buildings()

    def display_menu(self):
        clock = pygame.time.Clock()
        self.run_display = True
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            clock.tick(self.__fps)
            self.draw()
            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def draw(self):
        self.game.get_display().fill(self.game.BLACK)
        self.game.get_display().blit(self.__background_img,
                                     (self.mid_w - self.__background_img.get_width() // 2, 0))
        for building in self.__buildings:
            building.action(self.game, self.__units, self.__player_team)
        for unit in self.__units:
            unit.action(self.__buildings, self.__units)

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # TODO send message to server that unit is being placed
                if event.button == 1 or event.button == 5:
                    self.__units.append(Unit(self.game, self.mouse_pos))
                else:
                    self.__units.append(Unit(self.game, self.mouse_pos, team=1))

    def create_buildings(self):

        self.__buildings.append(Building(True, 0))
        self.__buildings.append(Building(True, 0, False))
        self.__buildings.append(Building(True, 1))
        self.__buildings.append(Building(True, 1, False))
        self.__buildings.append(Building(False, 0))
        self.__buildings.append(Building(False, 0, False))
        self.__buildings.append(Building(False, 1))
        self.__buildings.append(Building(False, 1, False))
        for building in self.__buildings:
            building.set_coordinates(self.game, self.__player_team, self.__x0)



