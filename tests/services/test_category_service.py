from unittest.mock import Mock

import pytest

from src.models.category import CategoryORM
from src.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from src.services.category import CategoryNotFound, CategoryService


def test_list_categories_returns_pydantic_models(
    category_service: CategoryService, category_repository_mock: Mock
) -> None:
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="category-1", name="一番"),
        CategoryORM(id="category-2", name="二番"),
    ]

    result = category_service.list_categories()

    assert result == [
        CategorySchema(id="category-1", name="一番"),
        CategorySchema(id="category-2", name="二番"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    created_category = CategoryORM(id="category-1", name="New category")
    category_repository_mock.create.return_value = created_category

    result = category_service.create_category(
        CategoryCreateSchema(name="New category")
    )

    category_repository_mock.create.assert_called_once_with(
        name="New category"
    )
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "New category",
    }


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdateSchema(name="Update the name"),
            "Update the name",
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    payload: CategoryUpdateSchema,
    expected_name: str,
) -> None:
    category = CategoryORM(id="category-1", name="Old category")
    category_repository_mock.get_by_id.return_value = category

    result = category_service.update_category("category-1", payload)

    category_repository_mock.get_by_id.assert_called_once_with(
        category_id="category-1"
    )
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": expected_name,
    }


def test_update_category_raises_when_category_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):
        category_service.update_category(
            "missing-category", CategoryUpdateSchema(name="Who_cares")
        )

    db_mock.commit.assert_not_called()


def test_delete_category_raises_when_category_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):
        category_service.delete_category("missing-task")

    db_mock.commit.assert_not_called()
