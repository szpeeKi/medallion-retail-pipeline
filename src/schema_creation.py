import psycopg2
import logging

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename='app.log',
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
            cur.execute("""CREATE TABLE bronze.products (
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

            cur.execute("""CREATE TABLE silver.products (
                            id INTEGER,
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
                            snapshot_date DATE

                            PRIMARY KEY (id, snapshot_date)
            );""")

finally:
    if conn:
        conn.close()
    else:
        logging.error('Connection Failed')
