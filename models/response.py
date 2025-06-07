from pydantic import BaseModel, Field
from typing import List, Optional

class Product(BaseModel):
    product_id: str = Field(..., example="B07XYZ123")
    product_name: str = Field(..., example="Wireless Mouse")
    product_price: str = Field(..., example="$1299")
    product_star_rating: Optional[str] = Field(None, example="4.3")
    viewed: Optional[bool] = Field(None, example=True)

class ProductListResponse(BaseModel):
    product: List[Product]

class ProductDBListResponse(BaseModel):
    products: List[Product]

class ProductDeleteResponse(BaseModel):
    message: str = Field(..., example="Product deleted")
    product: Product

class ProductViewedResponse(BaseModel):
    message: str = Field(..., example="Product marked as viewed")
    product: Product
