"""This module defines argument constants.

Attributes:
    ARGUMENT_FLAGS (Dict): Argument flags. The user flags must match any of the argument flags.
    URL_PREFIX (str): The URL for Codeforces.
"""

URL_PREFIX = "https://codeforces.com"

ARGUMENT_FLAGS = {
    "-t": {
        "dest": "file",
        "help": "Test your file against a problem from a problem set, or a problem from a contest.",
    },
    "-p": {
        "dest": "problem",
        "help": "What is the problem number, e.g. 1950.",
    },
    "-c": {
        "dest": "contest",
        "help": "What is the contest number, e.g. 1950.",
    },
    "-d": {
        "dest": "difficulty",
    },
}
