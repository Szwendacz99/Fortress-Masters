from threading import Thread, Lock
from time import sleep

from core.identity import Identity
from core.player import Player
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType


class Lobby(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__team_blu: list[Player] = []
        self.__team_red: list[Player] = []
        self.__active = True
        self.__lock = Lock()

    def add_player(self, player: Player) -> bool:
        """
        Add player to lobby to first team that have place
        and return true if successful. If both teams full then
        return false.
        :param player: new, connected player
        :return:
        """
        if len(self.__team_red) < 2:
            self.__team_red.append(player)
            return True
        elif len(self.__team_blu) < 2:
            self.__team_blu.append(player)
            return True
        return False

    def broadcast(self, msg: LobbyStateMessage):
        self.__lock.acquire()
        for p in self.__team_blu+self.__team_red:
            p.send_message(msg)
        self.__lock.release()

    def get_identities(self) -> list[Identity]:
        return [p.get_identity() for p in self.__team_blu+self.__team_red]

    def __broadcast_heartbeat(self):
        self.__lock.acquire()

        msg = BasicMessage(MessageType.HEARTBEAT)

        for p in self.__team_blu + self.__team_red:
            p.send_message(msg)

        self.__lock.release()

    def run(self) -> None:
        while self.__active:
            self.__broadcast_heartbeat()
            sleep(1)
