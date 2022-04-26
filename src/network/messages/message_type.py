from enum import Enum, unique


@unique
class MessageType(Enum):
    HEARTBEAT = 1
    JOIN = 2
