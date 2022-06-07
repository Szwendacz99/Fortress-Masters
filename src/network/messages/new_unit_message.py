from uuid import UUID

from pygame.math import Vector2

from core.team import Team
from game.units.unit_type import UnitType
from game.units.unit import Unit
from game.units.spaceship import Spaceship
from game.units.spaceship_1 import Spaceship_1
from game.units.spaceship_2 import Spaceship_2
from game.units.spaceship_3 import Spaceship_3
from game.units.spaceship_4 import Spaceship_4
from game.units.spaceship_5 import Spaceship_5
from game.units.spaceship_6 import Spaceship_6

from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class NewUnitMessage(BasicMessage):
    def __init__(self, uuid: UUID, unit_type_class: Unit, pos: (int, int), team: Team):
        BasicMessage.__init__(self, msg_type=MessageType.NEW_UNIT)
        self.unit_type_class: Unit = unit_type_class
        self.pos: Vector2 = pos
        self.team: Team = team
        self.uuid = uuid
