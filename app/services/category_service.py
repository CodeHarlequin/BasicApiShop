from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import Category, CategoryCreate
from app.models.category import Category
from typing import Optional
from app.exceptions.category_exceptions import *


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)
        
    def get_all_categories(self) -> list[Category]:
        return self.repository.read_all()
    # end def
    
    def create_category(self, category_create: CategoryCreate) -> Category:
        existing_category = self.repository.read_by_name(category_create.name)
        if existing_category:
            raise DuplicateCategoryError("La categoria ya existe")
        # end if
        
        # Se mapean los valores
        category = Category(**category_create.model_dump())
        return self.repository.create(category)
    # end def
