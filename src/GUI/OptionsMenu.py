from src.GUI.Menu import Menu

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + self.text_font_size
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + self.text_font_size * 2
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', self.title_font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - self.title_font_size)
            self.game.draw_text("Volume", self.text_font_size, self.volx, self.voly)
            self.game.draw_text("Controls", self.text_font_size, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
            self.game.curr_menu.display_menu()
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.ENTER_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass