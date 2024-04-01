"""This module defines the c sharp compiler. Allows the user to compile c sharp code.
"""

from __future__ import annotations

import subprocess

from typing import TYPE_CHECKING

from quacktools.compiler.compiler import Compiler

if TYPE_CHECKING:
    from quacktools.app.app import App


class CSharpCompiler(Compiler):
    """The CSharpCompiler instance allows the user to compile c sharp code."""

    def __init__(self, app: App) -> None:
        """Initializes the compiler.

        Args:
            app (App): The application instance.
        """

        super().__init__(app)

    def compile(self) -> None:
        """Compiles the user's code."""

        command = f"cd {self.filename} && dotnet build"
        subprocess.run(command, check=True, shell=True)

    def get_program_output(self) -> None:
        """Get the user's program's code output."""

        command = f"cd {self.filename} && dotnet run"

        for sample_input in self.samples["input"]:
            sample_input = "".join(sample_input).strip()
            self.get_user_output(sample_input, command)
