import pygame
from pygame.surface import Surface

from src.GUI.CreditsMenu import CreditsMenu
from src.GUI.MainMenu import MainMenu
from src.GUI.Menu import Menu
from src.GUI.OptionsMenu import OptionsMenu


class Game:
    def __init__(self):
        pygame.init()
        self.__running: bool = True
        self.__playing: bool = False
        self.__ready: bool = False
        self.__key_up: bool = False
        self.__key_down: bool = False
        self.__key_enter: bool = False
        self.__key_back: bool = False
        self.__window_width: int = pygame.display.Info().current_w
        self.__window_height: int = pygame.display.Info().current_h
        self.__display: Surface = pygame.Surface((self.__window_width, self.__window_height))
        self.__window: Surface = pygame.display.set_mode((self.__window_width, self.__window_height))
        self.__font_name: str = '../resources/fonts/8-BIT WONDER.TTF'

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        pygame.mouse.set_visible(False)

        self.main_menu: MainMenu = MainMenu(self)
        self.options: OptionsMenu = OptionsMenu(self)
        self.credits: CreditsMenu = CreditsMenu(self)
        self.curr_menu: Menu = self.main_menu

    def game_loop(self):
        # TODO: Implement game window
        pygame.mouse.set_visible(True)
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                self.__playing = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.__key_enter = True
                if event.key == pygame.K_ESCAPE:
                    self.__key_back = True
                if event.key == pygame.K_DOWN:
                    self.__key_down = True
                if event.key == pygame.K_UP:
                    self.__key_up = True

    def reset_keys(self):
        self.__key_up = False
        self.__key_down = False
        self.__key_enter = False
        self.__key_back = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.__font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.__display.blit(text_surface, text_rect)

    def get_window_width(self) -> int:
        return self.__window_width

    def get_window_height(self) -> int:
        return self.__window_height

    def get_display(self) -> Surface:
        return self.__display

    def get_window(self) -> Surface:
        return self.__window

    def get_key_back(self) -> bool:
        return self.__key_back

    def get_key_down(self) -> bool:
        return self.__key_down

    def get_key_up(self) -> bool:
        return self.__key_up

    def get_key_enter(self) -> bool:
        return self.__key_enter
