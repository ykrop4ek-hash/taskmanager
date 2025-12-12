import sys
import os
import datetime
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Task

class TestTaskModel(unittest.TestCase):

    def test_task_creation(self):
        task = Task("Test title", "desc", "high", "2025-01-01")

        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "desc")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.due_date, "2025-01-01")
        self.assertEqual(task.status, "pending")

    def test_to_dict(self):
        task = Task("Test")
        d = task.to_dict()

        self.assertIn("title", d)
        self.assertEqual(d["title"], "Test")

    def test_from_dict(self):
        data = {
            "id": "123",
            "title": "AAA",
            "description": "BBB",
            "priority": "low",
            "due_date": "2030-01-01",
            "status": "done"
        }

        task = Task.from_dict(data)
        self.assertEqual(task.id, "123")
        self.assertEqual(task.status, "done")


if __name__ == "__main__":
    unittest.main()
