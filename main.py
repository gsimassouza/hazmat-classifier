import argparse
import logging
import os
from src.data_collection import get_product_data
from src.data_processing import convert_json_to_csv
from src.classifier_v1 import classify_products_v1
from src.classifier_v2 import classify_products_v2
from src.config import QUERIES, DATA_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Hazmat Classification Pipeline")
    parser.add_argument("--skip-data-collection", action="store_true", help="Skip the data collection step")
    parser.add_argument("--skip-data-processing", action="store_true", help="Skip the data processing step")
    parser.add_argument("--skip-classification", action="store_true", help="Skip the classification step")
    parser.add_argument("--dataset-name", type=str, default="dataset_1", help="Name of the dataset")
    parser.add_argument("--batch-size", type=int, default=1, help="Batch size for classification")
    parser.add_argument("--classifier", type=str, default="v1", choices=["v1", "v2"], help="Which classifier to use: 'v1' (LLM workflow) or 'v2' (LLM agentic system)")
    parser.add_argument("--product-ids", type=str, nargs="*", default=None, help="List of PRODUCT_IDs to classify (space separated). If not set, classify all.")
    parser.add_argument("--output-csv-name", type=str, default=None, help="Custom name for the output classified CSV file.")

    args = parser.parse_args()

    dataset_dir = os.path.join(DATA_DIR, args.dataset_name)
    os.makedirs(dataset_dir, exist_ok=True)

    if not args.skip_data_collection:
        logging.info("Starting data collection...")
        get_product_data(QUERIES, dataset_dir)
        logging.info("Data collection finished.")

    if not args.skip_data_processing:
        logging.info("Starting data processing...")
        convert_json_to_csv(args.dataset_name)
        logging.info("Data processing finished.")

    if not args.skip_classification:
        logging.info(f"Starting classification using '{args.classifier}' classifier...")
        if args.classifier == "v1":
            classify_products_v1(args.dataset_name, args.batch_size, product_ids=args.product_ids, output_csv_name=args.output_csv_name)
        elif args.classifier == "v2":
            classify_products_v2(args.dataset_name, args.batch_size, product_ids=args.product_ids, output_csv_name=args.output_csv_name)
        logging.info("Classification finished.")

if __name__ == "__main__":
    main()
