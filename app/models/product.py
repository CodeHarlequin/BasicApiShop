from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.category import Category
from app.models.base_model import BaseModel

class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    # Claves foraneas
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Propiedades de navegacion
    category = relationship("Category", back_populates="products")
