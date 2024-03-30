import os

from abc import ABC, abstractmethod

from quacktools.utilities.utility import Utility


class Compiler(ABC):
    def __init__(self, app):
        self.app = app
        self.file = None
        self.filename = None
        self.extension = None
        self.user_outputs = None
        self.samples = None
        self.test_cases_passed = 0

    @abstractmethod
    def compile(self):
        pass

    @abstractmethod
    def get_program_output(self):
        pass

    def initialize(self):
        self.set_file()
        self.set_samples()

    def set_file(self):
        self.file = self.app.arguments.file
        self.filename, self.extension = self.app.arguments.file.split(".")

    def set_samples(self):
        self.samples = Utility.get_samples(self.app.url)
