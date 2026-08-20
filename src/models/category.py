from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]
