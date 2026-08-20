from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)

class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]

class TaskCreateSchema(BaseModel):
    title: str

class TaskSchema(TaskCreateSchema):
    id: str
    completed: bool

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class Book(BaseModel):
    book: str

class CategoryCreateSchema(BaseModel):
    name: str

class CategorySchema(CategoryCreateSchema):
    id: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None

book: str = "" # To prevent 500 error code

categories: list[CategorySchema] = []

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


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

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

# @app.post('/book', status_code=status.HTTP_201_CREATED)
# def post_book(payload: Book, db: Session = Depends(get_db)) -> str:
#     global book 
#     book = payload.book
#     return book
# 
# @app.get('/book')
# def get_book(db: Session = Depends(get_db)):
#     return f'Любимая книга: {book}'


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
