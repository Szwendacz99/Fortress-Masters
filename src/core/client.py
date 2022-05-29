from builtins import staticmethod
from logging import debug, info, error
from threading import Thread, Lock
from time import time
from uuid import UUID

from core.identity import Identity
from core.message_receiver import MessageReceiver
from game.building import Building
from game.bullet import Bullet
from game.spaceship import Spaceship
from game.unit import Unit
from game.unit_type import UnitType
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.join_message import JoinMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType
from network.messages.new_unit_message import NewUnitMessage
from network.messages.units_update_message import UnitsUpdateMessage


class Client(Thread, MessageReceiver):
    buildings: dict[UUID, Building] = {}
    units: dict[UUID, Unit] = {}
    bullets: dict[UUID, Bullet] = {}

    def __init__(self, game, username: str, is_server: bool = False):
        Thread.__init__(self)
        self.lobby_list: list[Identity] = []
        self.__game_started: bool = False
        self.__is_server: bool = is_server

        self.__identity: Identity = Identity(username)
        self.__connection: Connection = None
        self.__last_msg_receive_time: float = time()
        self.daemon = True
        self.__game = game
        self.__lock = Lock()

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
            self.__game.play_menu.start_game()
        elif message.get_type() == MessageType.TEAM_SET:
            self.__identity.set_team(message.get_team())
            info(f"Assigned to team {message.get_team()}")
        elif message.get_type() == MessageType.NEW_UNIT:
            self.add_new_unit(message)
        elif message.get_type() == MessageType.UNITS_UPDATE:
            self.update_units(message)
        elif message.get_type() == MessageType.UNIT_DEATH:
            self.units.get(message.uuid).die(server_told=True)

        return True

    def add_new_unit(self, msg: NewUnitMessage):
        if msg.unit_type == UnitType.SPACESHIP:
            Client.units[msg.uuid] = Spaceship(uuid=msg.uuid,
                                               game=self.__game,
                                               start_pos=msg.pos,
                                               team=msg.team)

    def update_units(self, msg: UnitsUpdateMessage):
        for unit in msg.units:
            curr_unit = Client.units.get(unit.uuid)
            if curr_unit is not None:
                curr_unit.set_pos(unit.pos)

    def get_identity(self) -> Identity:
        return self.__identity

    def get_lobby_list(self) -> list[Identity]:
        return self.lobby_list

    def send_message(self, msg: [BasicMessage, LobbyStateMessage]):
        # debug(f"Client sending message with type: {msg.get_type()}")
        self.__lock.acquire()
        self.__connection.send_data(msg)
        self.__lock.release()

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

    @staticmethod
    def add_building(building: Building):
        Client.buildings[building.uuid] = building

    def get_is_server(self) -> bool:
        return self.__is_server
