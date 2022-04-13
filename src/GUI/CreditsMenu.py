import src.GUI.Menu as libMenu


class CreditsMenu(libMenu.Menu):
    def __init__(self, game):
        libMenu.Menu.__init__(self, game)

        self.__c1x: float = self.mid_w
        self.__c1y: float = self.mid_h + self.text_font_size
        self.__c2x: float = self.mid_w
        self.__c2y: float = self.mid_h + self.text_font_size * 2
        self.__c3x: float = self.mid_w
        self.__c3y: float = self.mid_h + self.text_font_size * 3

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.get_display().fill((0, 0, 0))

            self.game.draw_text('CREDITS', self.title_font_size, self.game.get_window_width() / 2,
                                self.game.get_window_height() / 2 - self.title_font_size)
            self.game.draw_text('Szymon Mazur', self.text_font_size, self.__c1x, self.__c1y)
            self.game.draw_text('Maciej Lebiest', self.text_font_size, self.__c2x, self.__c2y)
            self.game.draw_text('Przemyslaw Marek', self.text_font_size, self.__c3x, self.__c3y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.get_key_back():
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
            self.game.curr_menu.display_menu()
