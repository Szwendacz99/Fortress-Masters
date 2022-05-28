from uuid import UUID

from core.identity import Identity
from core.team import Team
from game.unit import Unit
from game.unit_type import UnitType
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class NewUnitMessage(BasicMessage):
    def __init__(self, uuid: UUID, unit_type: UnitType, pos: (int, int), team: Team):
        BasicMessage.__init__(self, msg_type=MessageType.NEW_UNIT)
        self.unit_type = unit_type
        self.pos: (int, int) = pos
        self.team: Team = team
        self.uuid = uuid
