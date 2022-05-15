from logging import error
from threading import Thread
from time import time

from core.identity import Identity
from core.message_receiver import MessageReceiver
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage


class ConnectedPlayer(Thread):
    def __init__(self, identity: Identity, msg_receiver: MessageReceiver):
        Thread.__init__(self)
        self.__identity: Identity = identity
        self.__connection: Connection = None
        self.__message_receiver: MessageReceiver = msg_receiver
        self.__last_msg_receive_time: float = time()

    def get_name(self) -> str:
        return self.__identity.get_username()

    def set_connection(self, conn: Connection):
        self.__connection: Connection = conn

    def send_message(self, msg: [BasicMessage, LobbyStateMessage]):
        self.__connection.send_data(msg)

    def get_identity(self) -> Identity:
        return self.__identity

    def get_last_msg_receive_time(self) -> float:
        return self.__last_msg_receive_time

    def run(self) -> None:
        while self.__connection.is_alive():
            try:
                self.__message_receiver.receive(self.__connection.receive_data())
            except:
                error("Lost connection with server!")
                self.__connection.disconnect()
            self.__last_msg_receive_time = time()

    def disconnect(self):
        self.__connection.disconnect()
