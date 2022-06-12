from game.identity import Identity
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class JoinMessage(BasicMessage):
    def __init__(self, identity: Identity):
        BasicMessage.__init__(self, msg_type=MessageType.JOIN)
        self.__identity: Identity = identity

    def get_identity(self) -> Identity:
        return self.__identity
