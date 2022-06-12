from game.team import Team
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class TeamSetMessage(BasicMessage):
    def __init__(self, team: Team, left: bool):
        BasicMessage.__init__(self, MessageType.TEAM_SET)
        self.__team = team
        self.__left = left

    def get_team(self) -> Team:
        return self.__team

    def get_left(self) -> bool:
        return self.__left
