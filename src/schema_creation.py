import psycopg2
import logging

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename='app.log',
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

    cur.execute("DROP TABLE bronze_products, silver_products")
    cur.execute("""CREATE SCHEMA IF NOT EXISTS bronze (
                    id INT PRIMARY KEY,
                    title VARCHAR(255),
                    price NUMERIC(10,2),
                    description TEXT,
                    category VARCHAR(255),
                    image TEXT,
                    rating JSONB
                    );""")
    cur.execute("""CREATE SCHEMA IF NOT EXISTS silver (
                    id INT PRIMARY KEY,
                    title TEXT,
                    price FLOAT,
                    description TEXT,
                    category TEXT,
                    image TEXT,
                    rating_score FLOAT,
                    rating_count INT
                    );""")
except Exception as e:
    logging.error(f'Connection Failed! {e}')
