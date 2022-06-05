from builtins import staticmethod
from logging import debug, info, error
from threading import Thread, Lock
from time import time
from uuid import UUID

from core.identity import Identity
from core.message_receiver import MessageReceiver
from game.building import Building
from game.bullet import Bullet
from game.laser import Laser
from game.rocket import Rocket
from game.units.spaceship import Spaceship
from game.units.spaceship_1 import Spaceship_1
from game.units.spaceship_2 import Spaceship_2
from game.units.spaceship_3 import Spaceship_3
from game.units.spaceship_4 import Spaceship_4
from game.units.spaceship_5 import Spaceship_5
from game.units.spaceship_6 import Spaceship_6
from game.units.unit import Unit
from game.units.unit_type import UnitType
from network.connection import Connection
from network.messages.basic_message import BasicMessage
from network.messages.building_hit_message import BuildingHitMessage
from network.messages.join_message import JoinMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType
from network.messages.new_bullet_message import NewBulletMessage
from network.messages.new_unit_message import NewUnitMessage
from network.messages.units_update_message import UnitsUpdateMessage


class Client(Thread, MessageReceiver):
    buildings: list[Building] = []
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
                                          timeout=3)
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
            self.__game.play_menu.set_game_ready()
        elif message.get_type() == MessageType.TEAM_SET:
            self.__identity.set_team(message.get_team())
            info(f"Assigned to team {message.get_team()}")
        elif message.get_type() == MessageType.NEW_UNIT:
            self.add_new_unit(message)
        elif message.get_type() == MessageType.UNITS_UPDATE:
            self.update_units(message)
        elif message.get_type() == MessageType.UNIT_HIT:
            if self.units.get(message.uuid) is not None:
                self.units.get(message.uuid).lose_hp(message.damage, server_told=True)
        elif message.get_type() == MessageType.BUILDING_HIT:
            self.building_receive_hit(message)
        elif message.get_type() == MessageType.NEW_BULLET:
            self.add_new_bullet(message)

        return True

    def add_new_bullet(self, msg: NewBulletMessage):

        if msg.target_type == Building:
            target = self.buildings[msg.building_target_id]
        else:
            target = self.units[msg.target_uuid]

        if msg.source_type == Building:
            source = self.buildings[msg.building_source_id]
        else:
            source = self.units[msg.source_uuid]

        source.shoot_target(target)


    def add_new_unit(self, msg: NewUnitMessage):
        if msg.unit_type == UnitType.SPACESHIP:
            Client.units[msg.uuid] = Spaceship(uuid=msg.uuid,
                                               game=self.__game,
                                               start_pos=msg.pos,
                                               team=msg.team,
                                               client_team=self.__game.client.get_identity().get_team())
        elif msg.unit_type == UnitType.SPACESHIP_1:
            Client.units[msg.uuid] = Spaceship_1(uuid=msg.uuid,
                                                 game=self.__game,
                                                 start_pos=msg.pos,
                                                 team=msg.team,
                                                 client_team=self.__game.client.get_identity().get_team())
        elif msg.unit_type == UnitType.SPACESHIP_2:
            Client.units[msg.uuid] = Spaceship_2(uuid=msg.uuid,
                                                 game=self.__game,
                                                 start_pos=msg.pos,
                                                 team=msg.team,
                                                 client_team=self.__game.client.get_identity().get_team())
        elif msg.unit_type == UnitType.SPACESHIP_3:
            Client.units[msg.uuid] = Spaceship_3(uuid=msg.uuid,
                                                 game=self.__game,
                                                 start_pos=msg.pos,
                                                 team=msg.team,
                                                 client_team=self.__game.client.get_identity().get_team())
        elif msg.unit_type == UnitType.SPACESHIP_4:
            Client.units[msg.uuid] = Spaceship_4(uuid=msg.uuid,
                                                 game=self.__game,
                                                 start_pos=msg.pos,
                                                 team=msg.team,
                                                 client_team=self.__game.client.get_identity().get_team())
        elif msg.unit_type == UnitType.SPACESHIP_5:
            Client.units[msg.uuid] = Spaceship_5(uuid=msg.uuid,
                                                 game=self.__game,
                                                 start_pos=msg.pos,
                                                 team=msg.team,
                                                 client_team=self.__game.client.get_identity().get_team())
        elif msg.unit_type == UnitType.SPACESHIP_6:
            Client.units[msg.uuid] = Spaceship_6(uuid=msg.uuid,
                                                 game=self.__game,
                                                 start_pos=msg.pos,
                                                 team=msg.team,
                                                 client_team=self.__game.client.get_identity().get_team())

    def building_receive_hit(self, msg: BuildingHitMessage):
        for building in self.buildings:
            if building.get_team() == msg.team and \
                    building.get_big() is msg.big and \
                    building.get_left() is msg.left:
                # print(f"{building.get_x()} {building.get_y()} hm")
                building.lose_hp(msg.damage, server_told=True)
            elif building.get_team() == (not msg.team) and \
                    building.get_big() is msg.big and \
                    building.get_left() is not msg.left:
                # print(f"{building.get_x()} {building.get_y()}")
                building.lose_hp(msg.damage, server_told=True)

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
            except PermissionError as e:
                error(f"Lost connection with server with error {e.__class__}: {str(e)}")
                self.__connection.disconnect()
            self.__last_msg_receive_time = time()

    def disconnect(self):
        self.__connection.disconnect()

    @staticmethod
    def add_building(building: Building):
        Client.buildings.append(building)

    def get_is_server(self) -> bool:
        return self.__is_server
