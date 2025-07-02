"""
llm_utils.py
Reusable LLM call and prompt utilities for the Hazmat Classifier project.
"""
import os
from typing import Optional

def call_llm(system: str, prompt: str, model: Optional[str] = None) -> str:
    """Call the LLM with a system prompt and user prompt. Model can be set via env or argument."""
    # Example: Replace with your actual LLM API call
    import openai
    model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Add more LLM-related utilities as needed
