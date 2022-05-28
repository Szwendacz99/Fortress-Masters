from enum import Enum, unique


@unique
class MessageType(Enum):
    HEARTBEAT = 1
    JOIN = 2
    LOBBY_STATE = 3
    LOBBY_FULL = 4
    GAME_START = 5
    TEAM_SET = 6
