"""This module defines a custom exception. It is thrown when the difficulty of the problem is not
specified in the arguments.
"""

from quacktools.exceptions.missing_argument_error import MissingArgumentError

from quacktools.constants.exception_constants import MISSING_DIFFICULTY_ERROR


class MissingDifficultyError(MissingArgumentError):
    """Custom exception. Thrown when the difficulty of the problem is not specified in the arguments."""

    def __init__(self) -> None:
        """Initializes the MissingDifficultyError exception."""

        super().__init__(MISSING_DIFFICULTY_ERROR)
