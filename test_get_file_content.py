import unittest
import os
from functions.get_file_content import get_file_content
from config import CHARACTER_LIMIT


class TestGetFileContent(unittest.TestCase):
    def test_truncation_message_when_file_exceeds_character_limit(self):
        print("Results for current directory")
        result = get_file_content("calculator", "lorem.txt")
        content = result.split("[...")[0] if "[..." in result else result

        self.assertEqual(len(content), CHARACTER_LIMIT)
        if "[..." in result:
            self.assertIn("truncated", result)

    def test_short_file_returns_full_content_without_truncation(self):
        print("Results for current directory")
        result = get_file_content("calculator", "main.py")
        content = result.split("[...")[0] if "[..." in result else result

        print(content)

        self.assertNotEqual(len(content), CHARACTER_LIMIT)
        if "[..." in result:
            self.assertIn("truncated", result)

    def test_file_in_nested_path_returns_content_below_limit(self):
        print("Results for current directory")
        result = get_file_content("calculator", "pkg/calculator.py")
        content = result.split("[...")[0] if "[..." in result else result

        print(content)

        self.assertNotEqual(len(content), CHARACTER_LIMIT)
        if "[..." in result:
            self.assertIn("truncated", result)

    def test_raises_when_file_path_outside_working_directory(self):
        print("Results for current directory")

        with self.assertRaises(Exception) as ctx:
            get_file_content("calculator", "/bin/cat")
        print(ctx.exception, "\n")
        self.assertIn("Error:", str(ctx.exception))

    def test_raises_when_file_does_not_exist(self):
        print("Results for current directory")
        with self.assertRaises(Exception) as ctx:
            get_file_content("calculator", "pkg/does_not_exist.py")
        print(ctx.exception, "\n")
        self.assertIn("Error:", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
