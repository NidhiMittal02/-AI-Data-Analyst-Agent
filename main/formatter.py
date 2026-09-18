import requests
import os
from dotenv import load_dotenv
import random
import json

load_dotenv()

key = os.getenv('AI_PIPE_API_KEY')
key1 = os.getenv('AI_PIPE_API_KEY1')
key2 = os.getenv('AI_PIPE_API_KEY2')
key3 = os.getenv('AI_PIPE_API_KEY3')
key4 = os.getenv('AI_PIPE_API_KEY4')
pkey = os.getenv('PERPLEXITY_API_KEY')
gkey = os.getenv('GROK_API_KEY')

keys = {
    "PER":pkey,
    "AI":key,
    "AI1":key1,
    "AI2":key2,
    "AI3":key3,
    "AI4":key4
}

def safe_serialize(data):
    try:
        # Try to serialize as JSON for structure
        return json.dumps(data, ensure_ascii=False)
    except (TypeError, ValueError):
        # Fallback to plain string
        return str(data)
    
def format(input,output):
    # output and input provide krke pucho ki correct format hain kya which is needed, if not, make it correct 

    ty = 'AI'
    if random.randint(0,4)!=0:
        ty += str(random.randint(1,4))
    
    for i in range(5):
        # randomnum = random.randint(0,4)
        api_url = "https://aipipe.org/openrouter/v1/chat/completions"
        try:
            headers = {
                "Authorization": f"Bearer {keys[ty]}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openai/gpt-4.1" if ty != 'PER' else "sonar-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "You must return the output **exactly** in the structure required by the Problem Statement. "
                            "Do NOT add explanations, notes, or any extra text. "
                            "The response must match the required format perfectly.\n\n"
                            "=== Problem Statement ===\n"
                            f"{input}\n\n"
                            "=== Raw Output ===\n"
                            f"{safe_serialize(output)}\n\n"
                            "Now reformat the Raw Output so that it follows the Problem Statement EXACTLY. "
                            "without quotation marks, booleans as true/false, and strings with quotes only if required by the format. "
                            "Return ONLY the final structured output in valid JSON."
                            "For any base64 answers, replace them with 'empty' (in string format), just make sure that the remaining answer are in correct format and overall format is correct as required by the problem."
                            "Very Important: Ensure that all numbers are returned as proper numeric values (integers or floats) like 1 must not be returned as '1' but as 1, it must be as asked in the problem statement."
                        )

                    }
                ],
            }
            if ty=='PER':
                payload['max_tokens'] = 1000

            response = requests.post(api_url, headers=headers, json=payload)

            return response.json()['choices'][0]['message']['content']
        except:
            ty = 'AI'
            if random.randint(0,4)!=0:
                ty += str(random.randint(1,4))

    return output