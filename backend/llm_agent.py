import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

def ask_llm(user_query, context_data):
    prompt = f"""
You are a smart Indian wedding planner assistant.

User question: {user_query}

Here is some reference data you can use:
{context_data}

Give a helpful and short recommendation with cost estimates and service options.
"""

    payload = {
        "model": "meta-llama-3-8b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful wedding planner assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
