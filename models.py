import datetime
import uuid
from database import db
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
    def __init__(self, title, description="", priority="medium", due_date=None, status="pending", task_id=None, created_at=None, updated_at=None):
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
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        """Сохраняет задачу в базу данных"""
        query = """
        INSERT INTO tasks (id, title, description, priority, due_date, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            priority = EXCLUDED.priority,
            due_date = EXCLUDED.due_date,
            status = EXCLUDED.status,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id, created_at, updated_at;
        """

        db.execute_query(query, (
            self.id, self.title, self.description, self.priority,
            self.due_date, self.status,
            self.created_at or datetime.datetime.now(),
            datetime.datetime.now()
        ))
        db.commit()

        # Получаем обновленные данные
        result = db.cursor.fetchone()
        if result:
            self.created_at = result['created_at']
            self.updated_at = result['updated_at']

        return self

    @staticmethod
    def mark_done_by_short_id(short_id):
        """Отмечает задачу как выполненную по короткому ID (первым 8 символам)"""
        query = "UPDATE tasks SET status = 'done', updated_at = CURRENT_TIMESTAMP WHERE id LIKE %s"
        db.execute_query(query, (f"{short_id}%",))
        db.commit()
        return db.cursor.rowcount > 0

    def delete(self):
        """Удаляет задачу из базы данных"""
        query = "DELETE FROM tasks WHERE id = %s"
        db.execute_query(query, (self.id,))
        db.commit()

    def mark_as_done(self):
        """Отмечает задачу как выполненную"""
        self.status = "done"
        query = "UPDATE tasks SET status = 'done', updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        db.execute_query(query, (self.id,))
        db.commit()

    @staticmethod
    def get_all(filters=None):
        """Получает все задачи с опциональными фильтрами"""
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if filters:
            if filters.get('status'):
                query += " AND status = %s"
                params.append(filters['status'])
            if filters.get('priority'):
                query += " AND priority = %s"
                params.append(filters['priority'])
            if filters.get('due_date'):
                query += " AND due_date = %s"
                params.append(filters['due_date'])

        query += " ORDER BY created_at DESC"
        db.execute_query(query, params)
        tasks_data = db.cursor.fetchall()

        tasks = []
        for data in tasks_data:
            task = Task(
                title=data['title'],
                description=data['description'],
                priority=data['priority'],
                due_date=data['due_date'].isoformat() if data['due_date'] else None,
                status=data['status'],
                task_id=data['id'],
                created_at=data['created_at'],
                updated_at=data['updated_at']
            )
            tasks.append(task)

        return tasks

    @staticmethod
    def get_by_id(task_id):
        """Получает задачу по ID"""
        query = "SELECT * FROM tasks WHERE id = %s"
        db.execute_query(query, (task_id,))
        data = db.cursor.fetchone()

        if data:
            return Task(
                title=data['title'],
                description=data['description'],
                priority=data['priority'],
                due_date=data['due_date'].isoformat() if data['due_date'] else None,
                status=data['status'],
                task_id=data['id'],
                created_at=data['created_at'],
                updated_at=data['updated_at']
            )
        return None

    @staticmethod
    def delete_by_id(task_id):
        """Удаляет задачу по ID"""
        query = "DELETE FROM tasks WHERE id = %s"
        db.execute_query(query, (task_id,))
        db.commit()
        return db.cursor.rowcount > 0

    @staticmethod
    def mark_done_by_id(task_id):
        """Отмечает задачу как выполненную по ID"""
        query = "UPDATE tasks SET status = 'done', updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        db.execute_query(query, (task_id,))
        db.commit()
        return db.cursor.rowcount > 0

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
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
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
