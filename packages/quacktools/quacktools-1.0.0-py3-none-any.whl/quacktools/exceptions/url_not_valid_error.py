"""This module defines a custom exception. It is thrown when the Codeforces URL is invalid.
"""

from quacktools.exceptions.custom_exception import CustomException


class URLNotValidError(CustomException):
    """Custom exception. Thrown when URL is invalid."""

    def __init__(self, url: str) -> None:
        """Initializes the URLNotValidError exception.

        Args:
            url (str): The input URL.
        """

        super().__init__(f"'{url}' is not a not a valid URL.")
