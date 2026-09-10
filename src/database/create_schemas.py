from pathlib import Path
import psycopg2
import logging

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename=LOG_DIR / 'app.log',
                    filemode='a')
conn = None
try: 
    with psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='admin',
        host='localhost'
    ) as conn:

        logging.info('Connection Successful!')

        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS bronze_products, silver_products, dim_product, fact_category_metrics, dim_category, bronze.products")
            cur.execute("""CREATE SCHEMA IF NOT EXISTS bronze;""")
            cur.execute("""CREATE SCHEMA IF NOT EXISTS silver;""")
            cur.execute("""CREATE SCHEMA IF NOT EXISTS gold;""")
            cur.execute("""CREATE TABLE IF NOT EXISTS bronze.products (
                                id INTEGER,
                                title TEXT,
                                description TEXT,
                                category TEXT,
                                price NUMERIC(12,2),
                                discount_percentage NUMERIC(5,2),
                                rating NUMERIC(3,2),
                                stock INTEGER,
                                tags JSONB,
                                brand TEXT,
                                sku TEXT,
                                weight NUMERIC(10,2),
                                dimensions JSONB,
                                warranty_information TEXT,
                                shipping_information TEXT,
                                availability_status TEXT,
                                reviews JSONB,
                                return_policy TEXT,
                                minimum_order_quantity INTEGER,
                                meta JSONB,
                                images JSONB,
                                thumbnail TEXT,
                                source_file TEXT,
                                ingested_at TIMESTAMPTZ,

                            PRIMARY KEY (id, source_file)
            );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS silver.products (
                                id INTEGER,
                                snapshot_date DATE,
                                title TEXT,
                                description TEXT,
                                category TEXT,
                                price NUMERIC(10,2),
                                discount_percentage NUMERIC(5,2),
                                rating NUMERIC(3,2),
                                brand TEXT,
                                weight NUMERIC(5,2),
                                dimension_width NUMERIC(5,2),
                                dimension_height NUMERIC(5,2),
                                dimension_depth NUMERIC(5,2),
                                availability_status TEXT,
                                barcode TEXT,

                            PRIMARY KEY (id, snapshot_date)
            );""")
            cur.execute("""CREATE TABLE IF NOT EXISTS gold.dim_category (
                                category_id SERIAL PRIMARY KEY, 
                                category_name TEXT UNIQUE
            );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS gold.dim_product (
                                id INT PRIMARY KEY, 
                                category_id INT REFERENCES gold.dim_category (category_id), 
                                title TEXT, 
                                description TEXT, 
                                brand TEXT,
                                weight NUMERIC(5,2),
                                dimension_width NUMERIC(5,2),
                                dimension_height NUMERIC(5,2),
                                dimension_depth NUMERIC(5,2),
                                barcode TEXT
            );""")
        
except Exception:
    logging.exception('An error occurred while connecting')
    raise

finally:
    if conn:
        conn.close()