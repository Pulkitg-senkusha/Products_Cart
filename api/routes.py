from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.product_services import fetch_and_store_products, ProductAPIError
from typing import List
from database.connections import get_all_products, delete_product, mark_product_viewed
from logger import logger

router = APIRouter(prefix="/products", tags=["products"])

class Product(BaseModel):
    product_id: str
    product_name: str
    product_price: str
    product_star_rating: str

class ProductListResponse(BaseModel):
    product: List[Product]

@router.get("/{title}", response_model=ProductListResponse)
def get_product_data(title: str):
    logger.info(f"Fetching product data for title: {title}")
    try:
        product_data = fetch_and_store_products(title)
        logger.info(f"Successfully fetched and stored product data for: {title}")
        return product_data
    except ProductAPIError as e:
        logger.error(f"ProductAPIError: {e.message} (status code: {e.status_code})")
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/products/", tags=["products"])
async def get_products():
    logger.info("Fetching all products from the database")
    try:
        products = get_all_products()
        logger.info(f"Fetched {len(products)} products from the database")
        return {"products": products}
    except Exception as e:
        logger.exception("Error while fetching products")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/products/{product_id}", tags=["products"])
async def delete_product_endpoint(product_id: str):
    logger.info(f"Attempting to delete product with ID: {product_id}")
    try:
        deleted = delete_product(product_id)
        if not deleted:
            logger.warning(f"Product with ID {product_id} not found")
            raise HTTPException(status_code=404, detail="Product not found")
        logger.info(f"Deleted product with ID: {product_id}")
        return {"message": "Product deleted", "product": deleted}
    except Exception as e:
        logger.exception(f"Error deleting product with ID: {product_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/products/{product_id}/viewed", tags=["products"])
async def mark_as_viewed(product_id: str):
    logger.info(f"Marking product with ID {product_id} as viewed")
    try:
        updated = mark_product_viewed(product_id)
        if not updated:
            logger.warning(f"Product with ID {product_id} not found for viewing")
            raise HTTPException(status_code=404, detail="Product not found")
        logger.info(f"Marked product with ID {product_id} as viewed")
        return {"message": "Product marked as viewed", "product": updated}
    except Exception as e:
        logger.exception(f"Error marking product {product_id} as viewed")
        raise HTTPException(status_code=500, detail=str(e))
