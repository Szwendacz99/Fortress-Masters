from abc import ABC

from core.team import Team
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class TeamSetMessage(BasicMessage):
    def __init__(self, team: Team):
        BasicMessage.__init__(self, MessageType.TEAM_SET)
        self.__team = team

    def get_team(self) -> Team:
        return self.__team
