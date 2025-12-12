import unittest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import commands
import storage
from models import Task


class Args:
    """Простой объект для имитации Namespace из argparse"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestCommands(unittest.TestCase):

    @patch("builtins.print")
    def test_add_task(self, mock_print):
        args = Args(title="Test", description="Desc", priority="low", due_date="2030-01-01")

        commands.add_task(args)

        mock_print.assert_called_with("✅ Задача добавлена: Test")

    @patch("builtins.print")
    def test_list_tasks_empty(self, mock_print):
        args = Args(status=None, priority=None)
        storage.save_tasks([])

        commands.list_tasks(args)
        mock_print.assert_called_with("Нет задач по заданным критериям.")


if __name__ == "__main__":
    unittest.main()

