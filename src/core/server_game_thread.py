from logging import info
from threading import Thread, Lock
from time import sleep, time

from core.identity import Identity
from core.connected_player import ConnectedPlayer
from network.messages.basic_message import BasicMessage
from network.messages.lobby_state_message import LobbyStateMessage
from network.messages.message_type import MessageType


class ServerGameThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__team_blu: list[ConnectedPlayer] = []
        self.__team_red: list[ConnectedPlayer] = []
        self.__active = True
        self.__lock = Lock()

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
            return True
        elif len(self.__team_blu) < 2:
            self.__team_blu.append(player)
            return True
        return False

    def broadcast(self, msg):
        self.__lock.acquire()
        for p in self.__team_blu+self.__team_red:
            try:
                p.send_message(msg)
            except:
                self.__lock.release()
                self.__disconnect(p)
                self.__lock.acquire()
        self.__lock.release()

    def get_identities(self) -> list[Identity]:
        return [p.get_identity() for p in self.__team_blu+self.__team_red]

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
        else:
            self.__team_red.remove(player)
        self.__lock.release()
        self.broadcast(LobbyStateMessage(self.get_identities()))

    def run(self) -> None:
        info("Starting lobby thread")
        hb: BasicMessage = BasicMessage(MessageType.HEARTBEAT)
        while self.__active:
            self.__check_for_disconnects()
            self.broadcast(hb)
            sleep(1)
