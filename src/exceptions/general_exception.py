class GeneralException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    def __str__(self):
        return f"Unknown error occurred: {self._message}"
