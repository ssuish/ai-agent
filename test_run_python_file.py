import unittest
import os
from functions.run_python_file import run_python_file


class TestWriteFile(unittest.TestCase):
    def test_calculator_usage_instruction(self):
        print("Results for current directory")
        result = run_python_file("calculator", "main.py")
        print(result, "\n")

        self.assertIn("Usage: python main.py", result)

    def test_run_calculator(self):
        print("Results for current directory")
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result, "\n")

        self.assertIn("8", result)

    def test_run_calculator_test(self):
        print("Results for current directory")
        result = run_python_file("calculator", "tests.py")
        print(result, "\n")

        self.assertIn("Ran 9 tests in", result)

    def test_file_in_parent_dir(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            run_python_file("calculator", "../main.py")
        print(ctx.exception, "\n")
        self.assertIn("outside the permitted working directory", str(ctx.exception))

    def test_non_existing_file(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            run_python_file("calculator", "nonexistent.py")
        print(ctx.exception, "\n")
        self.assertIn("does not exists", str(ctx.exception))

    def test_not_a_python_file(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            run_python_file("calculator", "lorem.txt")
        print(ctx.exception, "\n")
        self.assertIn("is not a Python file", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
