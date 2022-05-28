from game.bullet import Bullet


class Rocket(Bullet):
    path_blue = 'resources/img/rocket_blue.png'
    path_red = 'resources/img/rocket_red.png'

    def __init__(self, game, start_pos, target, damage, speed: float = 1.66, team: int = 0):
        Bullet.__init__(self, game, start_pos, target, damage, self.path_blue, self.path_red, speed, team,
                        img_size_x=11, img_size_y=11)
