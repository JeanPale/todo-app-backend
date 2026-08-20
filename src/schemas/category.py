from pydantic import BaseModel

class CategoryCreateSchema(BaseModel):
    name: str

class CategorySchema(CategoryCreateSchema):
    id: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None

