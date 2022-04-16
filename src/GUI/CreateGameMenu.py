import pygame.mouse

import src.GUI.Menu as libMenu
import src.GUI.Widgets.Button as libButton
import src.GUI.Widgets.TextInput as libTextInput


class NewGameMenu(libMenu.Menu):
    def __init__(self, game):
        libMenu.Menu.__init__(self, game)

        self.back_button = libButton.Button(image=None, pos=(self.game.get_window_width() / 2,
                                                             self.game.get_window_height() / 2),
                                            label_text="GO BACK", font=self.game.get_font(self.text_font_size),
                                            base_color="Red", hovering_color="Green")

        self.test_input = libTextInput.TextInput(background_color="WHITE", pos=(self.mid_w, self.mid_h + self.text_font_size ),
                                              font=self.game.get_font(self.text_font_size), font_color="BLACK")


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('Lobby', self.title_font_size, self.game.get_window_width() / 2,
                                self.game.get_window_height() / 2 - self.title_font_size)

            self.back_button.changeColor(self.mouse_pos)
            self.back_button.update(self.game.get_display())


            self.test_input.update(self.game.get_display())

            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_menu.display_menu()
                    self.run_display = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.checkForInput(self.mouse_pos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_menu.display_menu()

