from pathlib import Path
import requests 
import logging
from datetime import datetime
import os
import json

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(message)s",
                    filename=LOG_DIR / 'app.log',
                    filemode='a')




def extract_data(endpoint: str):
    URL = f'https://dummyjson.com/{endpoint}'

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

    folder_path = BASE_DIR / "data" / "raw"
    try: 
        os.makedirs(folder_path, exist_ok=True)

        file_path = folder_path / f"{endpoint}_{formatted_date}.json"

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            logging.info(f"File created in {file_path}!")
    except PermissionError as p:
        logging.error(f'Access denied: {p}')
    except FileNotFoundError as f:
        logging.error(f'Path doesnt exists: {f}')
    except OSError as e:
        logging.error(f'Error: {e}')

save_raw_data(extract_data('products'),'products')