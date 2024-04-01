"""This module defines the java compiler. Allows the user to compile java code.
"""

from __future__ import annotations

import subprocess

from typing import TYPE_CHECKING

from quacktools.compiler.compiler import Compiler

if TYPE_CHECKING:
    from quacktools.app.app import App


class JavaCompiler(Compiler):
    """The JavaCompiler instance allows the user to compile java code."""

    def __init__(self, app: App) -> None:
        """Initializes the compiler.

        Args:
            app (App): The application instance.
        """

        super().__init__(app)

    def compile(self) -> None:
        """Compiles the user's code."""

        command = f"javac {self.file}"
        subprocess.run(command, check=True, shell=True)

    def get_program_output(self) -> None:
        """Get the user's program's code output."""

        command = f"java {self.filename}"

        for sample_input in self.samples["input"]:
            sample_input = "".join(sample_input).strip()
            self.get_user_output(sample_input, command)
