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
    cur.execute("""CREATE TABLE IF NOT EXISTS dim_category (
                    id SERIAL PRIMARY KEY,
                    category TEXT
                    );""")

    cur.execute("""
                CREATE TABLE IF NOT EXISTS fact_category_metrics (
                    category_id INT PRIMARY KEY REFERENCES dim_category(id),
                    total_products INT,
                    avg_price FLOAT,
                    avg_rating FLOAT
                    );
""")

    cur.execute("""CREATE TABLE IF NOT EXISTS dim_product (
                    id INT PRIMARY KEY,
                    title TEXT,
                    category_id INT REFERENCES dim_category(id),
                    price FLOAT,
                    description TEXT,
                    image TEXT,
                    rating_score FLOAT,
                    rating_count INT
                    );""")

    cur.execute("TRUNCATE TABLE fact_category_metrics, dim_product, dim_category CASCADE;")

    cur.execute("""
                INSERT INTO dim_category(category)
                SELECT DISTINCT(category) AS category_name
                FROM silver_products;
                """)


    cur.execute("""
                INSERT INTO dim_product(id,title,category_id,price,description,image,rating_score,rating_count)
                SELECT 
                    sil.id,
                    sil.title,
                    cat.id,
                    sil.price,
                    sil.description,
                    sil.image,
                    sil.rating_score,
                    sil.rating_count
                FROM silver_products AS sil
                JOIN dim_category AS cat
                ON sil.category = cat.category;
""")

    cur.execute("""
                INSERT INTO fact_category_metrics(category_id, total_products, avg_price, avg_rating)
                SELECT 
                    prod.category_id,
                    COUNT(prod.id),
                    ROUND(AVG(prod.price::numeric),2),
                    ROUND(AVG(prod.rating_score::numeric),2)
                FROM dim_product AS prod
                GROUP BY prod.category_id;
""")
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    logging.error(f'Connection Failed! {e}')


