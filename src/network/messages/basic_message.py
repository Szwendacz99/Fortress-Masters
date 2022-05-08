from abc import ABC

from network.messages.message_type import MessageType


class BasicMessage(ABC):
    def __init__(self, msg_type: MessageType):
        super().__init__()
        self._message_type: MessageType = msg_type

    def get_type(self) -> MessageType:
        return self._message_type
