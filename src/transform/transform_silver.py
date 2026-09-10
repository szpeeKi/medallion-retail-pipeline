from pathlib import Path
import logging
import json
import psycopg2

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename=LOG_DIR / 'app.log',
                    filemode='a')


try: 
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='admin',
        host='localhost'
    )

    logging.info('Connection Sucessful!')

    cur = conn.cursor()
    cur.execute("""
                INSERT INTO silver.products(id,snapshot_date,title,description,category,price,
                discount_percentage,rating,brand,weight,dimension_width,
                dimension_height,dimension_depth,availability_status,barcode)

                SELECT DISTINCT ON (id,snapshot_date)
                    id, 
                    SPLIT_PART(SPLIT_PART(source_file, '/',5),'_',1)::DATE AS snapshot_date,
                    title, 
                    description, 
                    category, 
                    price, 
                    discount_percentage, 
                    rating, 
                    brand, 
                    weight, 
                    (NULLIF(dimensions->>'width', ''))::NUMERIC(5,2),
                    (NULLIF(dimensions->>'height', ''))::NUMERIC(5,2),
                    (NULLIF(dimensions->>'depth', ''))::NUMERIC(5,2),
                    availability_status,
                    (meta->>'barcode')::TEXT
                FROM bronze.products
                ORDER BY id,snapshot_date,source_file DESC

                ON CONFLICT (id, snapshot_date) 
                DO UPDATE SET 
                    title = EXCLUDED.title, description = EXCLUDED.description, category = EXCLUDED.category, 
                    price = EXCLUDED.price, discount_percentage = EXCLUDED.discount_percentage, rating = EXCLUDED.rating, 
                    brand = EXCLUDED.brand, weight = EXCLUDED.weight, dimension_width = EXCLUDED.dimension_width, 
                    dimension_height = EXCLUDED.dimension_height, dimension_depth = EXCLUDED.dimension_depth, availability_status = EXCLUDED.availability_status, barcode = EXCLUDED.barcode 
""")
    conn.commit()
    conn.close()
except Exception as e:
    logging.error(f'Connection Failed! {e}')
