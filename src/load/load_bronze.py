from pathlib import Path
import argparse
import psycopg2
import logging
import boto3
import json
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

sp_zoneinfo = ZoneInfo("America/Sao_Paulo")

PREFIX = 'products/'

query = """INSERT INTO bronze.products (id, title,description,category, price, discount_percentage, rating, stock,tags, brand,
                                                         sku,weight,dimensions,warranty_information, shipping_information,
                                                       availability_status, reviews, return_policy, minimum_order_quantity, meta, images, thumbnail, source_file, ingested_at)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ON CONFLICT (id, source_file) DO NOTHING;"""


def run(load_date=None):
    """Carrega na bronze o JSON mais recente do dia `load_date` (padrao: hoje em Sao Paulo)."""
    ingested_at = datetime.now(sp_zoneinfo)
    if load_date is None:
        load_date = ingested_at.date()
    day_prefix = f"{PREFIX}{load_date:%Y/%m/%d}/"

    conn = None
    try:
        # O nome do bucket vem do ambiente, como na Lambda: nada de infraestrutura gravado no codigo.
        bucket = os.environ['BUCKET_NAME']
        s3 = boto3.client('s3')

        listing = s3.list_objects_v2(Bucket=bucket, Prefix=day_prefix)
        keys = sorted(obj['Key'] for obj in listing.get('Contents', []) if obj['Key'].endswith('.json'))

        if not keys:
            raise FileNotFoundError(f'No file found for {load_date} in s3://{bucket}/{day_prefix}')

        source_file = keys[-1]

        response = s3.get_object(Bucket=bucket, Key=source_file)

        json_data = json.load(response['Body'])

        with psycopg2.connect(
            dbname='postgres',
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST']
        ) as conn:
            logging.info('Connection Successful!')
            with conn.cursor() as cur:
                inserted = 0
                for item in json_data['products']:
                    row = (
                        item['id'],
                        item['title'],
                        item['description'],
                        item['category'],
                        item['price'],
                        item['discountPercentage'],
                        item['rating'],
                        item['stock'],
                        json.dumps(item['tags']),
                        item.get('brand',None),
                        item['sku'],
                        item['weight'],
                        json.dumps(item['dimensions']),
                        item['warrantyInformation'],
                        item['shippingInformation'],
                        item['availabilityStatus'],
                        json.dumps(item['reviews']),
                        item['returnPolicy'],
                        item['minimumOrderQuantity'],
                        json.dumps(item['meta']),
                        json.dumps(item['images']),
                        item['thumbnail'],
                        source_file,
                        ingested_at)

                    cur.execute(query,row)
                    inserted += cur.rowcount

                logging.info(f'{inserted} of {len(json_data["products"])} rows inserted from {source_file}')

    except Exception:
        logging.exception('An error occurred while loading bronze')
        raise

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parents[2]
    LOG_DIR = BASE_DIR / 'logs'
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(filename)s - %(message)s",
                        filename=LOG_DIR / 'app.log',
                        filemode='a')

    parser = argparse.ArgumentParser()
    parser.add_argument('load_date', nargs='?', type=date.fromisoformat,
                        help='Dia a carregar, no formato AAAA-MM-DD (padrao: hoje em Sao Paulo)')
    args = parser.parse_args()

    run(args.load_date)
