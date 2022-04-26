from socket import socket

from src.exceptions.general_exception import GeneralException


class NetworkException(GeneralException):
    def __init__(self, message: str, socket_reference: socket):
        super().__init__(message)
        self.__socket_reference = socket_reference

    def __str__(self):
        return f"Network error occurred: {self._message}"
