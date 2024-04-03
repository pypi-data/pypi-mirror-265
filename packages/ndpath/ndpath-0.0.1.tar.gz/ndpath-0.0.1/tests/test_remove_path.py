# tests/test_remove_path.py
import unittest
from ndpath import Ndpath


class TestRemovePath(unittest.TestCase):
    def test_remove_path(self):
        ndpath = Ndpath()
        ndpath.paths = ["/usr/bin", "/bin", "/new/path"]
        ndpath.selected_index = 1  # Select "/bin" for removal
        ndpath.remove_path()
        self.assertNotIn("/bin", ndpath.paths, "The selected path should be removed")
        self.assertEqual(
            len(ndpath.paths), 2, "The paths list should contain 2 paths after removal"
        )


if __name__ == "__main__":
    unittest.main()
