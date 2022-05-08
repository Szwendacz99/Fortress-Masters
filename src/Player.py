# TODO: Implement class Player
from core.identity import Identity
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.join_ack_message import JoinAckMessage


class Player:
    def __init__(self, identity: Identity):
        self.__identity: Identity = identity
        self.__connection: [Connection] = None

    def get_name(self) -> str:
        return self.__identity.get_name()

    def set_connection(self, conn: Connection):
        self.__connection: Connection = conn

    def send_message(self, msg: [BasicMessage, JoinAckMessage]):
        self.__connection.send_data(msg)

    def get_identity(self) -> Identity:
        return self.__identity
