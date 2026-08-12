from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class BookSchema(BaseModel):
    book: str

tasks: list[TaskSchema] = []

book: str = "" # To prevent 500 error code

@app.get('/tasks')
def read_tasks():
    return tasks

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()),
                          title=payload.title,
                          completed=False)
    tasks.append(new_task)
    return new_task

@app.post('/book')
def post_book(payload: BookSchema) -> str:
    global book 
    book = payload.book
    return book

@app.get('/book')
def get_book():
    return f'Любимая книга: {book}'

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema):
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
