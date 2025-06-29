# Code to create function to call LLM receiving a prompt and returning the response

import litellm

def call_llm(system, prompt, model="groq/llama-3.3-70b-versatile", temperature=0.7):
    """
    Calls the LLM with the given system and user prompt and returns the response.
    Args:
        system (str): The system message to set the assistant's behavior.
        prompt (str): The prompt to send to the LLM as the user message.
        model (str): The model to use.
        temperature (float): Sampling temperature.
        max_tokens (int): Maximum number of tokens in the response.
    Returns:
        str: The LLM's response.
    """
    response = litellm.completion(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response['choices'][0]['message']['content']


# Export content between tags <tag> from input string, using regex.
def extract_from_tag(input_string, tag):
    import re
    pattern = f"<{tag}>(.*?)</{tag}>"
    matches = re.findall(pattern, input_string, re.DOTALL)
    return matches[0] if matches else None
