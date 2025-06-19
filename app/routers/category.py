from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.product import *
from app.services.category_service import CategoryService
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.category import Category, CategoryCreate
from app.exceptions.category_exceptions import *

router = APIRouter(
    prefix="/category",
    tags=["Categorias"]
)

@router.get("/", response_model=list[Category])
def get_categories(
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    categories = service.get_all_categories()
    
    # Es mejor devolver un listdo vacio
    '''if not categories:
        raise HTTPException(status_code=404, detail="No se encontraron categorias")
    # end if'''
    
    return categories

# end def

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    category_creatd = None
    
    try:
        category_creatd = service.create_category(category)
    except DuplicateCategoryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # end try
    
    return category_creatd

# end def