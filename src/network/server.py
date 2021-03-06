from logging import info, warning
from threading import Thread

from network.server_game_thread import ServerGameThread
from game.identity import Identity
from network.connected_player import ConnectedPlayer
from exceptions.network_exception import NetworkException
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.join_message import JoinMessage
from network.messages.message_type import MessageType
from network.server_listener import ServerListener


class Server(Thread):

    def __init__(self, port: int, identity: Identity):
        super().__init__()
        self.__listener: ServerListener = ServerListener(port, timeout=10)
        self.__server_game_thread: ServerGameThread = ServerGameThread()
        self.__server_game_thread.start()
        self.__identity = identity
        self.__team_blu: list[ConnectedPlayer] = []
        self.__team_red: list[ConnectedPlayer] = []
        self.daemon = True

    def run(self):
        info(f"Started server lobby on port {self.__listener.get_port()}")
        while self.__listener.is_active():
            try:
                self.recv_connection_from_player()
            except NetworkException as e:
                warning(f"Client failed to join the server: {str(e)}")

    def recv_connection_from_player(self):
        """
        receive connection and identity from plater, and
        add the player to lobby
        :return:
        """
        new_conn: Connection = self.__listener.receive_connection()
        new_conn.set_timeout(10)
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
        player = ConnectedPlayer(identity, self.__server_game_thread)
        player.set_connection(conn)
        if not self.__server_game_thread.add_player(player):
            msg = BasicMessage(MessageType.LOBBY_FULL)
            player.send_message(msg)
            player.disconnect()
            return
        self.__server_game_thread.broadcast(LobbyStateMessage(self.__server_game_thread.get_identities()))
        info(f"Player {player.get_name()} has successfully joined the lobby!")

    def get_lobby_list(self) -> list[Identity]:
        return self.__server_game_thread.get_identities()

    def start_game(self):
        self.__listener.stop()
        self.__server_game_thread.start_game()
