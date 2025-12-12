import datetime
import uuid
"""
Модуль models — определяет модель данных задачи (Task).
"""
class Task:
    """
    Класс задачи.

    Attributes:
        id (str): уникальный ID задачи.
        title (str): название задачи.
        description (str): описание.
        priority (str): приоритет (low/medium/high).
        due_date (str): срок выполнения (YYYY-MM-DD).
        status (str): статус ('pending' или 'done').
    """
    def __init__(self, title, description="", priority="medium", due_date=None, status="pending", task_id=None):
        """
                Инициализация объекта Task.

                Args:
                    title (str): название задачи.
                    description (str, optional): описание. Defaults to "".
                    priority (str, optional): приоритет. Defaults to "medium".
                    due_date (str, optional): срок выполнения. Defaults to today.
                    status (str, optional): статус. Defaults to "pending".
                    task_id (str, optional): явный ID. Defaults to uuid4().
                """
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date or datetime.date.today().isoformat()
        self.status = status

    def to_dict(self):
        """
                Преобразует задачу в словарь.

                Returns:
                    dict: представление объекта.
                """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """
                Создаёт объект Task из словаря.

                Args:
                    data (dict): данные задачи.

                Returns:
                    Task: объект задачи.
                """
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
            status=data.get("status", "pending"),
            task_id=data.get("id")
        )

    def __str__(self):
        """Возвращает строковое представление задачи."""
        return f"[{self.status.upper()}] {self.title} (Priority: {self.priority}, Due: {self.due_date})"
