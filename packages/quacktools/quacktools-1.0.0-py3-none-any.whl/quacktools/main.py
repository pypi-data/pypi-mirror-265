"""This module contains the main driver code.
"""

import sys

from quacktools.app.app import App
from quacktools.exceptions.argument_flags_not_valid_error import ArgumentFlagsNotValidError
from quacktools.utilities.utility import Utility


def main() -> None:
    """Gets called upon using the 'quack' command from the CLI."""

    argument_flags = " ".join([sys.argv[i] for i in range(1, len(sys.argv), 2)])

    try:
        Utility.validate_argument_flags(argument_flags)
        App().run(argument_flags)
    except ArgumentFlagsNotValidError as e:
        print(f"{e.__class__.__name__}: {e}")


if __name__ == "__main__":
    main()
