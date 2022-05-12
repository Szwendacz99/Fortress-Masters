from logging import debug

from core.message_receiver import MessageReceiver
from core.player import Player
from core.identity import Identity
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.join_message import JoinMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType


class Client(MessageReceiver):
    def __init__(self, username: str):
        self.__player: Player = Player(identity=Identity(username), msg_receiver=self)
        self.lobby_list: list[Identity] = None

    def join_server(self, address: str, port: int):
        conn: Connection = Connection(address=address,
                                      port=port,
                                      timeout=5)
        conn.send_data(JoinMessage(self.__player.get_identity()))
        self.__player.set_connection(conn)
        self.__player.start()

    def receive(self, message) -> bool:
        debug("Client received mesage")
        if message.get_type() == MessageType.LOBBY_STATE:
            message: LobbyStateMessage = message
            debug(f"Client received lobby list: {[p.get_username() for p in message.get_players()]}")
            self.lobby_list = message.get_players()
        elif message.get_type() == MessageType.HEARTBEAT:
            self.__player.send_message(message)
        return True

    def get_lobby_list(self) -> list[Identity]:
        return self.lobby_list


