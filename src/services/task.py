from sqlalchemy.orm import Session

from src.repositories.task import TaskRepository
from src.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskNotFound(Exception):
    pass


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_to_create: TaskCreateSchema) -> TaskSchema:
        task_orm = self.task_repository.create(title=task_to_create.title)

        self.db.commit()
        return TaskSchema.model_validate(task_orm)

    def update_task(
        self, task_id: str, task_to_update: TaskUpdateSchema
    ) -> TaskSchema:
        task_to_update_orm = self.task_repository.get_by_id(task_id=task_id)
        if task_to_update_orm:
            if task_to_update.title is not None:
                task_to_update_orm.title = task_to_update.title
            if task_to_update.completed is not None:
                task_to_update_orm.completed = task_to_update.completed

            self.db.commit()
            return TaskSchema.model_validate(task_to_update_orm)
        else:
            raise TaskNotFound(f"Task (id: {task_id}) not found")

    def delete_task(self, task_id: str) -> None:
        task_to_delete_orm = self.task_repository.get_by_id(task_id=task_id)
        if task_to_delete_orm:
            self.task_repository.delete(task_to_delete_orm)
            self.db.commit()
        else:
            raise TaskNotFound(f"Task (id: {task_id}) not found")
