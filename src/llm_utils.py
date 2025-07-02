"""
llm_utils.py
Reusable LLM call and prompt utilities for the Hazmat Classifier project.
"""
import os
from typing import Optional
import litellm

def call_llm(system: str, prompt: str, model: str, max_tokens: Optional[int] = 10000, temperature: Optional[float] = 0.7) -> str:
    """Call the LLM with a system prompt and user prompt. Model can be set via env or argument."""
    # Example: Replace with your actual LLM API call

    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()

# Add more LLM-related utilities as needed
