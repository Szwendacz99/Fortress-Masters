from src.GUI.Menu import Menu


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + self.text_font_size
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + self.text_font_size * 2
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + self.text_font_size * 3
        self.quitx, self.quity = self.mid_w, self.mid_h + self.text_font_size * 4

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', self.title_font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - self.title_font_size)
            self.game.draw_text("Start Game", self.text_font_size, self.startx, self.starty)
            self.game.draw_text("Options", self.text_font_size, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", self.text_font_size, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", self.text_font_size, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.quity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.quity)
                self.state = 'Exit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == 'Start':
                self.game.playing = False
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
                self.game.curr_menu.display_menu()
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
                self.game.curr_menu.display_menu()
            elif self.state == 'Exit':
                self.game.playing = False

            self.run_display = False