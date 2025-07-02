import pandas as pd
import json
import os
import logging
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from dotenv import load_dotenv

from src.config import (
    DATA_DIR,
    HAZMAT_DEFINITION_FILE,
    JSON_EXTRACTOR_MODEL,
    HAZMAT_CLASSIFIER_MODEL,
)
from src.llm_utils import call_llm
from src.data_utils import extract_from_tag

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Confidence(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class HazmatClassification(BaseModel):
    product_id: str = Field(..., description="The unique identifier of the product.")
    is_hazmat: bool = Field(..., description="Indicates whether the product is classified as a Hazmat.")
    reason: Optional[str] = Field(None, description="The reason for the classification, if the product is a Hazmat.")
    confidence: Optional[Confidence] = Field(None, description="The confidence level of the classification, if the product is a Hazmat.")

def get_hazmat_definition():
    try:
        with open(HAZMAT_DEFINITION_FILE, "r", encoding='utf8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"Hazmat definition file not found at: {HAZMAT_DEFINITION_FILE}")
        raise

def classify_products(dataset_name="dataset_1", batch_size=100):
    hazmat_def = get_hazmat_definition()
    
    dataset_path = os.path.join(DATA_DIR, dataset_name, f"{dataset_name}.csv")
    try:
        products_df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        logging.error(f"Dataset file not found at: {dataset_path}")
        return

    products_df.drop(columns=['IS_HAZMAT', 'REASON', 'CONFIDENCE'], inplace=True, errors='ignore')

    hazmat_classifier_system_msg = f"""
    You are a domain-expert Hazmat classifier. Your task is to analyze the products below and determine, for each, if it is Hazmat or not, based on the definition provided between <hazmat_definition> tags.\n
    You must base your analysis on the following JSON schema, which describes the required analysis for each product in the fields:\n
    <json_schema>{HazmatClassification.model_json_schema()}</json_schema>\n
    Before answering, you must output your detailed reasoning process.\n
    Hazmat definition: <hazmat_definition>{hazmat_def}</hazmat_definition>\n
    Guidelines:\n
    - Always refer to the Hazmat definition to address the classification. Do not suppose anything. If not certain of the classification, output as hazmat with lower confidence.\n
    - Only output a product as non-hazmat if you are absolutely certain that it is not a Hazmat according to the definition provided.\n
    """

    hazmat_json_extractor_system_msg = f"""
    You are a domain-expert Hazmat classifier. Based on the analysis below, extract and output the final answer as a jsonl structure, located between <jsonl> tags, with each line following this schema (one line per product): <json_schema>{HazmatClassification.model_json_schema()}</json_schema>.\n
    Guidelines:\n
    - For the tag <jsonl>: The final answer must be a valid jsonl structure, with each line following the schema provided.\n
    - If not certain of the classification, output as hazmat with lower confidence.\n
    - Only output a product as non-hazmat if you are absolutely certain that it is not a Hazmat according to the definition provided.\n
    """

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
                model=HAZMAT_CLASSIFIER_MODEL,
            )
            
            logging.info("Raw response received, formatting to JSONL...")
            formatted_response = call_llm(
                system=hazmat_json_extractor_system_msg,
                prompt=raw_response,
                model=JSON_EXTRACTOR_MODEL,
            )
        except Exception as e:
            logging.error(f"Error during LLM call for batch {i//batch_size + 1}: {e}")
            continue
        
        jsonl_content = extract_from_tag(formatted_response, "jsonl")
        if jsonl_content:
            logging.info(f"Batch {i//batch_size + 1} jsonl content extracted!")
            with open(output_jsonl, "a", encoding="utf-8") as f:
                f.write(jsonl_content + "\n")
        
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
    for col in ["IS_HAZMAT", "REASON", "CONFIDENCE"]:
        if col not in products_df.columns:
            products_df[col] = None

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

