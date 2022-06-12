from abc import abstractmethod


class MessageReceiver:
    @abstractmethod
    def receive(self, message) -> bool:
        pass
