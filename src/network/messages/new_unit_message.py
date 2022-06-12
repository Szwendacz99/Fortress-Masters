from uuid import UUID

from pygame.math import Vector2

from game.team import Team
from game.units.unit import Unit

from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class NewUnitMessage(BasicMessage):
    def __init__(self, uuid: UUID, unit_type_class: Unit, pos: (int, int), team: Team):
        BasicMessage.__init__(self, msg_type=MessageType.NEW_UNIT)
        self.unit_type_class: Unit = unit_type_class
        self.pos: Vector2 = pos
        self.team: Team = team
        self.uuid = uuid
