import pandas as pd
import json
import os
import logging
from src.models import Confidence, HazmatClassification
from dotenv import load_dotenv
from src.prompts import HAZMAT_CLASSIFIER_SYSTEM_MSG, HAZMAT_JSON_EXTRACTOR_SYSTEM_MSG

from src.config import (
    DATA_DIR,
    HAZMAT_DEFINITION_WITH_EXAMPLES_FILE,
    INFO_EXTRACTOR_MODEL,
    DEFAULT_MODEL,
)
from src.llm_utils import call_llm
from src.data_utils import extract_from_tag, get_hazmat_definition

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def classify_products_v1(dataset_name="dataset_1", batch_size=100, product_ids=None, output_csv_name=None):
    hazmat_def = get_hazmat_definition()
    
    dataset_path = os.path.join(DATA_DIR, dataset_name, f"{dataset_name}.csv")
    try:
        products_df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        logging.error(f"Dataset file not found at: {dataset_path}")
        return

    # Filter by product_ids if provided
    if product_ids:
        products_df = products_df[products_df['PRODUCT_ID'].isin(product_ids)]
        if len(products_df) < len(product_ids):
            missing_ids = set(product_ids) - set(products_df['PRODUCT_ID'])
            logging.warning(f"Some product IDs not found in the dataset: {missing_ids}")

    products_df.drop(columns=['IS_HAZMAT', 'REASON', 'CONFIDENCE'], inplace=True, errors='ignore')

    hazmat_classifier_system_msg = HAZMAT_CLASSIFIER_SYSTEM_MSG.format(
        json_schema=HazmatClassification.model_json_schema(),
        hazmat_def=hazmat_def
    )
    hazmat_json_extractor_system_msg = HAZMAT_JSON_EXTRACTOR_SYSTEM_MSG.format(
        json_schema=HazmatClassification.model_json_schema(),
        hazmat_def=hazmat_def
    )

    output_jsonl = os.path.join(DATA_DIR, dataset_name, f"{dataset_name}_classified_products.jsonl")
    log_file = os.path.join(DATA_DIR, dataset_name, f"{dataset_name}_raw_log.txt")

    for i in range(0, len(products_df), batch_size):
        batch = products_df.iloc[i:i + batch_size]
        batch_list = batch.to_dict(orient="records")
        
        logging.info(f"Processing batch {i//batch_size + 1} with {len(batch_list)} products...")
        try:
            raw_response = call_llm(
                system=hazmat_classifier_system_msg,
                prompt=f"Products to classify:\n{batch_list}",
                model=DEFAULT_MODEL,
            )
            
            logging.info("Raw response received, formatting to JSONL...")
            formatted_response = call_llm(
                system=hazmat_json_extractor_system_msg,
                prompt=raw_response,
                model=INFO_EXTRACTOR_MODEL,
            )
        except Exception as e:
            logging.error(f"Error during LLM call for batch {i//batch_size + 1}: {e}")
            continue
        
        jsonl_content = extract_from_tag(formatted_response, "jsonl")
        if jsonl_content:
            logging.info(f"Batch {i//batch_size + 1} jsonl content extracted!")
            # Add classifier name and llm model to each line before saving
            jsonl_lines = jsonl_content.strip().split("\n")
            updated_lines = []
            for line in jsonl_lines:
                try:
                    row = json.loads(line)
                    row["CLASSIFIER_NAME"] = "classifier_v1"
                    row["LLM_MODEL"] = DEFAULT_MODEL
                    updated_lines.append(json.dumps(row, ensure_ascii=False))
                except Exception as e:
                    logging.warning(f"Could not update jsonl line: {line} ({e})")
                    continue
            with open(output_jsonl, "a", encoding="utf-8") as f:
                for updated_line in updated_lines:
                    f.write(updated_line + "\n")
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"Batch {i//batch_size + 1}:\n{raw_response}\n\n")
        
        logging.info(f"Batch {i//batch_size + 1} processed and saved to {output_jsonl} and {log_file}!")

    classified_rows = []
    with open(output_jsonl, "rb") as f:
        for bline in f:
            decoded_line = _try_decode_line(bline)
            if decoded_line and decoded_line.strip():
                try:
                    row = json.loads(decoded_line)
                    row = {k.upper(): v for k, v in row.items()}
                    classified_rows.append(row)
                except json.JSONDecodeError:
                    logging.warning(f"Skipping corrupted JSON line: {decoded_line}")
                    continue

    classified_df = pd.DataFrame(classified_rows)
    if not classified_df.empty:
        classified_df.columns = [col.upper() for col in classified_df.columns]

    products_df.columns = [col.upper() for col in products_df.columns]

    products_df = products_df.merge(
        classified_df,
        on='PRODUCT_ID',
        how='left',
        suffixes=("", "_CLASSIFIED")
    )

    # Ensure required columns exist in the output
    for col in ["IS_HAZMAT", "REASON", "CONFIDENCE", "CLASSIFIER_NAME", "LLM_MODEL"]:
        if col not in products_df.columns:
            if col == "CLASSIFIER_NAME":
                products_df[col] = "classifier_v1"
            elif col == "LLM_MODEL":
                products_df[col] = DEFAULT_MODEL
            else:
                products_df[col] = None

    if output_csv_name:
        classified_csv_path = os.path.join(DATA_DIR, dataset_name, output_csv_name)
    else:
        classified_csv_path = os.path.join(DATA_DIR, dataset_name, f"{dataset_name}_classified_products.csv")
    products_df.to_csv(classified_csv_path, index=False, encoding="utf-8")
    logging.info(f"Classification complete. Results saved to {classified_csv_path}")

def _try_decode_line(line):
    for encoding in ["utf-8", "latin1", "utf-8-sig"]:
        try:
            return line.decode(encoding)
        except UnicodeDecodeError:
            continue
    logging.warning(f"Could not decode line: {line}")
    return None

