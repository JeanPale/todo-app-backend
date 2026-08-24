from collections.abc import Sequence
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from src.models.category import CategoryORM

class CategoryRepository():
    def __init__(self, db: Session) -> None:
        self.db = db

    # def get_all(self) -> list[CategoryORM]:
    def get_all(self) -> Sequence[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id: str) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete(self, CategoryORM) -> None:
        self.db.delete(CategoryORM)
