import pandas as pd
import os
import logging
from src.models import Confidence, HazmatClassification

from src.data_utils import get_hazmat_definition, extract_from_tag
from src.config import DATA_DIR, INFO_EXTRACTOR_MODEL, DEFAULT_MODEL, SEARCH_AGENT_MODEL, NON_HAZMAT_PRODUCTS
from src.llm_utils import call_llm
from agents.agents import create_sds_search_agent, create_composition_search_agent, query_agent
from src.prompts import HAZMAT_CLASSIFIER_SYSTEM_MSG, HAZMAT_JSON_EXTRACTOR_SYSTEM_MSG, NON_HAZMAT_LIST_CHECK_PROMPT, SDS_FOUND_EXTRACTION_PROMPT, HAZMAT_CLASSIFIER_WITH_JSON_OUTPUT_SYSTEM_MSG


def classify_products_v2(dataset_name="dataset_1", product_ids=None, output_csv_name=None):
    """
    Args:
        dataset_name (str): Name of the dataset to classify.
        batch_size (int): Number of products per batch.
        product_ids (list, optional): List of product IDs to classify. If None, all products in the dataset will be classified.
        output_csv_name (str, optional): Name of the output CSV file. If None, defaults to 'hazmat_classification_results.csv'.
    Returns
    """
    
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

    # Create the agent runner
    sds_search_agent = create_sds_search_agent(model=SEARCH_AGENT_MODEL)
    composition_search_agent = create_composition_search_agent(model=SEARCH_AGENT_MODEL)

    # Process products row by row using iterrows
    results = []
    for idx, row in products_df.iterrows():
        
        product_id = row.get('PRODUCT_ID')
        product_title = row.get('TITLE')
        product_attributes = row.get('ATTRIBUTES')
        product_row_str = row.to_json()

        # First step: Check if product is in non-hazmat products list using LLM
        res = call_llm(
            system=NON_HAZMAT_LIST_CHECK_PROMPT.format(non_hazmat_products=NON_HAZMAT_PRODUCTS),
            prompt=product_title,
            model=DEFAULT_MODEL,
        )

        analysis = extract_from_tag(res, "analysis")
        answer = extract_from_tag(res, "answer")

        if answer.strip().lower() == "yes":
            result_row = HazmatClassification(
                product_id=product_id,
                is_hazmat=False,
                reason=f"Product is in non-hazmat list: {analysis}",
                confidence=Confidence.HIGH
            )
            results.append(result_row.model_dump())
            continue

        # Second step: Query SDS agent and then check if SDS or FISPQ documents were found
        sds_info = query_agent(sds_search_agent, f"Find the SDS or FISPQ for {product_title}.")
        res = call_llm(
            system=SDS_FOUND_EXTRACTION_PROMPT,
            prompt=sds_info,
            model=INFO_EXTRACTOR_MODEL,
        )
        sds_found = extract_from_tag(res, "sds_found")

        if sds_found.strip().lower() == "yes":
            # Send the SDS information to classifier agent
            res = call_llm(
                system=HAZMAT_CLASSIFIER_SYSTEM_MSG.format(
                    hazmat_def=hazmat_def,
                    output_json_schema=HazmatClassification.model_json_schema(),
                ),
                prompt=f"""
                Product information:
                <product_info>{product_row_str}</product_info>

                SDS/FISPQ search results:
                <sds_info>{sds_info}</sds_info>
                """,
                model=DEFAULT_MODEL,
            )
            # Extract JSON content from the response
            res = call_llm(
                system=HAZMAT_JSON_EXTRACTOR_SYSTEM_MSG.format(
                    hazmat_def=hazmat_def,
                    output_json_schema=HazmatClassification.model_json_schema(),
                ),
                prompt=res,
                model=INFO_EXTRACTOR_MODEL,
            )
            json_content = extract_from_tag(res, "jsonl")
            result_row = HazmatClassification.model_validate_json(json_content)
            results.append(result_row.model_dump())
            continue

        # Third step: (Placeholder) Check for hazmat label in images (to be implemented)
        

        # Fourth step: Check for chemicals quantities in composition 
        composition_info = query_agent(composition_search_agent, f"Find the chemical composition for {product_title}.")
        res = call_llm(
            system=HAZMAT_CLASSIFIER_WITH_JSON_OUTPUT_SYSTEM_MSG.format(
                hazmat_def=hazmat_def,
                output_json_schema=HazmatClassification.model_json_schema(),
            ),
            prompt=f"""
            Product information:
            <product_info>{product_row_str}</product_info>

            SDS/FISPQ search results:
            <sds_info>{sds_info}</sds_info>

            Composition information:
            <composition_info>{composition_info}</composition_info>
            """,
            model=DEFAULT_MODEL,
        )
        # Extract JSON content from the response
        res = call_llm(
            system=HAZMAT_JSON_EXTRACTOR_SYSTEM_MSG.format(
                json_schema=HazmatClassification.model_json_schema(),
            ),
            prompt=res,
            model=INFO_EXTRACTOR_MODEL,
        )
        json_content = extract_from_tag(res, "jsonl")

        if not json_content:
            json_content = res  # Fallback to raw response if no tag found

        try:
            result_row = HazmatClassification.model_validate_json(json_content)
        except Exception as e:
            logging.error(f"Error validating JSON content: {e}")
            result_row = HazmatClassification(
                product_id=product_id,
                is_hazmat=True,
                reason="Error validating JSON content",
                confidence=Confidence.LOW
            )
        results.append(result_row.model_dump())

    results_df = pd.DataFrame(results)
    output_csv = output_csv_name or f"{dataset_name}_v2_results.csv"
    output_path = os.path.join(DATA_DIR, dataset_name, output_csv)
    results_df.to_csv(output_path, index=False, encoding="utf-8")
    logging.info(f"Products classification complete. Results saved to {output_path}")