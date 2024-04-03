# tests/test_insert_path.py
import unittest
from unittest.mock import patch
import os
from ndpath import Ndpath


class TestInsertPath(unittest.TestCase):
    env_file_path = os.path.expanduser("~/.pathos.env")

    @patch("builtins.input", side_effect=["/new/path"])
    @patch("os.path.exists", return_value=True)
    def test_insert_path(self, mock_exists, mock_input):
        # Create an empty '.pathos.env' file for testing
        with open(self.env_file_path, "w") as f:
            pass

        # Test setup
        ndpath = Ndpath()
        ndpath.paths = ["/usr/bin", "/bin"]
        ndpath.selected_index = 0

        # Call the method to test
        ndpath.insert_path(False)

        # Assertions
        self.assertIn("/new/path", ndpath.paths, "The new path should be inserted correctly")
        self.assertEqual(
            ndpath.paths[1], "/new/path", "The new path should be at index 1, after '/usr/bin'"
        )

    def tearDown(self):
        # Cleanup - delete the temporary file
        if os.path.exists(self.env_file_path):
            os.remove(self.env_file_path)


if __name__ == "__main__":
    unittest.main()
