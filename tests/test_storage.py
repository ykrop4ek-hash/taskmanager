import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage
from models import Task
import json


class TestStorage(unittest.TestCase):

    def setUp(self):
        # создаем временный файл
        self.test_file = "test_tasks.json"
        storage.FILE_PATH = self.test_file  # Или используйте storage.set_file_path() если есть

        # очищаем перед тестами
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        # удаляем после тестов
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_and_load(self):
        t = Task("Test")
        storage.add_task(t)

        tasks = storage.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test")

    def test_delete_task(self):
        t1 = Task("A", task_id="1")
        t2 = Task("B", task_id="2")
        storage.save_tasks([t1, t2])

        storage.delete_task("1")
        tasks = storage.load_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, "2")

    def test_mark_done(self):
        t = Task("A", task_id="1")
        storage.save_tasks([t])

        storage.mark_done("1")
        tasks = storage.load_tasks()

        self.assertEqual(tasks[0].status, "done")

    def test_invalid_json(self):  # ← ДОБАВЛЕН ОТСТУП! Этот метод должен быть внутри класса
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json }")

        with self.assertRaises(json.JSONDecodeError):
            storage.load_tasks()


if __name__ == "__main__":
    unittest.main()
