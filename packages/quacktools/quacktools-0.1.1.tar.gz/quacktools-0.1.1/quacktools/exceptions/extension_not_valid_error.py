"""This module defines a custom exception. It is thrown when the extension of the file is invalid."""

from quacktools.exceptions.custom_exception import CustomException


class ExtensionNotValidError(CustomException):
    """Custom exception. Thrown when the extension of the file is invalid."""

    def __init__(self, extension):
        """Initializes the ExtensionNotValidError exception."""

        super().__init(f"Extension {extension} does not exist")
