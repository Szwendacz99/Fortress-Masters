from uuid import uuid4, UUID

from core.team import Team


class Identity:
    def __init__(self, username: str):
        self.__uuid: UUID = uuid4()
        self.__username = username
        self.__team: Team = None
        self.__left: bool = False

    def get_uuid(self) -> UUID:
        return self.__uuid

    def get_username(self) -> str:
        return self.__username

    def set_username(self, username: str):
        self.__username = username

    def set_team(self, team: Team):
        self.__team = team

    def get_team(self) -> Team:
        return self.__team

    def set_left(self, left: bool):
        self.__left = left

    def get_left(self) -> bool:
        return self.__left
