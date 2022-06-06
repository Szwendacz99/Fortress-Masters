from game.player_info_label import PlayerInfoLabel


class PlayerStatusBar:

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.__info_labels: list = []

        self.__create_player_bar()

    def __create_player_bar(self):
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y, self.game.get_font(14), "Player status"))
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y + 32, self.game.get_font(14), "Currency: "))
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y + 2 * 32, self.game.get_font(14), "Big tower HP %: "))
        self.__info_labels.append(PlayerInfoLabel(self.x, self.y + 3 * 32, self.game.get_font(14), "Little tower HP %: "))
        pass

    def update(self, currency, big_tower_hp, little_tower_hp):
        self.__info_labels[0].update(self.game.get_display())
        self.__info_labels[1].update(self.game.get_display(), currency)
        self.__info_labels[2].update(self.game.get_display(), big_tower_hp)
        self.__info_labels[3].update(self.game.get_display(), little_tower_hp)

    def resize(self):
        for button in self.__info_labels:
            button.resize(self.game.get_display())
