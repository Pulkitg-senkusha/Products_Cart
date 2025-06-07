import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from logger import logger  # ✅ Use logger instead of print

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            cursor_factory=RealDictCursor
        )
        logger.info("Database connection established")
        return conn
    except Exception as e:
        logger.exception("Error connecting to the database")
        raise

def init_db():
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS product1 (
            product_id VARCHAR(50) PRIMARY KEY,
            product_name VARCHAR(10000) NOT NULL,
            product_price VARCHAR(50),
            product_star_rating VARCHAR(10),
            viewed BOOLEAN DEFAULT FALSE
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        logger.info("Database initialized and table ensured")
    except Exception as e:
        conn.rollback()
        logger.exception("Error initializing the database")
        raise
    finally:
        if cur:
            cur.close()
        conn.close()

def store_products(products):
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        insert_query = """
        INSERT INTO product1 (product_id, product_name, product_price, product_star_rating)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id) DO UPDATE SET
            product_name = EXCLUDED.product_name,
            product_price = EXCLUDED.product_price,
            product_star_rating = EXCLUDED.product_star_rating
        RETURNING *;
        """
        inserted_products = []
        for product in products:
            try:
                cur.execute(insert_query, (
                    product['product_id'],
                    product['product_name'],
                    product['product_price'],
                    product['product_star_rating']
                ))
                result = cur.fetchone()
                if result:
                    inserted_products.append(dict(result))
            except Exception as e:
                logger.warning(f"Skipping product {product.get('product_id')} due to error: {e}")
                continue
        conn.commit()
        logger.info(f"Stored {len(inserted_products)} products")
        return inserted_products
    except Exception as e:
        conn.rollback()
        logger.exception("Error storing products")
        raise
    finally:
        if cur:
            cur.close()
        conn.close()

def get_all_products():
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product1;")
        products = cur.fetchall()
        logger.info(f"Fetched {len(products)} products from database")
        return [dict(product) for product in products]
    except Exception as e:
        logger.exception("Error fetching products")
        raise
    finally:
        if cur:
            cur.close()
        conn.close()

def delete_product(product_id: str):
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM product1 WHERE product_id = %s RETURNING *;", (product_id,))
        deleted_product = cur.fetchone()
        conn.commit()
        if deleted_product:
            logger.info(f"Deleted product with ID: {product_id}")
        else:
            logger.warning(f"Attempted to delete non-existent product with ID: {product_id}")
        return dict(deleted_product) if deleted_product else None
    except Exception as e:
        conn.rollback()
        logger.exception(f"Error deleting product with ID: {product_id}")
        raise
    finally:
        if cur:
            cur.close()
        conn.close()

def mark_product_viewed(product_id: str):
    conn = get_db_connection()
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product1 WHERE product_id = %s;", (product_id,))
        if not cur.fetchone():
            logger.warning(f"Product with ID {product_id} not found to mark as viewed")
            return None
        
        cur.execute("""
        ALTER TABLE product1 
        ADD COLUMN IF NOT EXISTS viewed BOOLEAN DEFAULT FALSE;
        """)
        
        cur.execute("""
        UPDATE product1 
        SET viewed = TRUE 
        WHERE product_id = %s 
        RETURNING *;
        """, (product_id,))
        
        updated_product = cur.fetchone()
        conn.commit()
        if updated_product:
            logger.info(f"Marked product ID {product_id} as viewed")
        return dict(updated_product) if updated_product else None
    except Exception as e:
        conn.rollback()
        logger.exception(f"Error marking product {product_id} as viewed")
        raise
    finally:
        if cur:
            cur.close()
        conn.close()
