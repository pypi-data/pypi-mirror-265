"""The Utility module contains utility methods that are used to extract unrelated logic away from
existing class members.
"""

from collections import defaultdict

from typing import List, Dict

import os
import sys
import argparse
import requests
import validators

from bs4 import BeautifulSoup

from quacktools.exceptions.argument_flags_not_valid_error import ArgumentFlagsNotValidError
from quacktools.exceptions.missing_argument_error import MissingArgumentError
from quacktools.exceptions.missing_test_file_error import MissingFileError
from quacktools.exceptions.missing_difficulty_error import MissingDifficultyError
from quacktools.exceptions.url_not_valid_error import URLNotValidError

from quacktools.constants.argument_constants import ARGUMENT_FLAGS, VALID_ARGUMENT_FLAGS
from quacktools.constants.exception_constants import MISSING_PROBLEM_TYPE_ERROR, FILE_NOT_FOUND_ERROR


class Utility:
    """The Utility instance allows existing class members to access useful functionalities."""

    @staticmethod
    def get_samples(url: str) -> Dict[str, List[str]]:
        """Returns the problem's I/O samples.

        Args:
            url (str): The input URL.

        Returns:
            Dict[str, List[str]]: The problem's I/O samples.
        """

        samples = defaultdict(list)

        request = requests.get(url, timeout=5)
        url_data = BeautifulSoup(request.text, "html.parser")
        input_divs = url_data.find_all(class_="input")
        output_divs = url_data.find_all(class_="output")

        for input_div in input_divs:
            tag = input_div.find("pre")
            samples["input"].append(tag.text.strip())

        for output_div in output_divs:
            tag = output_div.find("pre")
            samples["output"].append(tag.text.strip())

        return samples

    @staticmethod
    def get_arguments() -> argparse.Namespace:
        """Returns validated user arguments.

        Returns:
            argparse.Namespace: The validated user arguments.
        """

        parser = argparse.ArgumentParser()

        for flag, options in ARGUMENT_FLAGS.items():
            parser.add_argument(flag, **options)

        arguments = parser.parse_args()
        is_arguments_valid = False

        try:
            Utility.validate_arguments(arguments)
            is_arguments_valid = True
        except MissingArgumentError as e:
            print(f"{e.__class__.__name__}: {e}")
        except FileNotFoundError as e:
            print(f"{e.__class__.__name__}: {e}")

        if not is_arguments_valid:
            sys.exit(0)

        return arguments

    @staticmethod
    def validate_argument_flags(argument_flags: str) -> None:
        """Check if the input argument flags are valid. Exception will be thrown if the argument flags are
        invalid.

        Args:
            argument_flags (str): The user argument flags.

        Raises:
            ArgumentFlagsNotValidError: Thrown if argument flags are invalid.
        """

        if argument_flags not in VALID_ARGUMENT_FLAGS:
            raise ArgumentFlagsNotValidError()

    @staticmethod
    def validate_arguments(arguments: argparse.Namespace) -> None:
        """Check if the input arguments are valid. Exceptions will be thrown if arguments are invalid.

        Args:
            arguments (argparse.Namespace): The input arguments.

        Raises:
            FileNotFoundError: File is not found in current directory.
            MissingArgumentError: User did not input problem or contest arguments.
            MissingDifficultyError: User did not input the difficulty of the problem.
            MissingFileError: User did not input the name of the file.
        """

        if arguments.problem is None and arguments.contest is None:
            raise MissingArgumentError(MISSING_PROBLEM_TYPE_ERROR)

        if arguments.file is None:
            raise MissingFileError()

        if not os.path.exists(arguments.file):
            raise FileNotFoundError(FILE_NOT_FOUND_ERROR)

        if arguments.difficulty is None:
            raise MissingDifficultyError()

    @staticmethod
    def validate_url(url: str) -> None:
        """Validates the input URL.

        Args:
            url (str): The input URL.

        Raises:
            URLNotValidError: Thrown if URL is invalid.
        """

        if not validators.url(url) or not Utility.check_url_exists(url):
            raise URLNotValidError(url)

    @staticmethod
    def check_url_exists(url: str) -> bool:
        """Return a boolean value based on whether the URL is valid or not.

        Args:
            url (str): The input URL.

        Returns:
            bool: Boolean value based on whether URL is valid or not.
        """

        is_url_exists = False

        try:
            response = requests.head(url, timeout=5)
            is_url_exists = response.status_code == 200
        except requests.RequestException:
            pass

        return is_url_exists
