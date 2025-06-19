from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.product import *
from app.services.product_service import ProductService
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.product import Product
from app.exceptions.product_exceptions import *
from app.exceptions.category_exceptions import *

router = APIRouter(
    prefix="/products",
    tags=["Productos"]
)

@router.get("/", response_model=list[Product])
def get_products(
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    products = service.get_all_products()
    
    return products
# end def

@router.get("/{product_id}", response_model=Product)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    
    try:
        existing_product = service.get_by_id(product_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    # end try
    
    return existing_product
# end def

@router.post("/filter-products", response_model=list[Product])
def get_filtered_products(
    filters: ProductSearchFilter,
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    
    try:
        products = service.get_filtered_products(filters)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # end try
    
    return products 
# end def

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    product_creatd = None
    
    try:
        product_creatd = service.create_product(product)
    except (DuplicateProductError, CategoryNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    # end try
    
    return product_creatd 
# end def

@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_update: ProductCreate,
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    try:
        updated_product = service.update_product(product_id, product_update)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (DuplicateProductError, CategoryNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    # end try
    
    return updated_product
# end def

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    
    try:  
        service.delete_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    # end try
    
    return  # 204 NO CONTENT no devuelve body
# end def


@router.put("/{product_id}/toggle-active", response_model=Product)
def toggle_product_active_status(
    product_id: int,
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    
    try:
        update_product = service.toggle_active(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    # end try
    
    return update_product
# end def