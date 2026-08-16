import json 
import requests
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context): 
    now = datetime.now()

    formatted_string = now.strftime("%Y%m%d_%H%M%S")

    endpoint = event.get('endpoint','products')

    url = f'https://fakestoreapi.com/{endpoint}'

    response = requests.get(url)
    data = response.json()
    json_string = json.dumps(data, indent=4)

    bucket_name = 'medallion-retail-raw-rafa'
    s3_key = f'{endpoint}/{now.strftime("%Y/%m/%d")}/{formatted_string}.json'

    s3.put_object(
        Bucket = bucket_name,
        Key = s3_key,
        Body = json_string,
        ContentType = 'application/json'
    )

    return {
        'statusCode': 200,
        'Message': f'File created on {bucket_name}! File name: {s3_key}'
    }

print(lambda_handler({'endpoint': 'xyz123'}, None))