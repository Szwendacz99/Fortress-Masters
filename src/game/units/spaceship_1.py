from uuid import UUID

from core.team import Team
from game.units.unit import Unit
from game.rocket import Rocket


class Spaceship_1(Unit):
    path_blue = 'resources/img/ship_blue1.png'
    path_red = 'resources/img/ship_red1.png'
    path_blue_dead = 'resources/img/ship_blue_dead1.png'
    path_red_dead = 'resources/img/ship_red_dead1.png'

    # Name of the class of the bullets that this unit will attack with
    bullet_type = Rocket
    unit_size = 55
    cost: int = 20

    def __init__(self, uuid: UUID, game, start_pos,
                 hp: int = 300, atk_damage: int = 30, atk_speed: int = 200, atk_range: int = 100, speed: float = 0.25,
                 team: Team = Team.RED, left: bool = True, client_team: Team = Team.RED):
        Unit.__init__(self, uuid, game, start_pos, hp, atk_damage, atk_speed, atk_range, speed, team, client_team, left,
                      self.path_blue, self.path_red, self.path_blue_dead, self.path_red_dead,
                      self.unit_size, self.bullet_type)
        self.uuid = uuid
