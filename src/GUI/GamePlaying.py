import pygame
import pygame.mouse
import os

from pygame.rect import Rect
from pygame.surface import Surface

import src.GUI.Menu as libMenu
import src.GUI.Widgets.Button as libButton


class GamePlaying(libMenu.Menu):
    def __init__(self, game):
        libMenu.Menu.__init__(self, game)
        self.__fps: int = 60
        self.__background_img: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('../resources/img/map_bg.png')), (564, self.game.get_window_height()))
        self.__x0: int = self.mid_w - self.__background_img.get_width()//2

        self.__red_turret: Surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.normpath('../resources/img/red_turret.png')), (120, 120)), 180)
        self.__blue_turret: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('../resources/img/blue_turret.png')), (120, 120))
        self.__small_red_turret: Surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.normpath('../resources/img/red_turret.png')), (100, 100)), 180)
        self.__small_blue_turret: Surface = pygame.transform.scale(pygame.image.load(
            os.path.normpath('../resources/img/blue_turret.png')), (100, 100))

        self.__blue_turret_left: Rect = pygame.Rect(
            self.__x0 + 220 - self.__blue_turret.get_width()//2,
            self.h(840),
            self.__blue_turret.get_width(), self.__blue_turret.get_height())
        self.__blue_turret_right: Rect = pygame.Rect(
            self.mid_w + (self.mid_w - (self.__x0 + 220 + self.__blue_turret.get_width() // 2)),
            self.h(840),
            self.__blue_turret.get_width(), self.__blue_turret.get_height())
        self.__red_turret_left: Rect = pygame.Rect(
            self.__x0 + 220 - self.__red_turret.get_width() // 2,
            self.h(20),
            self.__red_turret.get_width(), self.__red_turret.get_height())
        self.__red_turret_right: Rect = pygame.Rect(
            self.mid_w + (self.mid_w - (self.__x0 + 220 + self.__red_turret.get_width() // 2)),
            self.h(20),
            self.__red_turret.get_width(), self.__red_turret.get_height())

        self.__small_blue_turret_left: Rect = pygame.Rect(
            self.__x0 + 120 - self.__small_blue_turret.get_width() // 2,
            self.h(740),
            self.__small_blue_turret.get_width(), self.__small_blue_turret.get_height())
        self.__small_blue_turret_right: Rect = pygame.Rect(
            self.mid_w + (self.mid_w - (self.__x0 + 120 + self.__small_blue_turret.get_width() // 2)),
            self.h(740),
            self.__small_blue_turret.get_width(), self.__small_blue_turret.get_height())
        self.__small_red_turret_left: Rect = pygame.Rect(
            self.__x0 + 120 - self.__small_red_turret.get_width() // 2,
            self.h(147),
            self.__small_red_turret.get_width(), self.__small_red_turret.get_height())
        self.__small_red_turret_right: Rect = pygame.Rect(
            self.mid_w + (self.mid_w - (self.__x0 + 120 + self.__small_red_turret.get_width() // 2)),
            self.h(147),
            self.__small_red_turret.get_width(), self.__small_red_turret.get_height())

    def display_menu(self):
        clock = pygame.time.Clock()
        self.run_display = True
        while self.run_display:
            clock.tick(self.__fps)
            self.draw()
            self.check_input()
            self.game.check_events()
            self.blit_screen()

    def draw(self):
        self.game.get_display().blit(self.__background_img,
                                     (self.mid_w - self.__background_img.get_width() // 2, 0))

        self.game.get_display().blit(self.__blue_turret,
                                     (self.__blue_turret_left.x, self.__blue_turret_left.y))
        self.game.get_display().blit(self.__blue_turret,
                                     (self.__blue_turret_right.x, self.__blue_turret_right.y))
        self.game.get_display().blit(self.__red_turret,
                                     (self.__red_turret_left.x, self.__red_turret_left.y))
        self.game.get_display().blit(self.__red_turret,
                                     (self.__red_turret_right.x, self.__red_turret_right.y))

        self.game.get_display().blit(self.__small_blue_turret,
                                     (self.__small_blue_turret_left.x, self.__small_blue_turret_left.y))
        self.game.get_display().blit(self.__small_blue_turret,
                                     (self.__small_blue_turret_right.x, self.__small_blue_turret_right.y))
        self.game.get_display().blit(self.__small_red_turret,
                                     (self.__small_red_turret_left.x, self.__small_red_turret_left.y))
        self.game.get_display().blit(self.__small_red_turret,
                                     (self.__small_red_turret_right.x, self.__small_red_turret_right.y))

        # print(self.__small_red_turret_left.y + self.__small_red_turret.get_height(),
        # self.__small_blue_turret_left.y, self.game.get_window_height())

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

    # Normalizes given height to match the background scaled down to user's screen
    def h(self, h: int):
        return int(h/1002 * self.game.get_window_height())
