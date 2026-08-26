from pydantic import BaseModel, ConfigDict


class CategoryCreateSchema(BaseModel):
    name: str


class CategorySchema(CategoryCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None
