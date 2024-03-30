import os
import sys
import requests
import validators

from bs4 import BeautifulSoup
from argparse import ArgumentParser
from collections import defaultdict

from quacktools.exceptions.missing_argument_error import MissingArgumentError
from quacktools.exceptions.missing_test_file_error import MissingFileError
from quacktools.exceptions.missing_difficulty_error import MissingDifficultyError
from quacktools.exceptions.file_not_found_error import FileNotFoundError
from quacktools.exceptions.url_not_valid_error import URLNotValidError

from quacktools.constants.argument_constants import ARGUMENT_FLAGS
from quacktools.constants.exception_constants import MISSING_PROBLEM_TYPE_ERROR


class Utility:
    @staticmethod
    def get_samples(url):
        samples = defaultdict(list)

        request = requests.get(url)
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
    def get_arguments():
        parser = ArgumentParser()

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
    def validate_arguments(arguments):
        if arguments.problem is None and arguments.contest is None:
            raise MissingArgumentError(MISSING_PROBLEM_TYPE_ERROR)

        if arguments.file is None:
            raise MissingFileError()

        if arguments.file not in os.listdir():
            raise FileNotFoundError()

        if arguments.difficulty is None:
            raise MissingDifficultyError()

    @staticmethod
    def validate_url(url):
        url_not_valid_error = f"'{url}' is not a not a valid URL."

        if not validators.url(url) or not Utility.check_url_exists(url):
            raise URLNotValidError(url_not_valid_error)

    @staticmethod
    def check_url_exists(url):
        is_url_exists = False

        try:
            response = requests.head(url, timeout=5)
            is_url_exists = response.status_code == 200
        except requests.RequestException:
            pass

        return is_url_exists
