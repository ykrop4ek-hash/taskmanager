from models import Task
import storage

"""
Модуль commands — содержит функции, выполняющие команды CLI.
"""

def add_task(args):
    """
        Создаёт новую задачу и сохраняет её.

        Args:
            args (Namespace): аргументы CLI.
        """
    task = Task(
        title=args.title,
        description=args.description,
        priority=args.priority,
        due_date=args.due_date
    )
    storage.add_task(task)
    print(f"✅ Задача добавлена: {task.title}")

def list_tasks(args):
    """
        Выводит список задач с возможностью фильтрации по статусу и приоритету.

        Args:
            args (Namespace): аргументы CLI.
        """
    tasks = storage.load_tasks()
    filtered = tasks

    if args.status:
        filtered = [t for t in filtered if t.status == args.status]
    if args.priority:
        filtered = [t for t in filtered if t.priority == args.priority]

    if not filtered:
        print("Нет задач по заданным критериям.")
        return

    for t in filtered:
        print(f"{t.id[:8]} | {t}")

def mark_done(args):
    """
        Отмечает задачу как выполненную.

        Args:
            args (Namespace): аргументы CLI.
        """
    storage.mark_done(args.id)
    print(f"✅ Задача {args.id} отмечена как выполненная.")

def delete_task(args):
    """
        Удаляет задачу по ID.

        Args:
            args (Namespace): аргументы CLI.
        """
    storage.delete_task(args.id)
    print(f"🗑️ Задача {args.id} удалена.")
