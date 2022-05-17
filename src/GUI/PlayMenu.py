from logging import debug, error

import pygame.mouse

from GUI.Menu import Menu
from GUI.Widgets.Button import Button
from GUI.Widgets.TextInput import TextInput
from core.client import Client
from core.identity import Identity
from core.server import Server


class NewGameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.__client: Client = None
        self.__server: Server = None

        self.__lobby_display_players: list[Identity] = []

        # TODO: ?Make input manager class
        self.INPUT_LETTERS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.'}

        self.INPUT_KEYS = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

        self.buttons: list[Button] = [Button(pos=(self.game.get_window_width() / 2,
                                                  self.title_font_size * 4),
                                             label_text="GO BACK", font=self.game.get_font(self.text_font_size),
                                             color="Red", hovering_color="Green"),
                                      Button(pos=(self.game.get_window_width() / 2,
                                                  self.title_font_size * 9),
                                             label_text="Create lobby", font=self.game.get_font(self.text_font_size),
                                             color="WHITE", hovering_color="Green"),
                                      Button(pos=(self.game.get_window_width() / 2,
                                                  self.title_font_size * 10),
                                             label_text="Join lobby", font=self.game.get_font(self.text_font_size),
                                             color="WHITE", hovering_color="Green"),
                                      Button(pos=(self.game.get_window_width() / 2,
                                                  self.title_font_size * 11),
                                             label_text="Start game", font=self.game.get_font(self.text_font_size),
                                             color="WHITE", hovering_color="Yellow", is_visible=False),
                                      ]

        self.text_input_array: list[TextInput] = [TextInput(pos=(self.mid_w, self.title_font_size * 6),
                                                            font=self.game.get_font(self.text_font_size), color="BLACK",
                                                            background_color="WHITE",
                                                            clicked_color="BLUE",
                                                            input_text="127.0.0.1",
                                                            input_label="ADDR: ",
                                                            input_label_color="WHITE"),
                                                  TextInput(pos=(self.mid_w, self.title_font_size * 7),
                                                            font=self.game.get_font(self.text_font_size), color="BLACK",
                                                            background_color="WHITE",
                                                            clicked_color="BLUE",
                                                            input_text="4401",
                                                            input_label="PORT: ",
                                                            input_label_color="WHITE"),

                                                  TextInput(pos=(self.mid_w, self.title_font_size * 8),
                                                            font=self.game.get_font(self.text_font_size), color="BLACK",
                                                            background_color="WHITE",
                                                            clicked_color="BLUE",
                                                            input_text="NICK",
                                                            input_label="NICK: ",
                                                            input_label_color="WHITE")
                                                  ]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('Lobby', self.title_font_size, self.game.get_window_width() / 2,
                                self.title_font_size * 3)

            if self.__server is not None and self.__server.is_alive():
                self.__lobby_display_players = self.__server.get_lobby_list()
            elif self.__client is not None:
                self.__lobby_display_players = self.__client.get_lobby_list()

            if len(self.__lobby_display_players) > 0:
                for i in range(len(self.__lobby_display_players)):
                    if i < 2:
                        self.game.draw_text(self.__lobby_display_players[i].get_username(), self.title_font_size,
                                            self.game.get_window_width() / 4,
                                            self.title_font_size * 5 + self.title_font_size * i)
                    else:
                        self.game.draw_text(self.__lobby_display_players[i].get_username(), self.title_font_size,
                                            3 * self.game.get_window_width() / 4,
                                            self.title_font_size * 3 + self.title_font_size * i)

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
                    if self.__server is not None and self.__server.is_alive():
                        return
                    self.__client = Client(username=self.text_input_array[2].input_text)
                    try:
                        self.__server = Server(port=int(self.text_input_array[1].input_text),
                                               identity=self.__client.get_identity())
                    except OSError as e:
                        error(f"Cannot start server: {str(e)}")
                        # TODO GUI inform that cannot start server because port is taken
                        self.__server = None
                        return
                    self.__server.start()
                    success: bool = self.__client.join_server(address=self.text_input_array[0].input_text,
                                                              port=int(self.text_input_array[1].input_text))
                    if not success:
                        self.__client = None
                    self.buttons[3].set_visible(True)
                elif self.buttons[2].cursor_hovers(self.mouse_pos):
                    # TODO: Join Lobby
                    self.__client = Client(username=self.text_input_array[2].input_text)
                    success: bool = self.__client.join_server(address=self.text_input_array[0].input_text,
                                                              port=int(self.text_input_array[1].input_text))
                    if not success:
                        self.__client = None

                elif self.buttons[3].cursor_hovers(self.mouse_pos):
                    # TODO: Send message to other clients, that game has started. Temporarily it will start the game.
                    self.__server.start_game()
                    if len(self.__lobby_display_players) == 4:
                        self.run_display = False
                        self.game.curr_menu = self.game.game_playing
                        self.game.curr_menu.display_menu()
                for text_input in self.text_input_array:
                    if text_input.cursor_hovers(self.mouse_pos):
                        text_input.set_clicked(True)
                    else:
                        text_input.set_clicked(False)
