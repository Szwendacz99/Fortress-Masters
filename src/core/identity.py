from uuid import uuid4, UUID


class Identity:
    def __init__(self):
        self.__uuid: UUID = uuid4()

    def get_uuid(self) -> UUID:
        return self.__uuid
