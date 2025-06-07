import requests
from Config.setting import config
from database.connections import store_products
from logger import logger
from Exceptions.product_exception import ProductAPIError, InvalidProductDataError

def fetch_and_store_products(title: str, limit: int = 4) -> dict:
    url = f"{config.product_base_url}search"
    params = {"query": title}
    headers = {
        "X-RapidAPI-Key": config.api_key,
        "X-RapidAPI-Host": config.amazon_api_host
    }

    try:
        logger.info(f"Fetching products for title: {title}")
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            raise ProductAPIError(f"API Error: {response.text}", status_code=response.status_code)

        data = response.json()
        products = data.get('data', {}).get('products')

        if not isinstance(products, list):
            logger.error("Unexpected response format: 'products' is not a list")
            raise InvalidProductDataError("Response JSON missing 'products' list")

        result = []
        for product in products:
            product_id = product.get('asin')
            product_name = product.get('product_title')
            product_price = product.get('product_price')
            product_star_rating = product.get('product_star_rating')

            if product_id and product_name and product_price:
                result.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "product_price": product_price,
                    "product_star_rating": product_star_rating
                })

            if len(result) >= limit:
                break

        logger.info(f"Extracted {len(result)} products, storing in DB...")
        inserted_products = store_products(result)
        logger.info(f"Inserted {len(inserted_products)} products into DB")
        return {"product": inserted_products}

    except ProductAPIError:
        # Re-raise known custom exceptions to be handled by caller
        raise
    except Exception as e:
        logger.exception("Failed to fetch or store products")
        raise ProductAPIError(f"Failed to fetch or store products: {str(e)}", 500)
