import pygame

from game.unit_selection_button import UnitSelectionButton
from game.units.unit_type import UnitType
from game.units.spaceship import Spaceship
from game.units.spaceship_1 import Spaceship_1
from game.units.spaceship_2 import Spaceship_2
from game.units.spaceship_3 import Spaceship_3
from game.units.spaceship_4 import Spaceship_4
from game.units.spaceship_5 import Spaceship_5
from game.units.spaceship_6 import Spaceship_6
from game.units.bunker import Bunker


class UnitSelectionBar:
    """A class representing unit selection bar in game

       Attributes:
           game     Game object
           x, y     Top left position of the bar
       """

    __selection_buttons: list[UnitSelectionButton] = []
    mouse_pos = None

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.create_buttons()

    def create_buttons(self):
        """
        Method used to add new Units to selection Bar.
        If you want to add new Units to game, modify body of this method
        :return:
        """
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y, pygame.image.load('resources/img/spaceship-selection.png'), 1, self.game.get_font(14),
            UnitType.SPACESHIP, Spaceship.cost))
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y + 64, pygame.image.load('resources/img/Spaceship_pack_pack_01_BLUE-selection.png'), 1, self.game.get_font(14),
            UnitType.SPACESHIP_1, Spaceship_1.cost))
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y + 64 * 2, pygame.image.load('resources/img/Spaceship_pack_pack_02_BLUE-selection.png'), 1, self.game.get_font(14),
            UnitType.SPACESHIP_2, Spaceship_2.cost))
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y + 64 * 3, pygame.image.load('resources/img/Spaceship_pack_pack_03_BLUE-selection.png'), 1, self.game.get_font(14),
            UnitType.SPACESHIP_3, Spaceship_3.cost))
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y + 64 * 4, pygame.image.load('resources/img/Spaceship_pack_pack_04_BLUE-selection.png'), 1, self.game.get_font(14),
            UnitType.SPACESHIP_4, Spaceship_4.cost))
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y + 64 * 5, pygame.image.load('resources/img/Spaceship_pack_pack_05_BLUE-selection.png'), 1, self.game.get_font(14),
            UnitType.SPACESHIP_5, Spaceship_5.cost))
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y + 64 * 6, pygame.image.load('resources/img/Spaceship_pack_pack_06_BLUE-selection.png'), 1, self.game.get_font(14),
            UnitType.SPACESHIP_6, Spaceship_6.cost))
        self.__selection_buttons.append(UnitSelectionButton(
            self.x, self.y + 64 * 7, pygame.image.load('resources/img/bunker_blue_selection.png'), 1, self.game.get_font(14),
            UnitType.BUNKER, Bunker.cost))

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.__selection_buttons:
            button.update(self.game.get_display())

    def get_selected_unit_type(self) -> UnitType:
        for button in self.__selection_buttons:
            if button.is_clicked():
                return button.get_unit_type()

    def get_selection_buttons(self) -> list[UnitSelectionButton]:
        return self.__selection_buttons

    def resize(self):
        for button in self.__selection_buttons:
            button.resize(self.game)
