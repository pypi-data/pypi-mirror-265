"""This module is responsible for handling the lifecycle of the quack command."""

from __future__ import annotations

import sys

from typing import TYPE_CHECKING, Union

from quacktools.compiler.cpp_compiler import CPPCompiler
from quacktools.utilities.utility import Utility

from quacktools.exceptions.url_not_valid_error import URLNotValidError
from quacktools.exceptions.extension_not_valid_error import ExtensionNotValidError

from quacktools.constants.argument_constants import URL_PREFIX


if TYPE_CHECKING:
    import argparse

    from quacktools.compiler.compiler import Compiler


class App:
    """The App instance is a singleton instance, and defines the lifecycle of the application.

    Attributes:
        arguments (argparse.Namespace): The raw user arguments.
        url (str): The input URL.
    """

    def __init__(self) -> None:
        """Initializes the App instance."""

        self.arguments: argparse.Namespace = Utility.get_arguments()
        self.url: str = self.get_url()

    def run(self) -> None:
        """Runs the application. It will get the compiler based on the file extension and then compile
        the user's code. Finally, it will then test the user's output against the sample's output.
        """

        compiler = None

        try:
            compiler = self.get_compiler()
        except ExtensionNotValidError as e:
            print(e)

        if compiler is None:
            sys.exit(0)

        compiler.initialize()
        compiler.compile()
        compiler.get_program_output()
        compiler.test_samples_with_user_output()

    def get_problem_number(self) -> str:
        """Returns the problem number of the problem. The problem number will depend on whether the
        problem is from a problemset or a contest.

        Returns:
            str: The problem number of the problem.
        """

        if self.arguments.problem is not None:
            return self.arguments.problem

        return self.arguments.contest

    def get_url(self) -> str:
        """Returns a valid Codeforce URL. If the URL is not valid, an exception will be thrown.

        Returns:
            str: A valid Codeforces URL.
        """

        url = None
        problem_number = self.get_problem_number()
        difficulty = self.arguments.difficulty

        if self.arguments.contest is not None:
            url = URL_PREFIX + f"/contest/{problem_number}/problem/{difficulty}"
        else:
            url = URL_PREFIX + f"/problemset/problem/{problem_number}/{difficulty}"

        is_url_valid = False

        try:
            Utility.validate_url(url)
            is_url_valid = True
        except URLNotValidError as e:
            print(f"{e.__class__.__name__}: {e}")

        if not is_url_valid:
            sys.exit(0)

        return url

    def get_compiler(self) -> Union[Compiler, None]:
        """Returns a compiler based on the file extension. If the extension of the file is invalid,
        an exception will be thrown.

        Returns:
            None: A compiler based on the file extension.

        Raises:
            ExtensionNotValidError: Exception thrown for invalid extension.
        """

        extension = self.arguments.file.split(".")[1]

        match extension:
            case "cpp":
                return CPPCompiler(self)

        raise ExtensionNotValidError(extension)
