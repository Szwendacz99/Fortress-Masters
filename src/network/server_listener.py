from logging import info
from socket import socket, AF_INET, SOCK_STREAM

from network.connection import Connection


class ServerListener:
    """
    Class for just receiving connections and creating Connection objects
    """
    def __init__(self, port: int, timeout: float):
        """
        Initialize listener on given port with connection dropping after
        timeout-seconds of no activity
        :param port: port to listen on
        :param timeout: connection timeout in seconds
        """
        self.__socket = socket(family=AF_INET, type=SOCK_STREAM)

        self.__timeout = timeout
        self.__port = port

        self.__prepare_socket()

    def __prepare_socket(self):
        """
        Bind and start listening for connections, but
        without accepting ones.
        :return:
        """
        info(f"Binding on port {self.__port}.")

        self.__socket.bind(("0.0.0.0", self.__port))

        info("Listening...")

        self.__socket.listen()

    def receive_connection(self) -> Connection:
        """
        Block until a connection is received
        Then return Connection with opened connection
        :return:
        """

        connection, address = self.__socket.accept()

        info(f"Received connection from {address}.")

        connection.settimeout(self.__timeout)

        return Connection(timeout=self.__timeout, sock=connection)
