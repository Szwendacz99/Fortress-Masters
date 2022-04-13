import pygame

from src.GUI.CreditsMenu import CreditsMenu
from src.GUI.MainMenu import MainMenu
from src.GUI.OptionsMenu import OptionsMenu


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.readyToPlay = False
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = '../resources/fonts/8-BIT WONDER.TTF'

        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        pygame.mouse.set_visible(False)

        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        #TODO: Implement game window
        pygame.mouse.set_visible(True)
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
