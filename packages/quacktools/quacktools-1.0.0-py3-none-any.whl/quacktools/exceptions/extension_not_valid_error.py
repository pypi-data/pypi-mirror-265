"""This module defines a custom exception. It is thrown when the extension of the file is invalid.
"""

from quacktools.exceptions.custom_exception import CustomException


class ExtensionNotValidError(CustomException):
    """Custom exception. Thrown when the extension of the file is invalid."""

    def __init__(self, extension: str) -> None:
        """Initializes the ExtensionNotValidError exception.

        Args:
            extension (str): The extension.
        """

        super().__init__(f"Extension {extension} does not exist")
