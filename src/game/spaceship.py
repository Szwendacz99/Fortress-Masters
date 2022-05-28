from game.unit import Unit
from game.rocket import Rocket
from game.laser import Laser


class Spaceship(Unit):
    path_blue = 'resources/img/ship_blue.png'
    path_red = 'resources/img/ship_red.png'
    path_blue_dead = 'resources/img/ship_blue_dead.png'
    path_red_dead = 'resources/img/ship_red_dead.png'

    unit_size = 45
    # Name of the class of the bullets that this unit will attack with
    bullet_type = Rocket

    def __init__(self, game, start_pos, speed: float = 0.22, atk_range: int = 100, team: int = 0, left: bool = True):
        Unit.__init__(self, game, start_pos, speed, atk_range, team, left,
                      self.path_blue, self.path_red, self.path_blue_dead, self.path_red_dead,
                      self.unit_size, self.bullet_type)
