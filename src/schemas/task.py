from pydantic import BaseModel, ConfigDict

class TaskCreateSchema(BaseModel):
    title: str

class TaskSchema(TaskCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: str
    completed: bool

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

