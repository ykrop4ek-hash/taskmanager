import argparse
import commands

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(title="Команды")

    # Добавление
    add_parser = subparsers.add_parser("add", help="Добавить задачу")
    add_parser.add_argument("--title", required=True, help="Название задачи")
    add_parser.add_argument("--description", default="", help="Описание задачи")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium", help="Приоритет")
    add_parser.add_argument("--due_date", help="Срок (YYYY-MM-DD)")
    add_parser.set_defaults(func=commands.add_task)

    # Список
    list_parser = subparsers.add_parser("list", help="Показать список задач")
    list_parser.add_argument("--status", choices=["pending", "done"], help="Фильтр по статусу")
    list_parser.add_argument("--priority", choices=["low", "medium", "high"], help="Фильтр по приоритету")
    list_parser.set_defaults(func=commands.list_tasks)

    # Завершить
    done_parser = subparsers.add_parser("done", help="Отметить задачу как выполненную")
    done_parser.add_argument("--id", required=True, help="ID задачи")
    done_parser.set_defaults(func=commands.mark_done)

    # Удалить
    del_parser = subparsers.add_parser("delete", help="Удалить задачу")
    del_parser.add_argument("--id", required=True, help="ID задачи")
    del_parser.set_defaults(func=commands.delete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
