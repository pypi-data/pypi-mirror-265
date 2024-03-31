"""This module contains exception error messages.

Attributes:
    FILE_NOT_FOUND_ERROR (str): File is not found in current directory error message.
    MISSING_DIFFICULTY_ERROR (str): Difficulty argument is not specified error message.
    MISSING_FILE_ERROR (str): File is not specified error message.
    MISSING_PROBLEM_TYPE_ERROR (str): Problem type is not specified error message.
"""

MISSING_PROBLEM_TYPE_ERROR = "Both 'problem' and 'contest' arguments are missing."
MISSING_FILE_ERROR = "You did not specify your 'file' for testing."
MISSING_DIFFICULTY_ERROR = "You did not specify the problem's 'difficulty'."
FILE_NOT_FOUND_ERROR = "File is not found in current directory."
