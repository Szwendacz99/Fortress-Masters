import sys
from logging import info
from time import time

import pygame
from pygame.surface import Surface

from network.client import Client
from network.server import Server
from gui.credits_menu import CreditsMenu
from gui.play_menu import PlayMenu
from gui.main_menu import MainMenu
from gui.menu import Menu
from gui.game_playing import GamePlaying
from gui.game_end_menu import GameEndMenu
from utils.font_manager import FontManager


class GameWindow:
    menus: list[Menu] = []

    def __init__(self):
        pygame.init()
        self.__running: bool = True
        self.__playing: bool = False

        self.client: Client = None
        self.server: Server = None

        self.team_won = None

        self.__last_resize_time = 0

        self.__window_width: int = pygame.display.Info().current_w // 1.6
        self.__window_height: int = pygame.display.Info().current_h // 1.6
        self.__display: Surface = pygame.display.set_mode((self.__window_width, self.__window_height), pygame.RESIZABLE)
        # self.__font_name: str = '../resources/fonts/8-BIT WONDER.TTF'

        # TODO: Refactor fonts
        self.font_manager: FontManager = FontManager(
            font_path='resources/fonts/JUNGLE_ADVENTURER/JungleAdventurer.ttf')

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        pygame.mouse.set_visible(True)

        self.main_menu: MainMenu = MainMenu(self)
        self.menus.append(self.main_menu)
        self.credits: CreditsMenu = CreditsMenu(self)
        self.menus.append(self.credits)
        self.play_menu: PlayMenu = PlayMenu(self)
        self.menus.append(self.play_menu)
        self.game_playing: GamePlaying = GamePlaying(self)
        self.menus.append(self.game_playing)
        self.game_end: GameEndMenu = GameEndMenu(self)
        self.menus.append(self.game_end)

        self.curr_menu: Menu = self.main_menu

    def check_events(self):

        if time() - self.__last_resize_time > 0.5 and \
                (self.__window_width != pygame.display.Info().current_w or
                 self.__window_height != pygame.display.Info().current_h):
            self.__window_width = pygame.display.Info().current_w
            self.__window_height = pygame.display.Info().current_h
            self.__display = pygame.display.set_mode((self.__window_width, self.__window_height), pygame.RESIZABLE)
            self.__last_resize_time = time()
            for menu in self.menus:
                menu.resize()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                self.__playing = False
                self.curr_menu.run_display = False

                # TODO end all threads on exit
                info("Exiting game...")
                pygame.quit()
                sys.exit(0)

    def resize(self):
        pass

    def draw_text(self, text, size, x, y, color=(255,255,255)):
        font = pygame.font.Font(self.font_manager.font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.__display.blit(text_surface, text_rect)

    def get_font(self, size) -> pygame.font.Font:
        return pygame.font.Font(self.font_manager.font_path, size)

    def get_window_width(self) -> int:
        return self.__window_width

    def get_window_height(self) -> int:
        return self.__window_height

    def get_display(self) -> Surface:
        return self.__display

    def set_running(self, __running):
        self.__running = __running

    def set_playing(self, __playing):
        self.__playing = __playing

    def get_team_won(self):
        return self.team_won
