from pathlib import Path
import psycopg2
import logging
import os

BASE_DIR = Path(__file__).resolve().parents[2]
EXPORT_DIR = BASE_DIR / 'dashboard' / 'data'

# Nome do arquivo -> consulta. Os nomes de tabela sao fixos (nada vem de fora), entao nao ha risco de injecao.
EXPORTS = {
    'dim_category.csv': 'SELECT category_id, category_name FROM gold.dim_category ORDER BY category_id',
    'dim_product.csv': """SELECT id, category_id, title, brand, weight, dimension_width,
                                 dimension_height, dimension_depth, barcode
                          FROM gold.dim_product ORDER BY id""",
    'fact_product_snapshot.csv': """SELECT snapshot_date, product_id, category_id, price,
                                           discount_percentage, rating, availability_status
                                    FROM gold.fact_product_snapshot ORDER BY snapshot_date, product_id""",
}


def run():
    """Exporta a gold para CSV em dashboard/data, que e a fonte do relatorio do Power BI."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    conn = None
    try:
        with psycopg2.connect(
            dbname='postgres',
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST']
        ) as conn:
            logging.info('Connection Successful!')

            with conn.cursor() as cur:
                for file_name, select in EXPORTS.items():
                    with open(EXPORT_DIR / file_name, 'w', encoding='utf-8', newline='') as f:
                        cur.copy_expert(f'COPY ({select}) TO STDOUT WITH CSV HEADER', f)
                    logging.info(f'{cur.rowcount} rows exported to {file_name}')

    except Exception:
        logging.exception('An error occurred while exporting gold')
        raise

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    LOG_DIR = BASE_DIR / 'logs'
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(filename)s - %(message)s",
                        filename=LOG_DIR / 'app.log',
                        filemode='a')

    run()
