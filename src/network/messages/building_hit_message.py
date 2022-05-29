from core.team import Team
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class BuildingHitMessage(BasicMessage):
    def __init__(self, team: Team, left: bool, big: bool, damage: int):
        BasicMessage.__init__(self, msg_type=MessageType.BUILDING_HIT)
        self.team: Team = team
        self.left: bool = left
        self.big: bool = big
        self.damage = damage
