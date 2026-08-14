from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
)


class TaskCreate(BaseModel):
    title: str

class Task(TaskCreate):
    id: str
    completed: bool

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class Book(BaseModel):
    book: str

class CategoryCreate(BaseModel):
    name: str

class Category(CategoryCreate):
    id: str

class CategoryUpdate(BaseModel):
    name: str | None = None

tasks: list[Task] = []

book: str = "" # To prevent 500 error code

categories: list[Category] = []

@app.get('/tasks')
def read_tasks():
    return tasks

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    new_task = Task(
            id=str(uuid4()),
            title=payload.title,
            completed=False)

    tasks.append(new_task)
    return new_task

@app.post('/book', status_code=status.HTTP_201_CREATED)
def post_book(payload: Book) -> str:
    global book 
    book = payload.book
    return book

@app.get('/book')
def get_book():
    return f'Любимая книга: {book}'

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

@app.get('/categories')
def get_categories():
    return categories

@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate) -> Category:
    new_category = Category(
            id=str(uuid4()),
            name=payload.name)

    categories.append(new_category)
    return new_category

@app.patch('/categories/{category_id}')
def update_category(category_id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name
            return category

@app.delete('/categories/{category_id}')
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
