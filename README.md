# Hazmat Classifier

A modular and reproducible pipeline for classifying products as hazardous materials (Hazmat) using Large Language Models (LLMs).

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Overview

This project provides a complete pipeline to:

1.  **Collect product data** from Mercado Livre using a combination of scraping and their official API.
2.  **Process the raw data** into a structured format (CSV).
3.  **Classify products** as Hazmat or not using an LLM.

The pipeline is designed to be modular, configurable, and reproducible.

## Architecture

This diagram illustrates the currently implemented architecture of the Hazmat Classifier pipeline.

![Architecture V1](docs/img/architecture-v1.png)

A proposed updated architecture for future enhancements.

![Architecture V2](docs/img/architecture-v2.png)

## Workflow

The pipeline consists of three main stages:

1.  **Data Collection (`data_collection.py`):**
    - Scrapes product IDs from Mercado Livre search results based on a predefined list of queries.
    - Fetches detailed product information for each ID using the Mercado Livre API.
    - Saves the raw data as JSON files.

2.  **Data Processing (`data_processing.py`):**
    - Reads the raw JSON data.
    - Extracts relevant fields (ID, title, attributes).
    - Converts the data into a single CSV file.

3.  **Classification (`classifier_v1.py` and `classifier_v2.py`):**
    - Reads the processed CSV file.
    - Sends product information to an LLM in batches.
    - The LLM classifies each product as Hazmat or not based on a provided definition.
    - Saves the classified data to a new CSV file, along with the LLM's reasoning and confidence level.

## Directory Structure

```
hazmat-classifier/
├── data/
│   ├── dataset_1/
│   └── hazmat-definition.md
├── docs/
│   └── img/
├── notebooks/
├── src/
├── .env.example
├── main.py
├── poetry.lock
├── prompts.txt
├── pyproject.toml
└── README.md
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/hazmat-classifier.git
    cd hazmat-classifier
    ```

2.  **Install dependencies:**
    This project uses Poetry for dependency management.
    ```bash
    poetry install
    ```

## Configuration

1.  **Environment Variables:**
    - Create a `.env` file by copying the example file:
      ```bash
      cp .env.example .env
      ```
    - Open the `.env` file and add your Mercado Livre API access token and any LLM API keys.

2.  **Pipeline Configuration (`src/config.py`):**
    - The `src/config.py` file contains all the configurable parameters for the pipeline, such as API endpoints, model names, file paths, and the list of search queries.

## Usage

The pipeline is executed through the `main.py` script.

### Running the Full Pipeline

To run all stages of the pipeline (data collection, processing, and classification with default settings), simply run:

```bash
python main.py
```

### Command-Line Arguments

You can customize the pipeline's execution with the following command-line arguments:

-   **Stage Control:**
    -   `--skip-data-collection`: Skips the data collection stage.
    -   `--skip-data-processing`: Skips the data processing stage.
    -   `--skip-classification`: Skips the classification stage.

-   **Dataset and Classification Configuration:**
    -   `--dataset-name <name>`: Sets the name of the dataset directory (default: `dataset_1`).
    -   `--batch-size <size>`: Sets the batch size for classification (default: `1`).
    -   `--classifier <v1|v2>`: Chooses which classifier to use. `v1` is a standard LLM workflow, and `v2` is an LLM agentic system (default: `v1`).
    -   `--product-ids <ID1> <ID2> ...`: Classifies a specific list of product IDs instead of the entire dataset.
    -   `--output-csv-name <filename>`: Specifies a custom name for the output CSV file with classified products.

### Examples

-   **Run only the classification stage:**
    ```bash
    python main.py --skip-data-collection --skip-data-processing
    ```

-   **Run classification using the `v2` classifier on a different dataset:**
    ```bash
    python main.py --skip-data-collection --skip-data-processing --dataset-name my_dataset --classifier v2
    ```

-   **Classify specific products with a custom output name:**
    ```bash
    python main.py --skip-data-collection --skip-data-processing --product-ids MLB123 MLB456 --output-csv-name custom_results.csv
    ```