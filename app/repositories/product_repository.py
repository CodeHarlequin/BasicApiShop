from app.repositories.base_repository import BaseRepository
from app.models.product import Product
from sqlalchemy.orm import joinedload
from app.schemas.product import ProductSearchFilter
from sqlalchemy import and_

class ProductRepository(BaseRepository[Product]):
    
    def __init__(self, db):
        super().__init__(db, Product)
    # end init
    
    def filter_products(self, filters: ProductSearchFilter) -> list[Product]:
        query = self.db.query(Product)
        conditions = []

        # Se crea el filtro apartir de los valores establecdidos en el objeto
        if filters.min_price is not None:
            conditions.append(Product.price >= filters.min_price)
        
        if filters.max_price is not None:
            conditions.append(Product.price <= filters.max_price)
        
        if filters.category_id is not None:
            conditions.append(Product.category_id == filters.category_id)

        if conditions:
            query = query.filter(and_(*conditions))

        return query.all()
    # end def
    
    def read_sorted_by_name(self) -> list[Product]:
        return (
            self.db.query(self.model)
            .options(joinedload(self.model.category))
            .order_by(self.model.name)
            .all()
        )
    # end def   
    
    def read_by_name(self, name: str) -> Product | None:
        return (
            self.db.query(self.model)
            .filter(self.model.name == name)
            .first()
        )
    # end def
    
    def update_active_status(self, product: Product) -> Product:
        product.is_active = not product.is_active
        self.db.commit()
        self.db.refresh(product)
        return product
    # end def
    
# end class