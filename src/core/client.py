from logging import debug, info, error
from threading import Thread
from time import time

from core.identity import Identity
from exceptions.network_exception import NetworkException
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.join_message import JoinMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType


class Client(Thread):
    def __init__(self, username: str):
        Thread.__init__(self)
        self.lobby_list: list[Identity] = []
        self.__game_started: bool = False

        self.__identity: Identity = Identity(username)
        self.__connection: Connection = None
        self.__last_msg_receive_time: float = time()
        self.daemon = True

    def join_server(self, address: str, port: int) -> bool:
        try:
            conn: Connection = Connection(address=address,
                                          port=port,
                                          timeout=5)
            conn.send_data(JoinMessage(self.get_identity()))
            self.__connection = conn
            self.start()
            return True
        except:
            return False

    def receive(self, message) -> bool:

        # debug("Client received message")
        if message.get_type() == MessageType.LOBBY_STATE:
            message: LobbyStateMessage = message
            debug(f"Client received lobby list: {[p.get_username() for p in message.get_players()]}")
            self.lobby_list = message.get_players()
        elif message.get_type() == MessageType.HEARTBEAT:
            self.send_message(message)
        elif message.get_type() == MessageType.GAME_START:
            info("Received info on game start!")
        elif message.get_type == MessageType.TEAM_SET:
            self.__identity.set_team(message.get_team())
            info(f"Assigned to team {message.get_team()}")
        return True

    def get_identity(self) -> Identity:
        return self.__identity

    def get_lobby_list(self) -> list[Identity]:
        return self.lobby_list

    def send_message(self, msg: [BasicMessage, LobbyStateMessage]):
        self.__connection.send_data(msg)

    def get_last_msg_receive_time(self) -> float:
        return self.__last_msg_receive_time

    def run(self) -> None:
        while self.__connection.is_alive():
            try:
                self.receive(self.__connection.receive_data())
            except Exception as e:
                error(f"Lost connection with server: {str(e)}")
                self.__connection.disconnect()
            self.__last_msg_receive_time = time()

    def disconnect(self):
        self.__connection.disconnect()
