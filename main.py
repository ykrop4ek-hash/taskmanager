import datetime
import uuid

class Task:
    def __init__(self, title, description="", priority="medium", due_date=None, status="pending", task_id=None):
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date or datetime.date.today().isoformat()
        self.status = status

    def to_dict(self):
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
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
            status=data.get("status", "pending"),
            task_id=data.get("id")
        )

    def __str__(self):
        return f"[{self.status.upper()}] {self.title} (Priority: {self.priority}, Due: {self.due_date})"
