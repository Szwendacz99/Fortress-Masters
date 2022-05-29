from uuid import UUID

from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class UnitDeathMessage(BasicMessage):
    def __init__(self, uuid: UUID):
        BasicMessage.__init__(self, msg_type=MessageType.UNIT_DEATH)
        self.uuid: UUID = uuid
