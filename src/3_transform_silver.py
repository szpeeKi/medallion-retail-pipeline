import logging
import json
import psycopg2

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
    cur.execute("""
            INSERT INTO 
                silver(id, title, price, description, 
                                category, image, rating_score, rating_count)

            SELECT 
                id,
                TRIM(title),
                price,
                TRIM(description),
                TRIM(UPPER(category)),
                image,
                (rating->>'rate')::FLOAT,
                (rating->>'count')::INT
            FROM bronze
            ON CONFLICT (id) DO UPDATE SET 
                                    title = EXCLUDED.title, 
                                    price = EXCLUDED.price,
                                    description = EXCLUDED.description,
                                    category = EXCLUDED.category,
                                    image = EXCLUDED.image,
                                    rating_score = EXCLUDED.rating_score,
                                    rating_count = EXCLUDED.rating_count;
""")
    conn.commit()
    conn.close()
except Exception as e:
    logging.error(f'Connection Failed! {e}')
