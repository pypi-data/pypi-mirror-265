"""This module defines the structure of a compiler. Custom compilers must reference the base compiler.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, List, Dict

import subprocess

from quacktools.utilities.logger import Logger
from quacktools.utilities.utility import Utility

from quacktools.constants.table_constants import TERMINAL_COLORS, TEST_CASE_OUTPUT_COLUMNS

if TYPE_CHECKING:
    from quacktools.app.app import App

# Note to self: compiler only a singleton instance, there may be no need for other types of
# compilers other than to be explicit. We will see if it becomes a redundant mess.


class Compiler(ABC):
    """The Compiler class is a parent class. All child classes (custom compilers in this context) must
    reference the parent class.

    Attributes:
        file (str): The file.
        samples (Dict): The I/O samples.

    Deleted Attributes:
        app (App): The application instance.
        filename (str): The name of the file.
        extension (str): The extension of the file.
        user_outputs (List): List containing the user's output for each test case.
    """

    def __init__(self, app: App) -> None:
        """Initializes the compiler.

        Args:
            app (App): The application instance.
        """

        self.app: App = app
        self.file: str = ""
        self.filename: str = ""
        self.extension: str = ""
        self.user_outputs: List[str] = []
        self.samples: Dict[str, List[str]] = {}

    @abstractmethod
    def get_program_output(self) -> None:
        """Abstract method. Retrieves the user's program's output."""

    def initialize(self) -> None:
        """Initializes the compiler by first setting the file and then setting the I/O samples."""

        self.set_file()
        self.set_samples()

    def get_user_output(self, sample_input: str, command: str) -> None:
        """Get the user's code output for the current test case.

        Args:
            sample_input (str): The current test case sample input.
            command (str): The command to be executed.
        """

        with open(f"{self.filename}.txt", "w", encoding="utf-8") as output_file:
            subprocess.run(
                command,
                check=True,
                shell=True,
                stdout=output_file,
                input=sample_input.encode(),
                stderr=subprocess.PIPE,
            )

        with open(f"{self.filename}.txt", "r", encoding="utf-8") as output_file:
            self.user_outputs.append(output_file.read())

    def get_test_case_result(self, sample_output: str, user_output: str) -> str:
        """Compares the sample's output to the user's output for the current test case. AC means that
        the user has passed the test case, otherwise, the user has failed the test case.

        Args:
            sample_output (str): The sample's output for the current test case.
            user_output (str): The user's output for the current test case.

        Returns:
            str: AC or WA based on comparison.
        """

        if sample_output == user_output:
            return f"{TERMINAL_COLORS['green']}AC{TERMINAL_COLORS['default']}"

        return f"{TERMINAL_COLORS['red']}WA{TERMINAL_COLORS['default']}"

    def set_file(self) -> None:
        """Set the file from the user's arguments."""

        self.file = self.app.arguments.file
        self.filename, self.extension = self.app.arguments.file.split(".")

    def set_samples(self) -> None:
        """Set the I/O samples. If the samples already exist, then we get the cached samples."""

        cache_key = self.app.url

        if self.app.cache.check_samples_cached(cache_key):
            self.samples = self.app.cache.get_samples(cache_key)
        else:
            self.samples = Utility.get_samples(cache_key)
            self.app.cache.set_samples(cache_key, self.samples)

    def test_samples_with_user_output(self) -> None:
        """Compare the user's code output with the sample's output. Results will be put into a table and
        displayed to the terminal.
        """

        test_cases = len(self.samples["input"])
        test_case_indices = []
        test_case_results = []
        sample_inputs = []
        sample_outputs = []

        for test_index in range(test_cases):
            test_case_indices.append(test_index + 1)
            sample_output = "".join(self.samples["output"][test_index])
            sample_inputs.append("".join(self.samples["input"][test_index]))
            sample_outputs.append(sample_output)
            test_case_results.append(self.get_test_case_result(sample_output, self.user_outputs[test_index]))

        rows = [test_case_indices, sample_inputs, sample_outputs, self.user_outputs, test_case_results]
        Logger.log_custom_table(TEST_CASE_OUTPUT_COLUMNS, rows)
