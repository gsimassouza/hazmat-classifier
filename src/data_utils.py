"""
data_utils.py
Reusable data loading, saving, and transformation utilities for the Hazmat Classifier project.
"""
import pandas as pd
import json
import os
from typing import List, Dict, Any, Optional

def load_jsonl(file_path: str, encoding: str = "utf-8") -> List[Dict[str, Any]]:
    """Load a JSONL file, returning a list of dicts. Tries utf-8, then latin-1."""
    try:
        with open(file_path, encoding=encoding) as f:
            return [json.loads(line) for line in f if line.strip()]
    except UnicodeDecodeError:
        with open(file_path, encoding="latin-1") as f:
            return [json.loads(line) for line in f if line.strip()]

def save_jsonl(data: List[Dict[str, Any]], file_path: str, encoding: str = "utf-8"):
    """Save a list of dicts to a JSONL file."""
    with open(file_path, "w", encoding=encoding) as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def load_csv(file_path: str, **kwargs) -> pd.DataFrame:
    """Load a CSV file as a DataFrame, normalizing column names to uppercase."""
    df = pd.read_csv(file_path, **kwargs)
    df.columns = [c.upper() for c in df.columns]
    return df

def save_csv(df: pd.DataFrame, file_path: str, **kwargs):
    """Save a DataFrame to CSV with utf-8 encoding."""
    df.to_csv(file_path, index=False, encoding="utf-8", **kwargs)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the DataFrame with all column names uppercased."""
    df2 = df.copy()
    df2.columns = [c.upper() for c in df2.columns]
    return df2

def merge_on_product_id(main_df: pd.DataFrame, classified_df: pd.DataFrame, columns_to_merge: List[str]) -> pd.DataFrame:
    """Merge selected columns from classified_df into main_df on PRODUCT_ID (case-insensitive)."""
    main_df = normalize_columns(main_df)
    classified_df = normalize_columns(classified_df)
    columns = [c.upper() for c in columns_to_merge]
    columns = ["PRODUCT_ID"] + [c for c in columns if c != "PRODUCT_ID"]
    merged = pd.merge(main_df, classified_df[columns], on="PRODUCT_ID", how="left")
    return merged

def fetch_wikipedia_html(article: str) -> str:
    """Fetch raw HTML for a Wikipedia article using the MediaWiki API."""
    import requests
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'parse',
        'page': article,
        'format': 'json',
        'prop': 'text'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['parse']['text']['*']

def convert_html_to_markdown(html: str) -> str:
    """Convert HTML to markdown using html_to_markdown if available."""
    try:
        from html_to_markdown import convert_to_markdown
        return convert_to_markdown(html)
    except ImportError:
        raise ImportError("html_to_markdown package is required for HTML to markdown conversion.")

def save_markdown(md: str, file_path: str):
    """Save markdown text to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md)

def extract_from_tag(text: str, tag: str) -> Optional[str]:
    """Extract content from a given tag in a string."""
    start_tag = f"<{tag}>"
    end_tag = f"</{tag}>"
    start_index = text.find(start_tag)
    if start_index == -1:
        return None
    start_index += len(start_tag)
    end_index = text.find(end_tag, start_index)
    if end_index == -1:
        return None
    return text[start_index:end_index].strip()
