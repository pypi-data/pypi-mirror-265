"""This module contains the main driver code."""

from quacktools.app.app import App


def main():
    """Gets called upon using the 'quack' command from the CLI."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
