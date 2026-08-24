from collections.abc import Sequence
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from src.models.task import TaskORM

class TaskRepository():
    def __init__(self, db: Session) -> None:
        self.db = db

    # def get_all(self) -> list[TaskORM]:
    def get_all(self) -> Sequence[TaskORM]:
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id: str) -> TaskORM | None:
        return self.db.get(TaskORM, task_id)

    def create(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete(self, TaskORM) -> None:
        self.db.delete(TaskORM)
