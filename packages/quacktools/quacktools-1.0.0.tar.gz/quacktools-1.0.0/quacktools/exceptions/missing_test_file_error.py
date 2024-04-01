"""This module defines a custom exception. It is thrown when the file is not specified in the arguments.
"""

from quacktools.exceptions.missing_argument_error import MissingArgumentError

from quacktools.constants.exception_constants import MISSING_FILE_ERROR


class MissingFileError(MissingArgumentError):
    """Custom exception. Thrown when file is not specified in the arguments."""

    def __init__(self) -> None:
        """Initializes the MissingFileError exception."""

        super().__init__(MISSING_FILE_ERROR)
