import src.GUI.Menu as libMenu


class MainMenu(libMenu.Menu):
    def __init__(self, game):
        libMenu.Menu.__init__(self, game)

        self.__state = "Start"
        self.__start_x: float = self.mid_w
        self.__start_y: float = self.mid_h + self.text_font_size
        self.__options_x: float = self.mid_w
        self.__options_y: float = self.mid_h + self.text_font_size * 2
        self.__credits_x: float = self.mid_w
        self.__credits_y: float = self.mid_h + self.text_font_size * 3
        self.__quit_x: float = self.mid_w
        self.__quit_y: float = self.mid_h + self.text_font_size * 4

        self.cursor_rect.midtop = (self.__start_x + self.offset, self.__start_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.get_display().fill(self.game.BLACK)
            self.game.draw_text('Main Menu', self.title_font_size, self.game.get_window_width() / 2,
                                self.game.get_window_height() / 2 - self.title_font_size)
            self.game.draw_text("Start Game", self.text_font_size, self.__start_x, self.__start_y)
            self.game.draw_text("Options", self.text_font_size, self.__options_x, self.__options_y)
            self.game.draw_text("Credits", self.text_font_size, self.__credits_x, self.__credits_y)
            self.game.draw_text("Exit", self.text_font_size, self.__quit_x, self.__quit_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.get_key_down():
            if self.__state == 'Start':
                self.cursor_rect.midtop = (self.__options_x + self.offset, self.__options_y)
                self.__state = 'Options'
            elif self.__state == 'Options':
                self.cursor_rect.midtop = (self.__credits_x + self.offset, self.__credits_y)
                self.__state = 'Credits'
            elif self.__state == 'Credits':
                self.cursor_rect.midtop = (self.__start_x + self.offset, self.__quit_y)
                self.__state = 'Exit'
            elif self.__state == 'Exit':
                self.cursor_rect.midtop = (self.__start_x + self.offset, self.__start_y)
                self.__state = 'Start'
        elif self.game.get_key_up():
            if self.__state == 'Start':
                self.cursor_rect.midtop = (self.__credits_x + self.offset, self.__credits_y)
                self.__state = 'Exit'
            elif self.__state == 'Options':
                self.cursor_rect.midtop = (self.__start_x + self.offset, self.__start_y)
                self.__state = 'Start'
            elif self.__state == 'Credits':
                self.cursor_rect.midtop = (self.__options_x + self.offset, self.__options_y)
                self.__state = 'Options'
            elif self.__state == 'Exit':
                self.cursor_rect.midtop = (self.__options_x + self.offset, self.__options_y)
                self.__state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.get_key_enter():
            if self.__state == 'Start':
                self.game.playing = False
            elif self.__state == 'Options':
                self.game.curr_menu = self.game.options
                self.game.curr_menu.display_menu()
            elif self.__state == 'Credits':
                self.game.curr_menu = self.game.credits
                self.game.curr_menu.display_menu()
            elif self.__state == 'Exit':
                self.game.playing = False

            self.run_display = False
