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
            cur.execute("""INSERT INTO gold.dim_category(category_name)
                            SELECT 
                                DISTINCT category
                            FROM silver.products
                            ON CONFLICT (category_name) DO NOTHING;""")
            cur.execute("""INSERT INTO gold.dim_product(id, category_id, title, description, brand, 
                                                        weight, dimension_width,dimension_height,dimension_depth, barcode)

                            SELECT DISTINCT ON (sil.id)
                                sil.id,
                                cat.category_id,
                                sil.title, 
                                sil.description, 
                                sil.brand, 
                                sil.weight, 
                                sil.dimension_width,
                                sil.dimension_height,
                                sil.dimension_depth, 
                                sil.barcode
                            FROM silver.products AS sil
                            JOIN gold.dim_category AS cat
                            ON sil.category = cat.category_name 
                            ORDER BY sil.id, sil.snapshot_date DESC
                            ON CONFLICT (id)
                            DO UPDATE SET
                                title = EXCLUDED.title, description = EXCLUDED.description,
                                brand = EXCLUDED.brand, weight = EXCLUDED.weight,
                                dimension_width = EXCLUDED.dimension_width, dimension_height = EXCLUDED.dimension_height,
                                dimension_depth = EXCLUDED.dimension_depth, barcode = EXCLUDED.barcode;

        """)
            # Apos execucao do INSERT INTO, ele sai do with ja dando commit automaticamente. 

except Exception:
    logging.exception('An error occurred while connecting')
    raise

finally:
    if conn:
        conn.close()

