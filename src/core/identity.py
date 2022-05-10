from uuid import uuid4, UUID


class Identity:
    def __init__(self, username: str):
        self.__uuid: UUID = uuid4()
        self.__username = username

    def get_uuid(self) -> UUID:
        return self.__uuid

    def get_username(self) -> str:
        return self.__username

    def set_username(self, username: str):
        self.__username = username
