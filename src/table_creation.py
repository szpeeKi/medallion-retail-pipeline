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
    cur.execute("""CREATE TABLE IF NOT EXISTS bronze_products (
                    id INT PRIMARY KEY,
                    title VARCHAR(255),
                    price FLOAT,
                    description TEXT,
                    category VARCHAR(255),
                    image TEXT,
                    rating JSONB
                    );""")
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    logging.error(f'Connection Failed! {e}')


