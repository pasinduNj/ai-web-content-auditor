import re
import os
from dotenv import load_dotenv

# Load env variables at the module level
load_dotenv()

def distill_content(raw_text):
    """
    Cleans and reduces noise in the text content to focus only on 
    high-value brand messaging for the LLM.
    """
    # 1. Remove common web "noise" using regex (extra spaces/newlines)
    clean_text = re.sub(r'\s+', ' ', raw_text).strip()
    
    # 2. Retrieve boilerplate from .env
    boilerplate_env = os.getenv("BOILERPLATE_WORDS", "")
    
    if boilerplate_env:
        # Split by comma and strip quotes/whitespace
        boilerplate = [w.strip().strip('"').strip("'") for w in boilerplate_env.split(",") if w.strip()]
        
        for word in boilerplate:
            # Case-insensitive replacement to be more thorough
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            clean_text = pattern.sub("", clean_text)
        
    # 3. Final whitespace cleanup after replacements
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
    return clean_text[:1000]

def structure_content(results_dict):
    """
    Formats the crawler's raw dictionary into a list of distilled 
    content blocks ready for the LLM task loop.
    """
    structured_list = []
    for url, raw_content in results_dict.items():
        # Apply the distillation to each page's content
        distilled = distill_content(raw_content)
        
        structured_list.append({
            "page": url,
            "content": distilled
        })
    return structured_list