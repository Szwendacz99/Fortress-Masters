# TODO: Implement class Player
from core.identity import Identity


class Player(Identity):
    def __int__(self, name: str):
        Identity.__init__(self, name)
