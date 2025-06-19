from pydantic import BaseModel, Field, computed_field
from typing import List, Optional
from app.schemas.product import Product
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., example="Categoria A")
    

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    # Propiedades de navegacion
    products: Optional[List[Product]] = []
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True