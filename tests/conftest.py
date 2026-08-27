from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from src.repositories.category import CategoryRepository
from src.repositories.task import TaskRepository
from src.services.category import CategoryService
from src.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    return Mock(spec=Session)


@pytest.fixture
def task_repository_mock() -> Mock:
    return Mock(spec=TaskRepository)


@pytest.fixture
def category_repository_mock() -> Mock:
    return Mock(spec=CategoryRepository)


@pytest.fixture
def task_service(db_mock: Mock, task_repository_mock: Mock) -> TaskService:
    task_service = TaskService(db_mock)
    task_service.task_repository = task_repository_mock
    return task_service


@pytest.fixture
def category_service(
    db_mock: Mock, category_repository_mock: Mock
) -> CategoryService:
    category_service = CategoryService(db_mock)
    category_service.category_repository = category_repository_mock
    return category_service
