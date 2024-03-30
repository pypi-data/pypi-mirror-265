from quacktools.exceptions.custom_exception import CustomException


class MissingArgumentError(CustomException):
    def __init__(self, message):
        super().__init__(message)
