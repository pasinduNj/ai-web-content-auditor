import ollama
import json

def analyze_content(page_name, text_content):
    
    prompt = f"""
    <start_of_turn>user
    You are a professional Website Auditor and Brand Strategist. 
    Analyze the following content for the page: {page_name}
    
    TASK 1: CONTENT AUDIT
    Identify specific improvements for clarity, grammar, tone, and engagement. 
    Identify missing content gaps (e.g., missing CTAs, social proof, or FAQs).

    TASK 2: TONE ANALYSIS
    Rate the following metrics on a scale of 1 to 10 (where 10 is the highest):
    - Professionalism: How formal and business-like is the writing?
    - Urgency: Does it encourage the user to act immediately?
    - Clarity: How easy is it for a 5th grader to understand?
    - Trust: Does the content build credibility and authority?

    ### CONSTRAINTS:
    - Return ONLY a valid JSON object.
    - Be concise. One sentence per 'change' and 'reason'.
    
    ### EXPECTED JSON STRUCTURE:
    {{
        
        "improvements": [
            {{"section": "...", "issue": "...", "change": "...", "reason": "..."}}
        ],
        "gaps": [
            {{"missing": "...", "location": "...", "outline": "...", "reason": "..."}}
        ],
        "scores": {{
            "professionalism": 0,
            "urgency": 0,
            "clarity": 0,
            "trust": 0
        }}
    }}

    ### CONTENT:
    {text_content[:1000]}
    <end_of_turn>
    <start_of_turn>model
    """

    try:
        response = ollama.generate(
            model='gemma2:2b', 
            prompt=prompt, 
            format='json',
            options={'temperature': 0.2}
        )
        return json.loads(response['response'])
    except Exception as e:
        return {
            "scores": {"professionalism": 0, "urgency": 0, "clarity": 0, "trust": 0},
            "error": f"LLM Analysis failed: {str(e)}"
        }