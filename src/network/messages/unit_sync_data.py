from uuid import UUID

from pygame.math import Vector2


class UnitSyncData:
    def __init__(self, uuid: UUID, pos: Vector2):
        self.pos = pos
        self.uuid = uuid
