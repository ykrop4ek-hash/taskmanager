import unittest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main

class TestCLI(unittest.TestCase):

    @patch("commands.add_task")
    def test_add_command(self, mock_add):
        test_args = ["add", "--title", "Test"]
        with patch("sys.argv", ["main.py"] + test_args):
            main.main()

        mock_add.assert_called_once()

    @patch("commands.list_tasks")
    def test_list_command(self, mock_list):
        test_args = ["list"]
        with patch("sys.argv", ["main.py"] + test_args):
            main.main()

        mock_list.assert_called_once()


if __name__ == "__main__":
    unittest.main()

