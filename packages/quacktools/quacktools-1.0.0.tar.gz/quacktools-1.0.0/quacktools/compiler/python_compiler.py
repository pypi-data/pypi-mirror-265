"""This module defines the python compiler. Allows the user to interpret python code.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from quacktools.compiler.compiler import Compiler

if TYPE_CHECKING:
    from quacktools.app.app import App


class PythonCompiler(Compiler):
    """The PythonCompiler instance allows the user to interpret python code."""

    def __init__(self, app: App) -> None:
        """Initializes the compiler.

        Args:
            app (App): The application instance.
        """

        super().__init__(app)

    def get_program_output(self) -> None:
        """Get the user's program's code output."""

        command = f"python3 {self.file}"

        for sample_input in self.samples["input"]:
            sample_input = "".join(sample_input).strip()
            self.get_user_output(sample_input, command)
