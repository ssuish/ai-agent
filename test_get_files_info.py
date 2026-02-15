import unittest
import os
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_current_dir(self):
        print("Results for current directory")
        result = get_files_info("calculator", ".")
        print(result, "\n")
        self.assertIsNotNone(result)
        self.assertIn("main.py", result)
        self.assertIn("tests.py", result)
        self.assertIn("pkg", result)

    def test_pkg_dir(self):
        print("Results for current directory")
        result = get_files_info("calculator", "pkg")
        print(result, "\n")
        self.assertIsNotNone(result)
        self.assertIn("calculator.py", result)
        self.assertIn("render.py", result)

    def test_bin_dir_raises_outside_working_directory(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            get_files_info("calculator", "/bin")
        print(ctx.exception, "\n")
        self.assertIn("outside the permitted working directory", str(ctx.exception))

    def test_parent_dir_raises_outside_working_directory(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            get_files_info("calculator", "../")
        print(ctx.exception, "\n")
        self.assertIn("outside the permitted working directory", str(ctx.exception))

    def test_nonexistent_path_raises(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            get_files_info("calculator", "nonexistent_subdir")
        print(ctx.exception, "\n")
        self.assertIn("is not a directory", str(ctx.exception))

    def test_file_path_raises_not_a_directory(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            get_files_info("calculator", "main.py")
        print(ctx.exception, "\n")
        self.assertIn("is not a directory", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()