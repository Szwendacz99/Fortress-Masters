from typing import Type
from uuid import UUID

from core.team import Team
from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType


class NewBulletMessage(BasicMessage):
    def __init__(self,
                 source_uuid: UUID,
                 source_type,
                 team: Team,
                 target_type,
                 target_uuid):
        BasicMessage.__init__(self, msg_type=MessageType.NEW_BULLET)
        self.team: Team = team
        self.source_uuid = source_uuid
        self.source_type: Type = source_type
        self.target_type: Type = target_type
        self.target_uuid = target_uuid
        self.building_target_id: int = -1
        self.building_source_id: int = -1

    def set_building_target_id(self, id: int):
        self.building_target_id = id

    def set_building_source_id(self, id: int):
        self.building_source_id = id
