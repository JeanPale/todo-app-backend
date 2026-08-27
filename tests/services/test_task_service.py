from unittest.mock import Mock

import pytest

from src.models.task import TaskORM
from src.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from src.services.task import TaskNotFound, TaskService


def test_list_tasks_returns_pydantic_models(
    task_service: TaskService, task_repository_mock: Mock
) -> None:
    task_repository_mock.get_all.return_value = [
        TaskORM(id="task-1", title="Study pytest", completed=False),
        TaskORM(id="task-2", title="Write 1st test", completed=False),
    ]

    result = task_service.list_tasks()

    assert result == [
        TaskSchema(id="task-1", title="Study pytest", completed=False),
        TaskSchema(id="task-2", title="Write 1st test", completed=False),
    ]


def test_create_task_commits_created_task(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
) -> None:
    created_task = TaskORM(id="task-1", title="New task", completed=False)
    task_repository_mock.create.return_value = created_task

    result = task_service.create_task(TaskCreateSchema(title="New task"))

    task_repository_mock.create.assert_called_once_with(title="New task")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": "New task",
        "completed": False,
    }


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_completed"),
    [
        pytest.param(
            TaskUpdateSchema(title="Update the title"),
            "Update the title",
            False,
        ),
        pytest.param(TaskUpdateSchema(completed=True), "Old task", True),
        pytest.param(
            TaskUpdateSchema(title="Done", completed=True), "Done", True
        ),
    ],
)
def test_update_task_updates_only_passed_fields(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
    payload: TaskUpdateSchema,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(id="task-1", title="Old task", completed=False)
    task_repository_mock.get_by_id.return_value = task

    result = task_service.update_task("task-1", payload)

    task_repository_mock.get_by_id.assert_called_once_with(task_id="task-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": expected_title,
        "completed": expected_completed,
    }


def test_update_task_raises_when_task_not_found(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
) -> None:
    task_repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFound):
        task_service.update_task(
            "missing-task", TaskUpdateSchema(title="Whatever")
        )

    db_mock.commit.assert_not_called()
