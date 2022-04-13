from src.GUI.Menu import Menu

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.c1x, self.c1y = self.mid_w, self.mid_h + self.text_font_size
        self.c2x, self.c2y = self.mid_w, self.mid_h + self.text_font_size * 2
        self.c3x, self.c3y = self.mid_w, self.mid_h + self.text_font_size * 3

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))

            self.game.draw_text('CREDITS', self.title_font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - self.title_font_size)
            self.game.draw_text('Szymon Mazur', self.text_font_size, self.c1x, self.c1y)
            self.game.draw_text('Maciej Lebiest', self.text_font_size, self.c2x, self.c2y)
            self.game.draw_text('Przemyslaw Marek', self.text_font_size, self.c3x, self.c3y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
            self.game.curr_menu.display_menu()