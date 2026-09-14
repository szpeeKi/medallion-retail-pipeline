import json 
import requests
import boto3
from datetime import datetime, timezone
import logging
import os
from zoneinfo import ZoneInfo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context): 
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))

    formatted_string = now.strftime("%Y%m%d_%H%M%S")

    endpoint = event.get('endpoint','products')

    url = f'https://dummyjson.com/{endpoint}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        json_string = json.dumps(data, indent=4)

        bucket_name = os.environ['BUCKET_NAME']
        s3_key = f'{endpoint}/{now.strftime("%Y/%m/%d")}/{formatted_string}.json'

        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json_string,
            ContentType='application/json'
        )

        return {
        'statusCode': 200,
        'body': f'File created on {bucket_name}! File name: {s3_key}'
        }
    except Exception:
        logger.exception('An error occurred during execution')
        raise