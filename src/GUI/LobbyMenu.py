import pygame.mouse

import src.GUI.Menu as libMenu
import src.GUI.Widgets.Button as libButton
import src.GUI.Widgets.TextInput as libTextInput

class LobbyMenu(libMenu.Menu):
    def __init__(self):
        pass

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('Lobby', self.title_font_size, self.game.get_window_width() / 2,
                                self.title_font_size * 3)

            for button in self.buttons:
                button.update(self.game.get_display(), self.mouse_pos)
            for text_input in self.text_input_array:
                text_input.update(self.game.get_display(), self.mouse_pos)

            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # TODO: make holding backspace delete more letters
                if event.key == pygame.K_ESCAPE:
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_menu.display_menu()
                    self.run_display = False
                else:
                    if pygame.key.name(event.key) in self.INPUT_KEYS | self.INPUT_LETTERS:
                        for text_input in self.text_input_array:
                            if text_input.is_clicked():
                                text_input.append_input(pygame.key.name(event.key))
                    elif event.key == pygame.K_BACKSPACE:
                        for text_input in self.text_input_array:
                            if text_input.is_clicked():
                                text_input.delete_last_input_letter()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons[0].cursor_hovers(self.mouse_pos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_menu.display_menu()
                elif self.buttons[1].cursor_hovers(self.mouse_pos):
                    # TODO: Create lobby
                    pass
                for text_input in self.text_input_array:
                    if text_input.cursor_hovers(self.mouse_pos):
                        text_input.set_clicked(True)
                    else:
                        text_input.set_clicked(False)
