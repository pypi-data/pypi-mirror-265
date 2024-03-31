"""This module contains table constants. Tables are displayed to the terminal.

Attributes:
    TERMINAL_COLORS (Dict): Terminal colors for text.
    TEST_CASE_OUTPUT_COLUMNS (List): Column headers for tables.
"""

TERMINAL_COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "default": "\033[0m",
}

TEST_CASE_OUTPUT_COLUMNS = [
    "TEST CASE",
    "INPUT",
    "OUTPUT",
    "USER_OUTPUT",
    "RESULT",
]
