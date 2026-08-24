from pathlib import Path
import psycopg2
import logging

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename=LOG_DIR / 'app.log',
                    filemode='w')
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
            cur.execute

finally:
    if conn:
        conn.close()
    else:
        logging.error('Connection Failed')