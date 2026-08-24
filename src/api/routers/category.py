from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_category_service
from src.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from src.services.category import CategoryNotFound, CategoryService

router = APIRouter(prefix='/categories')

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]

@router.get('', response_model=list[CategorySchema])
def get_categories(category_service: CategoryServiceDep) -> list[CategorySchema]:
    return category_service.list_categories()

@router.post('', response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, category_service: CategoryServiceDep) -> CategorySchema:
    return category_service.create_category(category_to_create=payload)

@router.patch('/{category_id}', response_model=CategorySchema)
def update_category(
        category_id: str,
        payload: CategoryUpdateSchema,
        category_service: CategoryServiceDep
) -> CategorySchema:
    try:
        return category_service.update_category(category_id=category_id, category_to_update=payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_service: CategoryServiceDep) -> None:
    try:
        return category_service.delete_category(category_id=category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

