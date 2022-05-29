from network.messages.basic_message import BasicMessage
from network.messages.message_type import MessageType
from network.messages.unit_sync_data import UnitSyncData


class UnitsUpdateMessage(BasicMessage):
    def __init__(self, units: list[UnitSyncData]):
        BasicMessage.__init__(self, msg_type=MessageType.UNITS_UPDATE)
        self.units: list[UnitSyncData] = units
