# commands.py
"""
Модуль commands — содержит функции, выполняющие команды CLI.
"""

from models import Task
import storage


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
    print(f"✅ Задача добавлена: {task.title} (ID: {task.id[:8]})")


def list_tasks(args):
    """
    Выводит список задач с возможностью фильтрации по статусу и приоритету.

    Args:
        args (Namespace): аргументы CLI.
    """
    # Создаем словарь фильтров из аргументов
    filters = {}

    # Проверяем, передан ли аргумент status (опциональный)
    if hasattr(args, 'status') and args.status:
        filters['status'] = args.status

    # Проверяем, передан ли аргумент priority (опциональный)
    if hasattr(args, 'priority') and args.priority:
        filters['priority'] = args.priority

    # Загружаем задачи с фильтрами
    tasks = storage.load_tasks(filters)

    # Если задач нет
    if not tasks:
        if filters:
            print("📭 Нет задач по заданным критериям.")
        else:
            print("📭 Список задач пуст.")
        return

    # Выводим заголовок
    if filters:
        filter_info = []
        if 'status' in filters:
            filter_info.append(f"статус: {filters['status']}")
        if 'priority' in filters:
            filter_info.append(f"приоритет: {filters['priority']}")
        print(f"📋 Найдено задач: {len(tasks)} (фильтры: {', '.join(filter_info)})")
    else:
        print(f"📋 Всего задач: {len(tasks)}")

    print("-" * 60)

    # Выводим каждую задачу
    for t in tasks:
        # Форматируем дату выполнения
        due_str = "нет срока"
        if t.due_date:
            if isinstance(t.due_date, str):
                due_str = t.due_date
            elif hasattr(t.due_date, 'isoformat'):
                due_str = t.due_date.isoformat()
            else:
                due_str = str(t.due_date)

        # Форматируем статус с иконкой
        status_icon = "✅" if t.status == "done" else "⏳"

        # Форматируем приоритет
        priority_icon = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }.get(t.priority, "⚪")

        print(f"ID: {t.id[:8]}")
        print(f"  {status_icon} {t.title}")
        print(f"  {priority_icon} Приоритет: {t.priority}")
        print(f"  📅 Срок: {due_str}")

        if t.description:
            print(f"  📝 Описание: {t.description}")

        # Добавляем информацию о дате создания, если есть
        if hasattr(t, 'created_at') and t.created_at:
            if hasattr(t.created_at, 'strftime'):
                created_str = t.created_at.strftime("%Y-%m-%d %H:%M")
            else:
                created_str = str(t.created_at)[:16]
            print(f"  🕐 Создана: {created_str}")

        print("-" * 60)


def mark_done(args):
    """
    Отмечает задачу как выполненную.

    Args:
        args (Namespace): аргументы CLI.
    """
    if storage.mark_done(args.id):
        print(f"✅ Задача {args.id} отмечена как выполненная.")
    else:
        print(f"❌ Задача с ID {args.id} не найдена.")


def delete_task(args):
    """
    Удаляет задачу по ID.

    Args:
        args (Namespace): аргументы CLI.
    """
    if storage.delete_task(args.id):
        print(f"🗑️ Задача {args.id} удалена.")
    else:
        print(f"❌ Задача с ID {args.id} не найдена.")