from uuid import UUID

from core.team import Team
from game.units.unit import Unit
from game.rocket import Rocket
from game.laser import Laser


class Bunker(Unit):
    path_blue = 'resources/img/bunker_blue.png'
    path_red = 'resources/img/bunker_red.png'
    path_blue_dead = 'resources/img/bunker_blue_dead.png'
    path_red_dead = 'resources/img/bunker_red_dead.png'

    # Name of the class of the bullets that this unit will attack with
    bullet_type = Laser
    unit_size = 75
    cost = 70

    def __init__(self, uuid: UUID, game, start_pos,
                 hp: int = 666, atk_damage: int = 26, atk_speed: int = 125, atk_range: int = 150, speed: float = 0.0,
                 team: Team = Team.RED, left: bool = True, client_team: Team = Team.RED):
        Unit.__init__(self, uuid, game, start_pos, hp, atk_damage, atk_speed, atk_range, speed, team, client_team, left,
                      self.path_blue, self.path_red, self.path_blue_dead, self.path_red_dead,
                      self.unit_size, self.bullet_type)
        self.uuid = uuid
