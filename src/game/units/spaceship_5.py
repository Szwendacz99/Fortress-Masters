from uuid import UUID

from core.team import Team
from game.units.unit import Unit
from game.rocket import Rocket


class Spaceship_5(Unit):
    path_blue = 'resources/img/Spaceship_pack_pack_05_BLUE.png'
    path_red = 'resources/img/Spaceship_pack_pack_05_RED.png'
    path_blue_dead = 'resources/img/Spaceship_pack_pack_05_BLUE-dead.png'
    path_red_dead = 'resources/img/Spaceship_pack_pack_05_RED-dead.png'

    # Name of the class of the bullets that this unit will attack with
    bullet_type = Rocket
    unit_size = 45

    def __init__(self, uuid: UUID, game, start_pos,
                 hp: int = 400, atk_damage: int = 40, atk_speed: int = 150, atk_range: int = 110, speed: float = 0.30,
                 team: Team = Team.RED, left: bool = True, client_team: Team = Team.RED):
        Unit.__init__(self, uuid, game, start_pos, hp, atk_damage, atk_speed, atk_range, speed, team, client_team, left,
                      self.path_blue, self.path_red, self.path_blue_dead, self.path_red_dead,
                      self.unit_size, self.bullet_type)
        self.uuid = uuid
