from game.identity import Identity
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class LobbyStateMessage(BasicMessage):
    def __init__(self, lobby_players: list[Identity]):
        BasicMessage.__init__(self, MessageType.LOBBY_STATE)
        self.__lobby_players: list[Identity] = lobby_players

    def get_players(self) -> list[Identity]:
        return self.__lobby_players
