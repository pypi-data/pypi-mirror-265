# tests/test_init_paths.py
import unittest
from unittest.mock import patch, mock_open
import os
from ndpath import Ndpath


class TestInitPaths(unittest.TestCase):
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="export PATH=/usr/bin:/bin")
    def test_init_paths_from_file(self, mock_file, mock_exists):
        mock_exists.return_value = True  # Simulate environment file exists
        ndpath = Ndpath()
        paths = ndpath.init_paths()
        self.assertIn("/usr/bin", paths)
        self.assertIn("/bin", paths)

    @patch("os.path.exists")
    def test_init_paths_from_env(self, mock_exists):
        # Mock `os.path.exists` to return False when checking for the environment file
        mock_exists.side_effect = lambda x: x != os.path.expanduser("~/.pathos.env")
        with patch.dict("os.environ", {"PATH": "/usr/local/sbin:/usr/local/bin"}, clear=True):
            ndpath = Ndpath()
            paths = ndpath.init_paths()
            self.assertIn("/usr/local/sbin", paths)
            self.assertIn("/usr/local/bin", paths)


if __name__ == "__main__":
    unittest.main()
