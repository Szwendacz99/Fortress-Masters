import pygame
import pygame.mouse
import os

from pygame.surface import Surface

from gui.menu import Menu
from game.building import Building
from game.unit import Unit
from game.bullet import Bullet
from game.spaceship import Spaceship
from game.unit_selection_bar import UnitSelectionBar


class GamePlaying(Menu):
    default_width: int = 1536
    default_height: int = 864

    buildings: list[Building] = []
    units: list[Unit] = []
    bullets: list[Bullet] = []

    def __init__(self, game):
        Menu.__init__(self, game)
        # TODO establishing on which team is a player
        self.__player_team = 0
        self.__fps: int = 60
        self.__background_img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/map_bg.png')), (self.w(564), self.h(864))).convert()
        self.create_buildings()

        self.__unit_selection_bar = UnitSelectionBar(game, self.game.get_window_width() / 2 + 564 / 2,
                                                     self.game.get_window_height() / 10)

    def resize(self):
        self.__background_img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('resources/img/map_bg.png')),
            (self.w(564), self.h(864))).convert()
        for unit in self.units:
            unit.calc_vector()

    def display_menu(self):
        clock = pygame.time.Clock()
        self.run_display = True
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

        for building in self.buildings:
            building.action(self.units, self.bullets, self.__player_team)
        for bullet in self.bullets:
            bullet.action(self.bullets, self.__player_team)
        for unit in self.units:
            unit.action(self.buildings, self.units, self.bullets, self.__player_team)

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
                        self.units.append(Spaceship(self.game, self.mouse_pos))
                    else:
                        self.units.append(Spaceship(self.game, self.mouse_pos, team=1))

    def create_buildings(self):
        self.buildings.append(Building(self.game, True, 0))
        self.buildings.append(Building(self.game, True, 0, False))
        self.buildings.append(Building(self.game, True, 1))
        self.buildings.append(Building(self.game, True, 1, False))
        self.buildings.append(Building(self.game, False, 0))
        self.buildings.append(Building(self.game, False, 0, False))
        self.buildings.append(Building(self.game, False, 1))
        self.buildings.append(Building(self.game, False, 1, False))
        for building in self.buildings:
            building.set_coordinates(self.__player_team)

    def h(self, h: int):
        return int(h / self.default_height * self.game.get_window_height())

    def w(self, w: int):
        return int(w / self.default_width * self.game.get_window_width())
