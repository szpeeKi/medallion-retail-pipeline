import requests 
import logging
from datetime import datetime
import os
import json

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename='app.log',
                    filemode='a')




def extract_data(endpoint: str):
    URL = f'https://fakestoreapi.com/{endpoint}'

    try:
        response = requests.get(URL)
        response.raise_for_status()
        logging.info(f"200: Connection Success")
        data = response.json()
        return data

    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error (e.g., 404, 500): {errh}")

    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Connection Error (e.g., DNS failure, refused connection): {errc}")

    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")

    except requests.exceptions.TooManyRedirects as errr:
        logging.error(f"Too Many Redirects: {errr}")

    except requests.exceptions.RequestException as e:
        logging.error(f"An unexpected requests error occurred: {e}")
        
    except Exception as e:
        logging.error(f"A non-requests error occurred: {e}")

def save_raw_data(data, endpoint: str):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d_%H%M")

    folder_path = f"data/raw"
    os.makedirs(folder_path, exist_ok=True)

    file_path = f"{folder_path}/{endpoint}_{formatted_date}.json"

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
        logging.info(f"File created in {file_path}!")

save_raw_data(extract_data('products'),'products')