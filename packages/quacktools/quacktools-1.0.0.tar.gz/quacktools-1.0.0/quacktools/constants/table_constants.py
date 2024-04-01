"""This module contains table constants. Tables are displayed to the terminal.

Attributes:
    DETAILED_USAGE_HEADERS (List): Detailed usage table headers.
    DETAILED_USAGE_ROWS (List): Detailed usage table rows.
    EXTENSION_HEADERS (List): Extension table headers.
    EXTENSION_ROWS (List): Extension table rows.
    INSTRUCTIONS (Dict): Set of instructions.
    TERMINAL_COLORS (Dict): Terminal colors for text.
    TEST_CASE_OUTPUT_COLUMNS (List): Column headers for tables.
"""

EXTENSION_HEADERS = [
    "SUPPORTED_FILE_TYPES",
    "SUPPORTED_FILE_EXTENSIONS",
]

DETAILED_USAGE_HEADERS = [
    "COMMAND",
    "DESCRIPTION",
]

EXTENSION_ROWS = [
    [
        "python",
        "cpp",
        "c",
        "csharp",
        "java",
    ],
    [
        ".py, .pyc",
        ".cxx, .cpp, .cc, .c++",
        ".c",
        ".cs, .csx",
        ".java",
    ],
]

DETAILED_USAGE_ROWS = [
    [
        "quack -t [filename].[extension] -p [problem-number] -d [difficulty]",
        "quack -t [filename].[extension] -c [contest-number] -d [difficulty]",
    ],
    [
        "Test your code for a problem from a contest. e.g.\n"
        "quack -t main.cpp -c 1950 -d A\n"
        "Would test main.cpp for contest problem 1950A.",
        "Test your code for a problem from a contest. e.g.\n"
        "quack -t main.cpp -c 1950 -d A\n"
        "Would test main.cpp for contest problem 1950A.",
    ],
]

TERMINAL_COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "default": "\033[0m",
}

INSTRUCTIONS = {
    "extensions": [
        EXTENSION_HEADERS,
        EXTENSION_ROWS,
    ],
    "detailed_usage": [
        DETAILED_USAGE_HEADERS,
        DETAILED_USAGE_ROWS,
    ],
}

TEST_CASE_OUTPUT_COLUMNS = [
    "TEST CASE",
    "INPUT",
    "OUTPUT",
    "USER_OUTPUT",
    "RESULT",
]
