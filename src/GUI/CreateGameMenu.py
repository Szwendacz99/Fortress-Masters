import pygame.mouse

import src.GUI.Menu as libMenu
import src.GUI.Widgets.Button as libButton
import src.GUI.Widgets.TextInput as libTextInput


class NewGameMenu(libMenu.Menu):
    def __init__(self, game):
        libMenu.Menu.__init__(self, game)

        self.INPUT_KEYS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

        self.back_button = libButton.Button(pos=(self.game.get_window_width() / 2,
                                                             self.title_font_size * 4),
                                            label_text="GO BACK", font=self.game.get_font(self.text_font_size),
                                            color="Red", hovering_color="Green")

        self.text_input_array = [libTextInput.TextInput(pos=(self.mid_w, self.title_font_size * 6),
                                                 font=self.game.get_font(self.text_font_size), color="BLACK", background_color="WHITE",
                                                 clicked_color="BLUE", input_label="PORT: ", input_label_color="WHITE"),

                                 libTextInput.TextInput(pos=(self.mid_w, self.title_font_size * 7),
                                                        font=self.game.get_font(self.text_font_size), color="BLACK",
                                                        background_color="WHITE",
                                                        clicked_color="BLUE", input_label="NICK: ",
                                                        input_label_color="WHITE")
                                 ]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('Lobby', self.title_font_size, self.game.get_window_width() / 2,
                                self.title_font_size * 3)

            self.back_button.update(self.game.get_display(), self.mouse_pos)
            for text_input in self.text_input_array:
                text_input.update(self.game.get_display(), self.mouse_pos)


            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # TODO: check if TextInput is clicked, and if it is append its' text or delete last letter if clicked button is backspace
                if event.key == pygame.K_ESCAPE:
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_menu.display_menu()
                    self.run_display = False
                else:
                    if pygame.key.name(event.key) in self.INPUT_KEYS:
                        for text_input in self.text_input_array:
                          if text_input.is_clicked():
                              text_input.append_input(pygame.key.name(event.key))
                    elif event.key == pygame.K_BACKSPACE:
                        for text_input in self.text_input_array:
                          if text_input.is_clicked():
                             text_input.delete_last_input_letter()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.cursor_hovers(self.mouse_pos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_menu.display_menu()
                for text_input in self.text_input_array:
                    if text_input.cursor_hovers(self.mouse_pos):
                        text_input.set_clicked(True)
                    else:
                        text_input.set_clicked(False)