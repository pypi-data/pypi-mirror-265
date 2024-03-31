"""The Logger module will log events to the terminal."""

from typing import List, Iterator, Any

from prettytable import PrettyTable, ALL


class Logger:
    """The logger instance is a singleton instance. It logs all important events to the terminal."""

    @staticmethod
    def log_custom_table(headers: List[str], rows: Iterator[Any]) -> None:
        """Log custom table to the terminal.

        Args:
            headers (List[str]): Description
            rows (Iterator[Tuple[str, ...]]): Description
        """

        table = PrettyTable(headers)
        table.add_rows(rows)
        table.hrules = ALL
        table.align = "l"

        print(table)
