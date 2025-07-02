import requests
import time
import re
import json
import os
import logging
from dotenv import load_dotenv
from src.config import ML_BASE_URL, ML_API_BASE_URL, SITE_ID

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ML_ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {ML_ACCESS_TOKEN}"
}

def scrape_product_ids_from_search(search_query, max_products=1000, pause=1.5):
    product_ids = []
    offset = 0
    per_page = 50

    while len(product_ids) < max_products:
        url = f"{ML_BASE_URL}/{search_query}_Desde_{offset+1}_NoIndex_True"
        logging.info(f"Scraping page: {url}")
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error accessing {url}: {e}")
            break

        matches = re.findall(r'"product_id":"(MLB\\d+)"', response.text)
        unique_matches = list(set(matches))
        product_ids.extend(unique_matches)

        if not matches:
            logging.info("No more products found, stopping.")
            break

        if len(product_ids) >= max_products - offset:
            logging.info("Close to max products, removing duplicates.")
            product_ids = list(set(product_ids))

        offset += per_page
        time.sleep(pause)

    return product_ids[:max_products]

def get_product_info(product_id):
    url = f"{ML_API_BASE_URL}/products/search?status=active&site_id={SITE_ID}&product_identifier={product_id}"
    logging.info(f"Fetching product info for ID: {product_id}")
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching product info for {product_id}: {e}")
        return None

def get_product_data(queries, data_folder="data/dataset_1"):
    products_ids_folder = os.path.join(data_folder, "products_ids")
    products_info_folder = os.path.join(data_folder, "products_info")
    os.makedirs(products_ids_folder, exist_ok=True)
    os.makedirs(products_info_folder, exist_ok=True)

    for i, query in enumerate(queries):
        product_ids_file = os.path.join(products_ids_folder, f"products_{i+1}_{query}.json")
        if not os.path.exists(product_ids_file):
            logging.info(f"Scraping for query {i+1}/{len(queries)}: {query}")
            products = scrape_product_ids_from_search(query, max_products=1000, pause=0)
            with open(product_ids_file, "w", encoding="utf-8") as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

    json_files = [f for f in os.listdir(products_ids_folder) if f.endswith(".json")]

    for json_file in json_files:
        output_file = os.path.join(products_info_folder, f"info_{json_file}")
        if os.path.exists(output_file):
            logging.info(f"Skipping {json_file} (already processed)")
            continue

        json_file_path = os.path.join(products_ids_folder, json_file)
        with open(json_file_path, "r", encoding="utf-8") as file:
            product_ids = json.load(file)

        prods_info = []
        for product_id in product_ids:
            time.sleep(0.01)
            info = get_product_info(product_id)
            if info:
                prods_info.append(info)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(prods_info, f, ensure_ascii=False, indent=4)
