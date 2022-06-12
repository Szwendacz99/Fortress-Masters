from logging import error

import pygame.mouse

from game.team import Team
from gui.menu import Menu
from gui.widgets.button import Button
from gui.widgets.text_input import TextInput
from network.client import Client
from game.identity import Identity
from network.server import Server


class PlayMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.__lobby_display_players: list[Identity] = []

        self.__game_ready: bool = False

        # TODO: ?Make input manager class
        self.INPUT_LETTERS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.'}

        self.INPUT_KEYS = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

        self.buttons: list[Button] = []

        self.text_input_array: list[TextInput] = []

        self.connection_status: str = "not connected"
        self.connection_color: tuple = (220, 220, 200)

        self.resize()

    def resize(self):
        super().resize()

        self.buttons: list[Button] = [Button(pos=(self.game.get_window_width() / 2,
                                                  self.font_manager.title_font_size * 3),
                                             label_text="GO BACK",
                                             font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                             color="Red", hovering_color="Green"),
                                      Button(pos=(self.game.get_window_width() / 2,
                                                  self.font_manager.title_font_size * 7),
                                             label_text="Create lobby",
                                             font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                             color="WHITE", hovering_color="Green"),
                                      Button(pos=(self.game.get_window_width() / 2,
                                                  self.font_manager.title_font_size * 8),
                                             label_text="Join lobby",
                                             font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                             color="WHITE", hovering_color="Green"),
                                      Button(pos=(self.game.get_window_width() / 2,
                                                  self.font_manager.title_font_size * 9),
                                             label_text="Start game",
                                             font=self.game.get_font(self.font_manager.get_regular_font_size()),
                                             color="WHITE", hovering_color="Yellow", is_visible=False),
                                      Button(pos=(3 * self.game.get_window_width() / 4,
                                                  self.font_manager.title_font_size * 8),
                                             label_text="Demo",
                                             font=self.game.get_font(self.font_manager.get_regular_font_size() // 2),
                                             color="WHITE", hovering_color="Yellow", is_visible=True),
                                      ]

        self.text_input_array: list[TextInput] = [TextInput(pos=(self.mid_w, self.font_manager.title_font_size * 4),
                                                            font=self.game.get_font(
                                                                self.font_manager.get_regular_font_size()),
                                                            color="BLACK",
                                                            background_color="WHITE",
                                                            clicked_color="BLUE",
                                                            input_text="127.0.0.1",
                                                            input_label="ADDR: ",
                                                            input_label_color="WHITE"),
                                                  TextInput(pos=(self.mid_w, self.font_manager.title_font_size * 5),
                                                            font=self.game.get_font(
                                                                self.font_manager.get_regular_font_size()),
                                                            color="BLACK",
                                                            background_color="WHITE",
                                                            clicked_color="BLUE",
                                                            input_text="4401",
                                                            input_label="PORT: ",
                                                            input_label_color="WHITE"),

                                                  TextInput(pos=(self.mid_w, self.font_manager.title_font_size * 6),
                                                            font=self.game.get_font(
                                                                self.font_manager.get_regular_font_size()),
                                                            color="BLACK",
                                                            background_color="WHITE",
                                                            clicked_color="BLUE",
                                                            input_text="NICK",
                                                            input_label="NICK: ",
                                                            input_label_color="WHITE")
                                                  ]

    def display_menu(self):
        self.run_display = True
        clock = pygame.time.Clock()
        while self.run_display:
            clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('Lobby', self.font_manager.title_font_size, self.game.get_window_width() / 2,
                                self.font_manager.title_font_size * 2)

            self.game.draw_text('Connection status:', self.font_manager.regular_font_size,
                                self.game.get_window_width() / 8,
                                self.font_manager.title_font_size)

            if self.connection_status is not None:
                self.game.draw_text(self.connection_status, self.font_manager.regular_font_size,
                                    self.game.get_window_width() / 8,
                                    self.font_manager.title_font_size * 2,
                                    self.connection_color)

            if self.game.server is not None and self.game.server.is_alive():
                self.__lobby_display_players = self.game.server.get_lobby_list()
            elif self.game.client is not None:
                self.__lobby_display_players = self.game.client.get_lobby_list()

            if len(self.__lobby_display_players) > 0:
                blu_players: int = 0
                red_players: int = 0
                for player in self.__lobby_display_players:
                    if player.get_team() == Team.RED:
                        self.game.draw_text(player.get_username(), self.font_manager.get_title_font_size(),
                                            self.game.get_window_width() / 5,
                                            self.font_manager.get_title_font_size() * 5 + self.font_manager.get_title_font_size() * red_players,
                                            (255, 0, 0))
                        red_players += 1
                    else:
                        self.game.draw_text(player.get_username(), self.font_manager.get_title_font_size(),
                                            4 * self.game.get_window_width() / 5,
                                            self.font_manager.get_title_font_size() * 5 + self.font_manager.get_title_font_size() * blu_players,
                                            (0, 0, 255))
                        blu_players += 1

            if len(self.__lobby_display_players) == 4 and self.game.server is not None:
                self.buttons[3].set_visible(True)

            for button in self.buttons:
                button.update(self.game.get_display(), self.mouse_pos)
            for text_input in self.text_input_array:
                text_input.update(self.game.get_display(), self.mouse_pos)

            self.check_input()
            self.game.check_events()
            self.blit_screen()

            if self.__game_ready:
                self.start_game()

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
                    if self.game.server is not None and self.game.server.is_alive():
                        return
                    self.game.client = Client(self.game,
                                              username=self.text_input_array[2].input_text,
                                              is_server=True)
                    try:
                        self.game.server = Server(port=int(self.text_input_array[1].input_text),
                                                  identity=self.game.client.get_identity())
                    except OSError as e:
                        error(f"Cannot start server: {str(e)}")
                        # TODO gui inform that cannot start server because port is taken
                        self.game.server = None
                        self.connection_status = f"Cannot start server: {str(e)}"
                        self.connection_color = (255, 50, 0)
                        return
                    self.game.server.start()
                    success, status = self.game.client.join_server(address=self.text_input_array[0].input_text,
                                                                   port=int(self.text_input_array[1].input_text))
                    if not success:
                        self.game.client = None
                        self.connection_status = status
                        self.connection_color = (255, 50, 0)
                        return
                    self.connection_status = "created lobby"
                    self.connection_color = (0, 255, 0)
                elif self.buttons[2].cursor_hovers(self.mouse_pos):
                    # TODO: Join Lobby
                    self.game.client = Client(self.game,
                                              username=self.text_input_array[2].input_text)
                    success, status = self.game.client.join_server(address=self.text_input_array[0].input_text.strip(),
                                                                   port=int(self.text_input_array[1].input_text.strip()))
                    if not success:
                        self.game.client = None
                        self.connection_status = status
                        self.connection_color = (255, 50, 0)
                        return

                    self.connection_status = "joined lobby"
                    self.connection_color = (0, 255, 0)

                elif self.buttons[3].cursor_hovers(self.mouse_pos):
                    # TODO: Send message to other clients, that game has started. Temporarily it will start the game.
                    if len(self.__lobby_display_players) == 4:
                        self.game.server.start_game()
                        self.set_game_ready()
                elif self.buttons[4].cursor_hovers(self.mouse_pos):
                    # Demo start button
                    self.set_game_ready()
                for text_input in self.text_input_array:
                    if text_input.cursor_hovers(self.mouse_pos):
                        text_input.set_clicked(True)
                    else:
                        text_input.set_clicked(False)

    def start_game(self):
        Client.buildings.clear()
        Client.units.clear()
        Client.bullets.clear()
        self.run_display = False
        self.game.curr_menu = self.game.game_playing
        self.game.curr_menu.display_menu()

    def set_game_ready(self, ready: bool = True):
        self.__game_ready = ready
