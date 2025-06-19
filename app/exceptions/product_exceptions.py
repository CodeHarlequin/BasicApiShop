class ProductNotFoundError(Exception):
    """Se lanza cuando no se encuentra un producto."""
    pass

class DuplicateProductError(Exception):
    """Se lanza cuando ya existe un producto con el mismo nombre."""
    pass

class InvalidProductDataError(Exception):
    """Se lanza cuando la entrada del producto es inválida."""
    pass

class FailedProductDeletionError(Exception):
    """Se lanza cuando falla la eliminación del producto."""
    pass