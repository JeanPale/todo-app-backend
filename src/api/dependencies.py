from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.services.task import TaskService
from src.services.category import CategoryService

def get_task_service(db: Session = Depends(get_db)):
    """TaskService dependency injection function"""
    return TaskService(db)

def get_category_service(db: Session = Depends(get_db)):
    """TaskService dependency injection function"""
    return CategoryService(db)
