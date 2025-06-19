from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.schemas.product import Product, ProductCreate, ProductSearchFilter
from app.models.product import Product
from fastapi import HTTPException
from typing import Optional
from app.exceptions.product_exceptions import *
from app.exceptions.category_exceptions import *

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def get_all_products(self) -> list[Product]: # Ordenando por nombre
        products = []
        
        try:
            products = self.repository.read_sorted_by_name()
        except Exception as e: 
            # En caso de un error inesparado se devolvera una lista vacia 
            # no hay conexion con la base de datos
            # TODO: Implementar un logger
            pass
        # end try
        
        return products
    # end def
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        # Valida que que el id sea valido antes de pasarlo al repositorio
        if product_id < 0:
            raise ValueError("El id debe ser valido")
        # end if
        
        read_product = self.repository.read_by_id(product_id)
        if not read_product:
            raise ProductNotFoundError("Producto no encontrado")
        # end if
        
        return read_product
    # end def
    
    def create_product(self, product_create: ProductCreate):
        if product_create.price <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        # end if
        
        existing_product = self.repository.read_by_name(product_create.name)
        if existing_product:
            raise DuplicateProductError("El producto ya existe")
        # end if
        
        # Validar otros campos como category_id
        if product_create.category_id is not None:
            category = self.repository.read_by_id(product_create.category_id)
            if not category:
                raise CategoryNotFoundError("La categoria no existe")
            # end if
        # end if
        
        # Se mapean los valores
        product = Product(**product_create.model_dump()) 
        return self.repository.create(product)
    # end def
    
    def delete_product(self, product_id: int) -> bool:
        product = self.repository.read_by_id(product_id)
        if not product:
            raise ProductNotFoundError("Producto no encontrado")
        # end if
        
        response = self.repository.delete(product_id)
        
        # Validacion del resultado
        if not response:
            raise FailedProductDeletionError("No se pudo eliminar el producto")
        # end if
        
        return response
    # end def
    
    def update_product(self, product_id: int, product_data: ProductCreate) -> Product:
        """Actualiza un producto existente con los datos proporcionados.

            Args:
                product_id (int): El ID del producto que se desea actualizar.
                product_data (ProductCreate): Un objeto que contiene los datos actualizados del producto.

            Returns:
                Product: El objeto del producto actualizado.

            Raises:
                ProductNotFoundError: Si no existe un producto con el ID proporcionado.
                ValueError: Si los datos del producto contienen valores no válidos, como un precio no positivo.
                DuplicateProductError: Si ya existe otro producto con el mismo nombre.
                CategoryNotFoundError: Si el ID de categoría especificado no existe.
        """
        
        # Valida que exita un producto con el id indicado 
        product = self.repository.read_by_id(product_id)
        if not product:
            raise ProductNotFoundError("Producto no encontrado")
        # end if
        
        # Valida los datos pasados como argumento sean correctos
        if product_data.price <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        # end if
        
        existing_product = self.repository.read_by_name(product_data.name)
        if existing_product and existing_product.id != product_id:
            raise DuplicateProductError("El producto ya existe")
        # end if
        
        if product_data.category_id is not None:
            category = self.repository.read_by_id(product_data.category_id)
            if not category:
                raise CategoryNotFoundError("La categoria no existe")
            # end if
        # end if
        
        updated_dict = product_data.model_dump(exclude_unset=True)
        return self.repository.update(product_id, updated_dict)
    # end def
    
    def toggle_active(self, product_id: int) -> Product | None:
        product = self.repository.read_by_id(product_id)
        if not product:
            raise ProductNotFoundError("Producto no encontrado")
        # end if
        
        return self.repository.update_active_status(product)
    # end def
    
    def get_filtered_products(self, filters: ProductSearchFilter) -> list[Product]:
        # Validaciones para de rango de precio
        if filters.min_price is not None and filters.min_price <= 0:
            raise ValueError("El precio mínimo debe ser mayor que cero")
        # end if

        if filters.max_price is not None and filters.max_price <= 0:
            raise ValueError("El precio máximo debe ser mayor que cero")
        # end if
        
        if filters.min_price is not None and filters.max_price is not None:
            if filters.min_price > filters.max_price:
                raise ValueError("El precio mínimo no puede ser mayor que el máximo")
            # end if
        # end if
        
        # Validacion de la categoria
        if filters.category_id is not None:
            category = self.repository.read_by_id(filters.category_id)
            if not category:
                raise CategoryNotFoundError("La categoria no existe")
            # end if
        # end if
        
        return self.repository.filter_products(filters)
    # end def 
    
# end class