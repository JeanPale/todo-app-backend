from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from src.models.base import Base
from src.models.task import TaskORM
from src.models.category import CategoryORM
from src.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from src.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from src.db.session import engine, SessionLocal, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
)


def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(
            id=task_orm.id,
            title=task_orm.title,
            completed=task_orm.completed,
            )

def category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
    return CategorySchema(
            id=category_orm.id,
            name=category_orm.name,
            )

@app.get('/tasks')
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(
            title=payload.title,
            completed=False)
    db.add(new_task)
    db.commit()

    return task_orm_to_model(new_task)

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_to_update = db.get(TaskORM, task_id)
    if task_to_update:
        task_to_update.title = payload.title if payload.title else task_to_update.title
        task_to_update.completed = payload.completed if payload.completed is not None else task_to_update.completed
        db.commit()
        return task_orm_to_model(task_to_update)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task_to_delete = db.get(TaskORM, task_id)
    if task_to_delete:
        db.delete(task_to_delete)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

@app.get('/categories', response_model=list[CategorySchema])
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category) for category in categories]

@app.post('/categories', response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    category = CategoryORM(name=payload.name)

    db.add(category)
    db.commit()

    return category_orm_to_model(category)

@app.patch('/categories/{category_id}', response_model=CategorySchema)
def update_category(category_id: str, payload: CategoryUpdateSchema, db: Session = Depends(get_db)):
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category.name = payload.name if payload.name else category.name
    db.commit()
    
    return category_orm_to_model(category)

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()
