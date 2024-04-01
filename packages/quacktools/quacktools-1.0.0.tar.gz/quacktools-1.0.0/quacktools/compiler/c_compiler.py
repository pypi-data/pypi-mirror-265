"""This module defines the c compiler. Allows the user to compile c code.
"""

from __future__ import annotations

import subprocess

from typing import TYPE_CHECKING

from quacktools.compiler.compiler import Compiler

if TYPE_CHECKING:
    from quacktools.app.app import App


class CCompiler(Compiler):
    """The CCompiler instance allows the user to compile c code.

    Attributes:
        executable_file (str): Description
    """

    def __init__(self, app: App) -> None:
        """Initializes the compiler.

        Args:
            app (App): The application instance.
        """

        super().__init__(app)

        self.executable_file = ""

    def compile(self) -> None:
        """Compiles the user's code."""

        self.executable_file = self.filename + ".exe"
        command = f"gcc {self.file} -o {self.executable_file}"
        subprocess.run(command, check=True, shell=True)

        # Display compilation errors to user

    def get_program_output(self) -> None:
        """Get the user's program's code output."""

        command = f"./{self.executable_file}"

        for sample_input in self.samples["input"]:
            sample_input = "".join(sample_input).strip()
            self.get_user_output(sample_input, command)
