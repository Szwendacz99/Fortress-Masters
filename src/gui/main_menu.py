import sys
from logging import info

import pygame.mouse

from gui.menu import Menu
from gui.widgets.button import Button


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.__create_game_x: float = 0.
        self.__create_game_y: float = 0.

        self.__credits_x: float = 0.
        self.__credits_y: float = 0.

        self.__quit_x: float = 0.
        self.__quit_y: float = 0.

        self.button_array = []

        self.resize()

    def resize(self):
        self.mid_w: float = self.game.get_window_width() / 2
        self.mid_h: float = self.game.get_window_height() / 2

        self.__create_game_x: float = self.mid_w
        self.__create_game_y: float = self.mid_h + self.font_manager.get_regular_font_size()

        self.__credits_x: float = self.mid_w
        self.__credits_y: float = self.mid_h + self.font_manager.get_regular_font_size() * 2

        self.__quit_x: float = self.mid_w
        self.__quit_y: float = self.mid_h + self.font_manager.get_regular_font_size() * 3

        self.button_array = [Button(pos=(self.__create_game_x, self.__create_game_y),
                                    label_text="PLAY", font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                    color="White", hovering_color="Green"),
                             Button(pos=(self.__credits_x, self.__credits_y),
                                    label_text="CREDITS", font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                    color="White", hovering_color="Green"),
                             Button(pos=(self.__quit_x, self.__quit_y),
                                    label_text="QUIT", font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                    color="White", hovering_color="Green")]

    def display_menu(self):
        self.run_display = True
        clock = pygame.time.Clock()
        while self.run_display:
            clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('Fortress Masters', self.font_manager.title_font_size, self.game.get_window_width() / 2,
                                self.font_manager.title_font_size * 3)

            for button in self.button_array:
                button.update(self.game.get_display(), mouse_position=self.mouse_pos)

            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_array[0].cursor_hovers(self.mouse_pos):
                    self.game.curr_menu = self.game.play_menu
                    self.run_display = False
                    self.game.curr_menu.display_menu()
                elif self.button_array[1].cursor_hovers(self.mouse_pos):
                    self.game.curr_menu = self.game.credits
                    self.run_display = False
                    self.game.curr_menu.display_menu()
                elif self.button_array[2].cursor_hovers(self.mouse_pos):
                    info("Exiting game...")
                    pygame.quit()
                    sys.exit(0)
