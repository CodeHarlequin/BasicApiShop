from app.repositories.base_repository import BaseRepository
from app.models.category import Category

class CategoryRepository(BaseRepository[Category]):
    
    def __init__(self, db):
        super().__init__(db, Category)
    # end init
    
    
    def read_by_name(self, name: str) -> list[Category] | None:
        return (
            self.db.query(self.model)
            .filter(self.model.name == name)
            .first()
        )
    # end def
    
# end class