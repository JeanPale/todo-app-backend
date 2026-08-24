from sqlalchemy.orm import Session

from src.repositories.category import CategoryRepository
from src.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema

class CategoryNotFound(Exception):
    pass

class CategoryService():
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all()
        
        return [CategorySchema.model_validate(category) for category in categories_orm]

    def create_category(self, category_to_create: CategoryCreateSchema) -> CategorySchema:
        category_orm = self.category_repository.create(name=category_to_create.name)

        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(self, category_id: str, category_to_update: CategoryUpdateSchema) -> CategorySchema:
        category_to_update_orm = self.category_repository.get_by_id(category_id=category_id)
        if category_to_update_orm:
            if category_to_update.name is not None:
                category_to_update_orm.name = category_to_update.name

            self.db.commit()
            return CategorySchema.model_validate(category_to_update_orm)
        else:
            raise CategoryNotFound(f'Category {category_id} not found')

    def delete_category(self, category_id: str) -> None:
        category_to_delete_orm = self.category_repository.get_by_id(category_id=category_id)
        if category_to_delete_orm:
            self.category_repository.delete(category_to_delete_orm)
            self.db.commit()
        else:
            raise CategoryNotFound(f'Category {category_id} not found')
