import subprocess
from quacktools.constants.table_constants import TEST_CASE_OUTPUT_COLUMNS
from quacktools.utilities.logger import Logger

from quacktools.compiler.compiler import Compiler


class CPPCompiler(Compiler):
    def __init__(self, app):
        super().__init__(app)
        self.executable_file = ""

    def compile(self):
        self.executable_file = self.filename + ".exe"
        command = f"g++ {self.file} -o {self.executable_file}"
        subprocess.run(command, check=True, shell=True)

        # Display compilation errors to user

    def get_program_output(self):
        user_outputs = []

        for sample_input in self.samples["input"]:
            sample_input = "".join(sample_input).strip()
            command = f"./{self.executable_file}"

            with open("output.txt", "w") as output_file:
                subprocess.run(
                    command,
                    check=True,
                    stdout=output_file,
                    input=sample_input.encode(),
                    stderr=subprocess.PIPE,
                )

            with open("output.txt", "r") as output_file:
                user_outputs.append(output_file.read())

        self.user_outputs = user_outputs

    def test_samples_with_user_output(self):
        test_cases = len(self.samples["input"])
        test_case_indices = []
        test_case_results = []
        sample_inputs = []
        sample_outputs = []

        for test_index in range(test_cases):
            test_case_indices.append(test_index + 1)
            sample_output = "".join(self.samples["output"][test_index])
            sample_inputs.append("".join(self.samples["input"][test_index]))
            sample_outputs.append(sample_output)
            test_case_results.append("AC" if sample_output == self.user_outputs[test_index] else "WA")

        rows = zip(test_case_indices, sample_inputs, sample_outputs, self.user_outputs, test_case_results)
        Logger.log_custom_table(TEST_CASE_OUTPUT_COLUMNS, rows)
