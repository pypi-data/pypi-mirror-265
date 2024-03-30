from prettytable import PrettyTable, ALL


class Logger:
    @staticmethod
    def log_custom_table(headers, rows):
        table = PrettyTable(headers)
        table.add_rows(rows)
        table.hrules = ALL
        table.align = "l"

        print(table)
