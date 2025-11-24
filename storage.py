import json
import os
from models import Task

FILE_PATH = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(item) for item in data]

def save_tasks(tasks):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4, ensure_ascii=False)

def add_task(task):
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t.id != task_id]
    save_tasks(tasks)

def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.status = "done"
            break
    save_tasks(tasks)