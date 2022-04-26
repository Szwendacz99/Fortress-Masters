from src.network.server_listener import ServerListener
from threading import Thread


class Server(Thread):
    def __int__(self, port: int):
        self.__listener: ServerListener = ServerListener(port, 3)

    def run(self):
        while True:
            msg = self.__listener.receive_connection()
