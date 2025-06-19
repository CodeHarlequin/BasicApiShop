from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def read_all(self) -> List[T]:
        return self.db.query(self.model).all()
    # end def

    def read_by_id(self, obj_id: int) -> Optional[T]:
        return self.db.query(self.model).get(obj_id)
    # end def
    
    def update(self, obj_id: int, updated_fields: dict) -> Optional[T]:
        obj = self.read_by_id(obj_id)
        
        if not obj:
            return None
        # end if
        
        for key, value in updated_fields.items():
            setattr(obj, key, value)
        # end for
        
        self.db.commit()
        self.db.refresh(obj)
        return obj
    # end def

    def delete(self, obj_id: int) -> bool:
        obj = self.read_by_id(obj_id)
        
        if not obj:
            return False
        # end if
        
        self.db.delete(obj)
        self.db.commit()
        return True
    # end def
    
# end class
    