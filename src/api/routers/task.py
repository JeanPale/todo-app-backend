from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_task_service
from src.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from src.services.task import TaskNotFound, TaskService

router = APIRouter(prefix='/tasks')

TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]

@router.get('', response_model=list[TaskSchema])
def read_tasks(task_service: TaskServiceDep) -> list[TaskSchema]:
    return task_service.list_tasks()

@router.post('', response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
        payload: TaskCreateSchema,
        task_service: TaskServiceDep
) -> TaskSchema:
    return task_service.create_task(task_to_create=payload)

@router.patch('/{task_id}', response_model=TaskSchema)
def update_task(
        task_id: str,
        payload: TaskUpdateSchema,
        task_service: TaskServiceDep
) -> TaskSchema:
    try:
        return task_service.update_task(task_id=task_id, task_to_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskServiceDep):
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
