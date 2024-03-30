from quacktools.exceptions.missing_argument_error import MissingArgumentError

from quacktools.constants.exception_constants import MISSING_FILE_ERROR


class MissingFileError(MissingArgumentError):
    def __init__(self):
        super().__init__(MISSING_FILE_ERROR)
