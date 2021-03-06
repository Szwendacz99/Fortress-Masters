from logging import info, warning
from threading import Thread
from time import sleep, time

from network.client import Client
from game.identity import Identity
from network.connected_player import ConnectedPlayer
from game.team import Team
from network.message_receiver import MessageReceiver
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType
from network.messages.team_set_message import TeamSetMessage
from network.messages.unit_sync_data import UnitSyncData
from network.messages.units_update_message import UnitsUpdateMessage


class ServerGameThread(Thread, MessageReceiver):
    def __init__(self):
        Thread.__init__(self)
        self.__team_blu: list[ConnectedPlayer] = []
        self.__team_red: list[ConnectedPlayer] = []
        self.__active = True
        self.__game_playing = False

        self.__last_heartbeat_send_time: float = time()
        self.__last_passive_income_broadcast: float = time()
        self.daemon = True

    def start_game(self):
        self.__game_playing = True
        msg: BasicMessage = BasicMessage(MessageType.GAME_START)
        self.broadcast(msg)

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
            if len(self.__team_red) == 1:
                player.send_message(TeamSetMessage(Team.RED, left=True))
            else:
                player.send_message(TeamSetMessage(Team.RED, left=False))
            return True
        elif len(self.__team_blu) < 2:
            self.__team_blu.append(player)
            player.get_identity().set_team(Team.BLU)
            if len(self.__team_blu) == 1:
                player.send_message(TeamSetMessage(Team.BLU, left=True))
            else:
                player.send_message(TeamSetMessage(Team.BLU, left=False))
            return True
        return False

    def broadcast(self, msg):
        for p in self.__team_blu + self.__team_red:
            try:
                p.send_message(msg)
                # debug(f"Server sending broadcast with {msg.get_type()} message")
            except Exception as e:
                warning(f"Error on broadcasting to client: {str(e)}")
                self.__disconnect(p)

    def get_identities(self) -> list[Identity]:
        return [p.get_identity() for p in self.__team_blu + self.__team_red]

    def __check_for_disconnects(self):
        for player in self.__team_blu + self.__team_red:
            if (time() - player.get_last_msg_receive_time()) > 5:
                self.__disconnect(player=player)
                continue

    def __disconnect(self, player: ConnectedPlayer):
        info(f"Disconnecting user \"{player.get_name()}\"")
        player.disconnect()
        if player in self.__team_blu:
            self.__team_blu.remove(player)
        elif player in self.__team_red:
            self.__team_red.remove(player)
        self.broadcast(LobbyStateMessage(self.get_identities()))

    def receive(self, message: BasicMessage) -> bool:
        """
        Broadcast messages that need to be received by all players
        other types like Heartbeat, will be skipped
        :param message:
        :return:
        """
        if message.get_type() in [MessageType.NEW_UNIT,
                                  MessageType.NEW_BULLET]:
            self.broadcast(message)
        return True

    def run(self) -> None:
        info("Starting lobby thread")
        hb: BasicMessage = BasicMessage(MessageType.HEARTBEAT)
        while self.__active:
            self.__check_for_disconnects()
            if (time() - self.__last_heartbeat_send_time) > 1.0:
                self.broadcast(hb)
                self.__last_heartbeat_send_time = time()
            self.broadcast(UnitsUpdateMessage(self.get_units_list()))

            if (time() - self.__last_passive_income_broadcast) > 2 and self.__game_playing:
                self.broadcast(BasicMessage(MessageType.PASSIVE_INCOME))
                self.__last_passive_income_broadcast = time()
            sleep(0.2)

    def get_units_list(self) -> list[UnitSyncData]:
        result = []
        for unit in Client.units.values():
            result.append(UnitSyncData(uuid=unit.uuid,
                                       pos=unit.get_pos()
                                       )
                          )
        return result
