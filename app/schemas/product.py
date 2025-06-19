from pydantic import BaseModel, Field, computed_field, model_validator
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel): 
    name: str = Field(..., example="Producto A")
    price: float = Field(..., gt=0, example=19.99)
    stock: int = Field(0, ge=0, example=100)
    is_active: bool = Field(True, example=True)

class ProductCreate(ProductBase):
    category_id: Optional[int] = None  

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ProductSearchFilter(BaseModel):
    min_price: Optional[float] = Field(None, gt=0)
    max_price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None
    
    # No es posible capturar el error
    """
    @model_validator(mode="after")
    def check_price_range(self):
        if self.min_price is not None and self.max_price is not None:
            if self.min_price > self.max_price:
                raise ValueError("El precio minimo no puede ser mayor que el maximo")
            # end if
        # end if
        
        return self
    # end def 
    """

class Product(ProductBase):
    id: int
    
    # Foreign key
    category_id: Optional[int] = None
    
    created_at: datetime
    updated_at: datetime
    
    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * 1.21

 
    class Config:
        from_attributes = True   # Para que pueda convertir de SQLAlchemy a Pydantic