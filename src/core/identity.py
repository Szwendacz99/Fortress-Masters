from uuid import uuid4, UUID


class Identity:
    def __init__(self, name: str):
        self.__uuid: UUID = uuid4()
        self.__name = name

    def get_uuid(self) -> UUID:
        return self.__uuid

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name
