from pathlib import Path
import psycopg2
import logging
import boto3
import json
from datetime import datetime
from zoneinfo import ZoneInfo

sp_zoneinfo = ZoneInfo("America/Sao_Paulo")
ingested_at = datetime.now(sp_zoneinfo)

source_file = 'products/2026/08/14/20260814_005126.json'
s3 = boto3.client('s3')
response = s3.get_object(Bucket='medallion-retail-raw-rafa', Key=source_file)

json_data = json.load(response['Body'])

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename=LOG_DIR / 'app.log',
                    filemode='a')

query = """INSERT INTO bronze.products (id, title,description,category, price, discount_percentage, rating, stock,tags, brand,
                                                         sku,weight,dimensions,warranty_information, shipping_information, 
                                                       availability_status, reviews, return_policy, minimum_order_quantity, meta, images, thumbnail, source_file, ingested_at)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ON CONFLICT (id, source_file) DO NOTHING;"""
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
                    item['brand'],
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

except Exception:
    logging.exception('An error occurred while connecting')
    raise

finally:
    if conn:
        conn.close()