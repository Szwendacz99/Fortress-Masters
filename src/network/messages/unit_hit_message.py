from uuid import UUID

from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class UnitHitMessage(BasicMessage):
    def __init__(self, uuid: UUID, damage: int):
        BasicMessage.__init__(self, msg_type=MessageType.UNIT_HIT)
        self.uuid: UUID = uuid
        self.damage = damage
