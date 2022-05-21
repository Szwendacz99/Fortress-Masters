import pygame
import pygame.mouse
import os

from pygame.surface import Surface

from gui.menu import Menu
from game.building import Building
from game.unit import Unit


class GamePlaying(Menu):
    __buildings: list[Building] = []
    __units: list[Unit] = []

    def __init__(self, game):
        Menu.__init__(self, game)
        # TODO establishing on which team is a player
        self.__player_team = 0
        self.__fps: int = 60
        self.__background_img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/map_bg.png')), (564, self.game.get_window_height()))
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
            building.draw(self.game, self.__player_team)
        for unit in self.__units:
            unit.action(self.__buildings, self.__units, self.__player_team)

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__units.append(Unit(self.game, self.mouse_pos))

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


