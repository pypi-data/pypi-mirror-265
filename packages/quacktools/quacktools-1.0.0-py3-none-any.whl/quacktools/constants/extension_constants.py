"""This module contains extension constants and compiler constants.

Attributes:
    APPLICATION_NAME (str): The application name.
    CACHE_FILE_NAME (str): The cache file name.
    COMPILER_TYPES (Dict): All valid compiler types.
    EXTENSIONS (Dict): All valid extension types.
"""

APPLICATION_NAME = "quacktools"
CACHE_FILE_NAME = "/cache.json"

COMPILER_TYPES = {
    "cpp",
    "c",
    "csharp",
    "java",
}

EXTENSIONS = {
    "python": {
        "py",
        "pyc",
    },
    "cpp": {
        "cxx",
        "cpp",
        "cc",
        "c++",
    },
    "c": {
        "c",
    },
    "csharp": {
        "cs",
        "csx",
    },
    "java": {
        "java",
    },
}
