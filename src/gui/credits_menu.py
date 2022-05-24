import pygame

from gui.menu import Menu
from gui.widgets.button import Button


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.__c1x: float = 0
        self.__c1y: float = 0
        self.__c2x: float = 0
        self.__c2y: float = 0
        self.__c3x: float = 0
        self.__c3y: float = 0

        self.back_button = None

        self.resize()

    def resize(self):


        super().resize()

        self.__c1x: float = self.mid_w
        self.__c1y: float = self.mid_h + self.font_manager.get_regular_font_size()
        self.__c2x: float = self.mid_w
        self.__c2y: float = self.mid_h + self.font_manager.get_regular_font_size() * 2
        self.__c3x: float = self.mid_w
        self.__c3y: float = self.mid_h + self.font_manager.get_regular_font_size() * 3

        self.back_button = Button(pos=(self.game.get_window_width() / 2,
                                       self.game.get_window_height() / 2 - self.font_manager.get_title_font_size()),
                                  label_text="GO BACK", font=self.game.get_font(self.font_manager.get_title_font_size()),
                                  color="Red", hovering_color="Green")


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mouse_pos = pygame.mouse.get_pos()
            self.game.get_display().fill(self.game.BLACK)

            self.game.draw_text('CREDITS', self.font_manager.get_title_font_size(), self.game.get_window_width() / 2,
                                self.game.get_window_height() / 2 - self.font_manager.get_title_font_size() * 2)

            self.back_button.update(self.game.get_display(), self.mouse_pos)

            self.game.draw_text('Przemyslaw Marek', self.font_manager.get_regular_font_size(), self.__c1x, self.__c1y)
            self.game.draw_text('Maciej Lebiest', self.font_manager.get_regular_font_size(), self.__c2x, self.__c2y)
            self.game.draw_text('Szymon Mazur', self.font_manager.get_regular_font_size(), self.__c3x, self.__c3y)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.cursor_hovers(self.mouse_pos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
                    self.game.curr_menu.display_menu()
