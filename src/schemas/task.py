from pydantic import BaseModel

class TaskCreateSchema(BaseModel):
    title: str

class TaskSchema(TaskCreateSchema):
    id: str
    completed: bool

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

