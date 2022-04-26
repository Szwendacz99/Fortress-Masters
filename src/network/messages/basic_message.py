from abc import ABC

from src.core.identity import Identity
from src.network.messages.message_type import MessageType


class BasicMessage(ABC, Identity):
    def __init__(self, msg_type: MessageType):
        super().__init__()
        self._message_type: MessageType = msg_type

    def get_type(self) -> MessageType:
        return self._message_type
