from uuid import UUID

from pygame.math import Vector2

from core.team import Team
from game.units.unit_type import UnitType
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class NewUnitMessage(BasicMessage):
    def __init__(self, uuid: UUID, unit_type: UnitType, pos: (int, int), team: Team):
        BasicMessage.__init__(self, msg_type=MessageType.NEW_UNIT)
        self.unit_type: UnitType = unit_type
        self.pos: Vector2 = pos
        self.team: Team = team
        self.uuid = uuid
