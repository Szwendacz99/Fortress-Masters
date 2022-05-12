from logging import debug, info
from threading import Thread

from core.lobby import Lobby
from core.identity import Identity
from core.message_receiver import MessageReceiver
from core.player import Player
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.join_message import JoinMessage
from network.messages.message_type import MessageType
from network.server_listener import ServerListener


class Server(Thread, MessageReceiver):

    def __init__(self, port: int):
        super().__init__()
        self.__listener: ServerListener = ServerListener(port, 3)
        self.__lobby: Lobby = Lobby()
        self.__lobby.start()
        self.__lobby_mode: bool = True

    def run(self):
        info(f"Started server on port {self.__listener.get_port()}")
        while self.__lobby_mode:
            new_conn: Connection = self.__listener.receive_connection()
            debug(f"Received connection from {new_conn.get_peer()}")
            msg: [BasicMessage, JoinMessage] = new_conn.receive_data()
            if msg.get_type() == MessageType.JOIN:
                msg: JoinMessage = msg
                self.add_new_player(conn=new_conn, identity=msg.get_identity())

    def add_new_player(self, conn: Connection, identity: Identity):
        """
        Add new player to lobby list
        :param conn: connection with the plater
        :param identity: identity received from this plater
        :return:
        """
        player = Player(identity, self)
        player.set_connection(conn)
        if not self.__lobby.add_player(player):
            msg = BasicMessage(MessageType.LOBBY_FULL)
            player.send_message(msg)
            player.remove()
        self.__lobby.broadcast(LobbyStateMessage(self.__lobby.get_identities()))
        info(f"Player {player.get_name()} has successfully joined the lobby!")

    def receive(self, message: BasicMessage) -> bool:
        debug("Server received mesage")
        return True
