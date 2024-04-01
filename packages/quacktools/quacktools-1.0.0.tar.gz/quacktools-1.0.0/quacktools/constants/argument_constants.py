"""This module defines argument constants.

Attributes:
    ARGUMENT_FLAGS (Dict): Argument flags. The user flags must match any of the argument flags.
    DETAILED_USAGE_FLAG (str): Detailed usage flag.
    LIST_EXTENSIONS_FLAG (str): List extensions flag.
    PARSE_FLAGS (Set): Set of valid parsing flags.
    TEST_FLAGS (Set): Set of valid testing flags.
    URL_PREFIX (str): The URL for Codeforces.
    VALID_ARGUMENT_FLAGS (Set): Set of valid argument flags.
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
        "help": "What is the difficulty of the problem (should be uppercase letter), e.g. A.",
    },
    "-le": {
        "action": "store_true",
        "help": "List all supported file extension types.",
    },
    "-du": {
        "action": "store_true",
        "help": "Get detailed usage on how to use 'quacktools'.",
    },
}

PARSE_FLAGS = {
    "-t",
    "-p",
    "-d",
    "-t -p -d",
    "-t -c -d",
    "-h",
}

VALID_ARGUMENT_FLAGS = {
    "-t",
    "-p",
    "-d",
    "-t -p -d",
    "-t -c -d",
    "-h",
    "-le",
    "-du",
}

TEST_FLAGS = {
    "-t -p -d",
    "-t -c -d",
}

LIST_EXTENSIONS_FLAG = "-le"
DETAILED_USAGE_FLAG = "-du"
