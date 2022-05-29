from logging import info, debug
from threading import Thread, Lock
from time import sleep, time

from core.client import Client
from core.identity import Identity
from core.connected_player import ConnectedPlayer
from core.team import Team
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType
from network.messages.new_unit_message import NewUnitMessage
from network.messages.team_set_message import TeamSetMessage
from network.messages.unit_sync_data import UnitSyncData
from network.messages.units_update_message import UnitsUpdateMessage


class ServerGameThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__team_blu: list[ConnectedPlayer] = []
        self.__team_red: list[ConnectedPlayer] = []
        self.__active = True
        self.__last_heartbeat_send_time = time()
        self.__lock = Lock()
        self.daemon = True

    def add_player(self, player: ConnectedPlayer) -> bool:
        """
        Add player to lobby to first team that have place
        and return true if successful. If both teams full then
        return false.
        :param player: new, connected player
        :return:
        """
        player.start()
        if len(self.__team_red) < 2:
            self.__team_red.append(player)
            player.get_identity().set_team(Team.RED)
            self.__lock.acquire()
            player.send_message(TeamSetMessage(Team.RED))
            self.__lock.release()
            return True
        elif len(self.__team_blu) < 2:
            self.__team_blu.append(player)
            player.get_identity().set_team(Team.BLU)
            self.__lock.acquire()
            player.send_message(TeamSetMessage(Team.BLU))
            self.__lock.release()
            return True
        return False

    def broadcast(self, msg):
        self.__lock.acquire()
        for p in self.__team_blu + self.__team_red:
            try:
                p.send_message(msg)
                # debug(f"Server sending broadcast with {msg.get_type()} message")
            except:
                self.__lock.release()
                self.__disconnect(p)
                self.__lock.acquire()
        self.__lock.release()

    def get_identities(self) -> list[Identity]:
        return [p.get_identity() for p in self.__team_blu + self.__team_red]

    def __check_for_disconnects(self):
        for player in self.__team_blu + self.__team_red:
            if (time() - player.get_last_msg_receive_time()) > 5:
                self.__disconnect(player=player)
                continue

    def __disconnect(self, player: ConnectedPlayer):
        self.__lock.acquire()
        info(f"Disconnecting user \"{player.get_name()}\"")
        player.disconnect()
        if player in self.__team_blu:
            self.__team_blu.remove(player)
        elif player in self.__team_red:
            self.__team_red.remove(player)
        self.__lock.release()
        self.broadcast(LobbyStateMessage(self.get_identities()))

    def run(self) -> None:
        info("Starting lobby thread")
        hb: BasicMessage = BasicMessage(MessageType.HEARTBEAT)
        while self.__active:
            self.__check_for_disconnects()
            if (time() - self.__last_heartbeat_send_time) > 1:
                self.broadcast(hb)
                self.__last_heartbeat_send_time = time()
            self.broadcast(UnitsUpdateMessage(self.get_units_list()))
            sleep(0.1)

    def get_units_list(self) -> list[UnitSyncData]:
        result = []
        for unit in Client.units.values():
            result.append(UnitSyncData(uuid=unit.uuid,
                                       pos=unit.get_pos()
                                       )
                          )
        return result
