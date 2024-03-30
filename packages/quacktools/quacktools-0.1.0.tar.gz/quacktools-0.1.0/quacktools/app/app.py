import sys

from quacktools.compiler.cpp_compiler import CPPCompiler
from quacktools.utilities.utility import Utility

from quacktools.exceptions.url_not_valid_error import URLNotValidError

from quacktools.constants.argument_constants import URL_PREFIX


class App:
    def __init__(self):
        self.arguments = Utility.get_arguments()
        self.compiler = self.get_compiler()
        self.url = self.get_url()

    def run(self):
        self.compiler.initialize()
        self.compiler.compile()
        self.compiler.get_program_output()
        self.compiler.test_samples_with_user_output()

    def get_problem_number(self):
        if self.arguments.problem is not None:
            return self.arguments.problem

        return self.arguments.contest

    def get_url(self):
        url = None
        problem_number = self.get_problem_number()
        difficulty = self.arguments.difficulty

        if self.arguments.contest is not None:
            url = URL_PREFIX + f"/contest/{problem_number}/problem/{difficulty}"
        else:
            url = URL_PREFIX + f"/problemset/problem/{problem_number}/{difficulty}"

        is_url_valid = False

        try:
            Utility.validate_url(url)
            is_url_valid = True
        except URLNotValidError as e:
            print(f"{e.__class__.__name__}: {e}")

        if not is_url_valid:
            sys.exit(0)

        return url

    def get_compiler(self):
        extension = self.arguments.file.split(".")[1]

        match extension:
            case "cpp":
                return CPPCompiler(self)

        return None
