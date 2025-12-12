import json
import os
from models import Task

"""
Модуль storage — отвечает за загрузку, сохранение и изменение списка задач
в JSON-файле tasks.json.
"""
FILE_PATH = "tasks.json"

def load_tasks():
    """
        Загружает задачи из файла.

        Returns:
            list[Task]: список объектов Task.
        """
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(item) for item in data]

def save_tasks(tasks):
    """
        Сохраняет список задач в JSON-файл.

        Args:
            tasks (list[Task]): список задач.
        """
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4, ensure_ascii=False)

def add_task(task):
    """
        Добавляет новую задачу и сохраняет изменения.

        Args:
            task (Task): объект задачи.
        """
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

def delete_task(task_id):
    """
        Удаляет задачу по ID.

        Args:
            task_id (str): идентификатор задачи.
        """
    tasks = load_tasks()
    tasks = [t for t in tasks if t.id != task_id]
    save_tasks(tasks)

def mark_done(task_id):
    """
        Отмечает задачу как выполненную.

        Args:
            task_id (str): идентификатор задачи.
        """
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.status = "done"
            break
    save_tasks(tasks)