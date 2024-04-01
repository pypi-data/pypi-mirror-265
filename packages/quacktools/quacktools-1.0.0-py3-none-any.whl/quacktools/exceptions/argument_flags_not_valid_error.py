"""This module defines a custom exception. It is thrown when the user argument
flags are invalid.
"""

from quacktools.exceptions.custom_exception import CustomException

from quacktools.constants.exception_constants import ARGUMENT_FLAGS_NOT_VALID_ERROR


class ArgumentFlagsNotValidError(CustomException):
    """Custom exception. Thrown when the user argument flags are invalid."""

    def __init__(self) -> None:
        """Initializes the ArgumentFlagsNotValidError exception."""

        super().__init__(ARGUMENT_FLAGS_NOT_VALID_ERROR)
