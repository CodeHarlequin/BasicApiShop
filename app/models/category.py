from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String, index=True)
    
    # Propiedades de navegacion
    products = relationship("Product", back_populates="category")