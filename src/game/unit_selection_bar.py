import pygame

from game.unit_selection_button import UnitSelectionButton
from game.unit_type import UnitType


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
        self.__selection_buttons.append(UnitSelectionButton(self.x, self.y, pygame.image.load('resources/img/spaceship-selection.png'), 1, self.game.get_font(14), UnitType.SPACESHIP))

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.__selection_buttons:
            button.update(self.game.get_display())

    def get_selected_unit(self) -> UnitType:
        for button in self.__selection_buttons:
            if button.is_clicked():
                return button.get_unit_type()

    def get_selection_buttons(self) -> list[UnitSelectionButton]:
        return self.__selection_buttons

