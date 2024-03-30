from quacktools.exceptions.custom_exception import CustomException

from quacktools.constants.exception_constants import FILE_NOT_FOUND_ERROR


class FileNotFoundError(CustomException):
    def __init__(self):
        super().__init__(FILE_NOT_FOUND_ERROR)
