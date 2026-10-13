from pathlib import Path
import requests
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import json

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(filename)s - %(message)s",
                    filename=LOG_DIR / 'app.log',
                    filemode='a')


def extract_data(endpoint: str):
    url = f'https://dummyjson.com/{endpoint}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info(f"{response.status_code}: Connection Success")
        return response.json()

    except requests.exceptions.RequestException:
        # Loga e relanca: engolir o erro faria o script gravar um arquivo vazio como se fosse sucesso.
        logging.exception(f"Request to {url} failed")
        raise


def save_raw_data(data, endpoint: str):
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    formatted_date = now.strftime("%Y%m%d_%H%M")

    folder_path = BASE_DIR / "data" / "raw"
    try:
        os.makedirs(folder_path, exist_ok=True)

        file_path = folder_path / f"{endpoint}_{formatted_date}.json"

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            logging.info(f"File created in {file_path}!")
    except OSError:
        logging.exception(f"Could not write the raw file in {folder_path}")
        raise


if __name__ == '__main__':
    save_raw_data(extract_data('products'), 'products')
