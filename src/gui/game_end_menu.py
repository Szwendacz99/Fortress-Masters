import sys
from logging import info

import pygame.mouse

from gui.menu import Menu
from gui.widgets.button import Button

from core.team import Team


class GameEndMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.__create_game_x: float = 0.
        self.__create_game_y: float = 0.

        self.__main_menu_x: float = 0.
        self.__main_menu_y: float = 0.

        self.__quit_x: float = 0.
        self.__quit_y: float = 0.

        self.button_array = []

        team_won: Team = self.game.get_team_won()
        if team_won == Team.BLU:
            self.win_color = "blue"
        else:
            self.win_color = "red"

        self.resize()

    def resize(self):
        self.mid_w: float = self.game.get_window_width() / 2
        self.mid_h: float = self.game.get_window_height() / 2

        self.__main_menu_x: float = self.mid_w
        self.__main_menu_y: float = self.mid_h + self.font_manager.get_regular_font_size() * 2

        self.__quit_x: float = self.mid_w
        self.__quit_y: float = self.mid_h + self.font_manager.get_regular_font_size() * 3

        self.button_array = [Button(pos=(self.__main_menu_x, self.__main_menu_y),
                                    label_text="RETURN TO MAIN MENU",
                                    font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                    color="White", hovering_color="Green"),
                             Button(pos=(self.__quit_x, self.__quit_y),
                                    label_text="QUIT",
                                    font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                    color="White", hovering_color="Green")]

    def display_menu(self):
        self.run_display = True
        clock = pygame.time.Clock()
        while self.run_display:
            clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('GAME OVER', self.font_manager.title_font_size, self.game.get_window_width() / 2,
                                self.font_manager.title_font_size * 3)
            if self.win_color == "blue":
                self.game.draw_text('BLUE TEAM WON', self.font_manager.title_font_size,
                                    self.game.get_window_width() / 2,
                                    self.font_manager.title_font_size * 4, color=(0, 0, 255))
            else:
                self.game.draw_text('RED TEAM WON', self.font_manager.title_font_size,
                                    self.game.get_window_width() / 2,
                                    self.font_manager.title_font_size * 4, color=(255, 0, 0))

            for button in self.button_array:
                button.update(self.game.get_display(), mouse_position=self.mouse_pos)

            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_array[0].cursor_hovers(self.mouse_pos):
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                    self.game.curr_menu.display_menu()
                elif self.button_array[1].cursor_hovers(self.mouse_pos):
                    info("Exiting game...")
                    pygame.quit()
                    sys.exit(0)
