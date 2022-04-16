import pygame.mouse

import src.GUI.Menu as libMenu
import src.GUI.Widgets.Button as libButton


class MainMenu(libMenu.Menu):
    def __init__(self, game):
        libMenu.Menu.__init__(self, game)

        self.__create_game_x: float = self.mid_w
        self.__create_game_y: float = self.mid_h + self.text_font_size

        self.__join_game_x: float = self.mid_w
        self.__join_game_y: float = self.mid_h + self.text_font_size * 2

        self.__credits_x: float = self.mid_w
        self.__credits_y: float = self.mid_h + self.text_font_size * 3

        self.__quit_x: float = self.mid_w
        self.__quit_y: float = self.mid_h + self.text_font_size * 4

        self.button_array = [libButton.Button(image=None, pos=(self.__create_game_x, self.__create_game_y),
                                              label_text="CREATE GAME", font=self.game.get_font(self.text_font_size),
                                              base_color="White", hovering_color="Green"),
                             libButton.Button(image=None, pos=(self.__join_game_x, self.__join_game_y),
                                              label_text="JOIN GAME", font=self.game.get_font(self.text_font_size),
                                              base_color="White", hovering_color="Green"),
                             libButton.Button(image=None, pos=(self.__credits_x, self.__credits_y),
                                    label_text="CREDITS", font=self.game.get_font(self.text_font_size),
                                    base_color="White", hovering_color="Green"),
                             libButton.Button(image=None, pos=(self.__quit_x, self.__quit_y),
                                    label_text="QUIT", font=self.game.get_font(self.text_font_size),
                                    base_color="White", hovering_color="Green")]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('Fortress Masters', self.title_font_size, self.game.get_window_width() / 2,
                                self.game.get_window_height() / 2 - self.title_font_size)

            for button in self.button_array:
                button.changeColor(self.mouse_pos)
                button.update(self.game.get_display())

            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_array[0].checkForInput(self.mouse_pos):
                    # TODO: Implement Create Game Menu
                    self.game.curr_menu = self.game.new_game
                    self.run_display = False
                    self.game.curr_menu.display_menu()
                elif self.button_array[0].checkForInput(self.mouse_pos):
                    # TODO: Implement Join Game Menu
                    pass
                elif self.button_array[2].checkForInput(self.mouse_pos):
                    self.game.curr_menu = self.game.credits
                    self.run_display = False
                    self.game.curr_menu.display_menu()
                elif self.button_array[3].checkForInput(self.mouse_pos):
                    pygame.quit()
