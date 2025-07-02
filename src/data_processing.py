
import os
import json
import pandas as pd
from glob import glob
import logging
from src.config import DATA_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_json_to_csv(dataset_name="dataset_1"):
    products_info_json_path = os.path.join(DATA_DIR, dataset_name, "products_info")
    data = []

    json_files = glob(os.path.join(products_info_json_path, "*.json"))

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                file_data = json.load(f)
            except Exception as e:
                logging.error(f"Error loading {file_path}: {e}")
                continue

            for entry in file_data:
                results = entry.get("results", [])
                for product in results:
                    product_id = product.get("id")
                    name = product.get("name", "")
                    attributes_raw = product.get("attributes", [])

                    attributes = {
                        attr.get("name"): attr.get("value_name")
                        for attr in attributes_raw
                        if attr.get("name") and attr.get("value_name")
                    }

                    data.append({
                        "PRODUCT_ID": product_id,
                        "TITLE": name,
                        "ATTRIBUTES": attributes,
                        "SOURCE_FILE": os.path.basename(file_path)
                    })

    df = pd.DataFrame(data)
    output_path = os.path.join(DATA_DIR, dataset_name, f"{dataset_name}.csv")
    df.to_csv(output_path, index=False)
    logging.info(f"Successfully converted JSON files to {output_path}")
