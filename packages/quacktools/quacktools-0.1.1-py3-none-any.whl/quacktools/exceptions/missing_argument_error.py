"""This module defines a custom exception. It is thrown when the problem or contest are not specified
in the arguments.
"""

from quacktools.exceptions.custom_exception import CustomException


class MissingArgumentError(CustomException):
    """Custom exception. Thrown when the problem or contest are not specified in the arguments."""

    def __init__(self, message):
        """Initializes the MissingArgumentError exception."""

        super().__init__(message)
