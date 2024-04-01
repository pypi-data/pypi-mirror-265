"""This module is responsible for handling the lifecycle of the quack command.
"""

from __future__ import annotations

import sys
import argparse

from typing import TYPE_CHECKING, Union

from quacktools.cache.cache import Cache

from quacktools.compiler.c_compiler import CCompiler
from quacktools.compiler.cpp_compiler import CPPCompiler
from quacktools.compiler.c_sharp_compiler import CSharpCompiler
from quacktools.compiler.java_compiler import JavaCompiler
from quacktools.compiler.python_compiler import PythonCompiler

from quacktools.utilities.logger import Logger
from quacktools.utilities.utility import Utility

from quacktools.exceptions.url_not_valid_error import URLNotValidError
from quacktools.exceptions.extension_not_valid_error import ExtensionNotValidError

from quacktools.constants.table_constants import INSTRUCTIONS
from quacktools.constants.extension_constants import EXTENSIONS, COMPILER_TYPES
from quacktools.constants.argument_constants import (
    URL_PREFIX,
    TEST_FLAGS,
    PARSE_FLAGS,
    LIST_EXTENSIONS_FLAG,
    DETAILED_USAGE_FLAG,
)


if TYPE_CHECKING:
    from quacktools.compiler.compiler import Compiler


class App:
    """The App instance is a singleton instance, and defines the lifecycle of the application.

    Attributes:
        arguments (argparse.Namespace): The raw user arguments.
        url (str): The input URL.
        cache (Cache): The local cache.
    """

    def __init__(self) -> None:
        """Initializes the App instance."""

        self.arguments: argparse.Namespace = argparse.Namespace()
        self.cache: Cache = Cache()
        self.url: str = ""

        # Match user argument flags to appropriate method

    def run(self, argument_flags: str) -> None:
        """Runs the application. It will execute functionalities based on the user's argument flags.

        Args:
            argument_flags (str): The user's argument flags.
        """

        if argument_flags in PARSE_FLAGS:
            self.arguments = Utility.get_arguments()

        if argument_flags in TEST_FLAGS:
            self.test_user_code()
        elif argument_flags == LIST_EXTENSIONS_FLAG:
            Logger.log_custom_table(*INSTRUCTIONS["extensions"])
        elif argument_flags == DETAILED_USAGE_FLAG:
            Logger.log_custom_table(*INSTRUCTIONS["detailed_usage"])

    def test_user_code(self):
        """Test the user's code with the I/O samples."""

        self.url = self.get_url()

        extension_type = None

        try:
            extension_type = self.get_extension_type()
        except ExtensionNotValidError as e:
            print(f"{e.__class__.__name__}: {e}")

        if extension_type is None:
            sys.exit(0)

        compiler = self.get_compiler(extension_type)
        compiler.initialize()

        if extension_type in COMPILER_TYPES:
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

        url = ""
        problem_number = self.get_problem_number()
        difficulty = self.arguments.difficulty

        if self.arguments.contest is not None:
            url = URL_PREFIX + f"/contest/{problem_number}/problem/{difficulty}"
        else:
            url = URL_PREFIX + f"/problemset/problem/{problem_number}/{difficulty}"

        if self.cache.check_samples_cached(url):
            return url

        is_url_valid = False

        try:
            Utility.validate_url(url)
            is_url_valid = True
        except URLNotValidError as e:
            print(f"{e.__class__.__name__}: {e}")

        if not is_url_valid:
            sys.exit(0)

        return url

    def get_extension_type(self) -> Union[str, None]:
        """Returns the extension type of the file.

        Returns:
            Union[str, None]: The extension type.

        Raises:
            ExtensionNotValidError: Exception thrown for invalid extension.
        """

        file_extension = self.arguments.file.split(".")[1]

        for extension_type, extensions in EXTENSIONS.items():
            if file_extension in extensions:
                return extension_type

        raise ExtensionNotValidError(file_extension)

    def get_compiler(self, extension_type) -> Compiler:
        """Returns a compiler based on the file extension. If the extension of the file is invalid,
        an exception will be thrown.

        Returns:
            Compiler: A compiler based on the file extension.

        Args:
            extension_type (TYPE): Description
        """

        match extension_type:
            case "python":
                return PythonCompiler(self)
            case "cpp":
                return CPPCompiler(self)
            case "c":
                return CCompiler(self)
            case "csharp":
                return CSharpCompiler(self)
            case "java":
                return JavaCompiler(self)
