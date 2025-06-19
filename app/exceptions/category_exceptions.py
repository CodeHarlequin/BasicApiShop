class CategoryNotFoundError(Exception):
    """Se lanza cuando no se encuentra una categoria."""
    pass

class DuplicateCategoryError(Exception):
    """Se lanza cuando ya existe una categoria con el mismo nombre."""
    pass

class InvalidCategoryDataError(Exception):
    """Se lanza cuando la entrada de la categoría es inválida."""
    pass