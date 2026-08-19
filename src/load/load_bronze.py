import logging
import json
import psycopg2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
json_path = BASE_DIR / 'data' / 'raw' / 'products_20260807_1624.json'

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename=LOG_DIR / 'app.log',
                    filemode='a')

with open(json_path, 'r') as file:
    content = json.load(file)
    logging.info('Data writed to a variable')

try: 
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='admin',
        host='localhost'
    )

    logging.info('Connection Sucessful!')

    cur = conn.cursor()
    for item in content:
        values_insert = (
            item['id'],
            item['title'],
            item['price'],
            item['description'],
            item['category'],
            item['image'],
            json.dumps(item['rating'])
        )
        cur.execute("""INSERT INTO 
                        bronze(id,title,price,description,category,image,rating)
                        VALUES
                        (%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (id) DO UPDATE SET 
                        title = EXCLUDED.title, 
                        price = EXCLUDED.price,
                        description = EXCLUDED.description,
                        category = EXCLUDED.category,
                        image = EXCLUDED.image""",values_insert)
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    logging.error(f'Connection Failed! {e}')
