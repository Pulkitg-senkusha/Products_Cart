

class ProductAPIError(Exception):
    """
    Base Exception for all product-related API errors.
    Includes a custom message and status code.
    """
    def __init__(self, message: str = "Product API Error", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ProductNotFoundError(ProductAPIError):
    """
    Raised when a product is not found in the database.
    """
    def __init__(self, product_id: str):
        message = f"Product with ID '{product_id}' not found."
        super().__init__(message, status_code=404)


class ProductAlreadyExistsError(ProductAPIError):
    """
    Raised when trying to insert a product that already exists.
    """
    def __init__(self, product_id: str):
        message = f"Product with ID '{product_id}' already exists."
        super().__init__(message, status_code=409)


class InvalidProductDataError(ProductAPIError):
    """
    Raised when product data is missing or malformed.
    """
    def __init__(self, reason: str):
        message = f"Invalid product data: {reason}"
        super().__init__(message, status_code=400)
