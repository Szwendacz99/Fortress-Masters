from game.player_info_label import PlayerInfoLabel


class PlayerStatusBar:
    default_width: int = 1536
    default_height: int = 864

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.__info_labels: list = []

        self.__create_player_bar()

    def __create_player_bar(self):
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y, self.game.get_font(20), "Info of "))
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y + 32, self.game.get_font(20), "Currency: "))
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y + 2 * 32, self.game.get_font(20), "Big tower HP %: "))
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y + 3 * 32, self.game.get_font(20), "Little tower HP %: "))
        pass

    def update(self, currency, big_tower_hp, little_tower_hp, username):
        self.__info_labels[0].update(self.game.get_display(), username)
        self.__info_labels[1].update(self.game.get_display(), currency)
        self.__info_labels[2].update(self.game.get_display(), big_tower_hp)
        self.__info_labels[3].update(self.game.get_display(), little_tower_hp)

    def resize(self):
        for button in self.__info_labels:
            button.resize(self.game.get_display(), self.game)

    def h(self, h: int):
        return int(h / self.default_height * self.game.get_window_height())

    def w(self, w: int):
        return int(w / self.default_width * self.game.get_window_width())