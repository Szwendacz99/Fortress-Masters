from logging import debug, info
from threading import Thread

from core.server_game_thread import ServerGameThread
from core.identity import Identity
from core.message_receiver import MessageReceiver
from core.connected_player import ConnectedPlayer
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.join_message import JoinMessage
from network.messages.message_type import MessageType
from network.server_listener import ServerListener


class Server(Thread, MessageReceiver):

    def __init__(self, port: int, identity: Identity):
        super().__init__()
        self.__listener: ServerListener = ServerListener(port, 3)
        self.__server_game_thread: ServerGameThread = ServerGameThread()
        self.__server_game_thread.start()
        self.__identity = identity
        self.__team_blu: list[ConnectedPlayer] = []
        self.__team_red: list[ConnectedPlayer] = []

    def run(self):
        info(f"Started server lobby on port {self.__listener.get_port()}")
        while self.__listener.is_active():
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
        player = ConnectedPlayer(identity, self)
        player.set_connection(conn)
        if not self.__server_game_thread.add_player(player):
            msg = BasicMessage(MessageType.LOBBY_FULL)
            player.send_message(msg)
            player.disconnect()
            return
        self.__server_game_thread.broadcast(LobbyStateMessage(self.__server_game_thread.get_identities()))
        info(f"Player {player.get_name()} has successfully joined the lobby!")

    def receive(self, message: BasicMessage) -> bool:
        debug("Server received message")
        return True

    def get_lobby_list(self) -> list[Identity]:
        return self.__server_game_thread.get_identities()

    def start_game(self):
        self.__listener.stop()
        msg: BasicMessage = BasicMessage(MessageType.GAME_START)
        self.__server_game_thread.broadcast(msg)
