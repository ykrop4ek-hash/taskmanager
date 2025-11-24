from models import Task
import storage

def add_task(args):
    task = Task(
        title=args.title,
        description=args.description,
        priority=args.priority,
        due_date=args.due_date
    )
    storage.add_task(task)
    print(f"✅ Задача добавлена: {task.title}")

def list_tasks(args):
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
    storage.mark_done(args.id)
    print(f"✅ Задача {args.id} отмечена как выполненная.")

def delete_task(args):
    storage.delete_task(args.id)
    print(f"🗑️ Задача {args.id} удалена.")
