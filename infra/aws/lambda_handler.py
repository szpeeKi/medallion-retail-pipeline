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
item = json_data['products'][0]


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
    ingested_at
)

print(tuple(item))