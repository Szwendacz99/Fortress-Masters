import pickle
from logging import debug
from socket import socket, AF_INET, SOCK_STREAM
from threading import Lock

from src.exceptions.network_exception import NetworkException
from src.network.messages.basic_message import BasicMessage

MSG_SIZE_FIELD_LENGTH = 64
BYTEORDER = 'little'


class Connection:
    """
    Connection class is basic class for representing and
    handling TCP connection. It can be instantiated with an existing socket,
    or it can be given network address and port to create one.
    """

    def __init__(self, timeout: float, address: str = "", port: int = "", sock: socket = None):
        super().__init__()

        self.__timeout: float = timeout

        if sock is not None:
            self.__socket: socket = sock
        else:
            self.__socket = None
            self.__connect(address, port)

        self.__sending_lock = Lock()

        self.__is_alive = True

    def __int__(self, timeout: int, sock: socket):
        self.__timeout = timeout
        self.__socket = sock

    def __connect(self, address: str, port: int):
        debug(f"Connecting to {address}:{port}....")

        self.__socket = socket(family=AF_INET, type=SOCK_STREAM)
        self.__socket.settimeout(self.__timeout)
        self.__socket.connect((address, port))

        debug(f"Connected successfully.")

    def send_data(self, data: BasicMessage):

        packed_msg = pickle.dumps(obj=data)
        msg_size = len(packed_msg)

        debug(f"Sending data with size: {msg_size} bytes")

        bts = int.to_bytes(msg_size, MSG_SIZE_FIELD_LENGTH, BYTEORDER)
        sent_bytes = self.__socket.send(bts)
        if sent_bytes != MSG_SIZE_FIELD_LENGTH:
            raise NetworkException(message=f"Failed sending message size information, sent {sent_bytes}"
                                           f" out of {MSG_SIZE_FIELD_LENGTH}", socket_reference=self.__socket)
        sent_bytes = self.__socket.send(packed_msg)
        if sent_bytes != msg_size:
            raise NetworkException(message=f"Failed sending message size information, sent {sent_bytes}"
                                           f" out of {msg_size}", socket_reference=self.__socket)

        debug(f"Sent: {sent_bytes + MSG_SIZE_FIELD_LENGTH} bytes")

    def receive_data(self) -> BasicMessage:
        try:
            data_to_receive = int.from_bytes(self.__socket.recv(MSG_SIZE_FIELD_LENGTH), BYTEORDER)
            data = self.__socket.recv(data_to_receive)
        except Exception as e:
            raise NetworkException(str(e), self.__socket)

        if len(data) != data_to_receive:
            raise NetworkException(message=f"Error on receiving, received only {len(data)}"
                                           f" out of {data_to_receive} bytes", socket_reference=self.__socket)

        debug(f"Received {len(data)} bytes.")

        return pickle.loads(data)

    def get_timeout(self) -> float:
        return self.__timeout

    def disconnect(self):
        self.__socket.close()
        self.__is_alive = False

    def __del__(self):
        debug("Connection object is being destroyed")
        self.disconnect()

    def is_alive(self) -> bool:
        return self.__is_alive
