

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import requests
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

app = FastAPI()

# ✅ Allow frontend (Streamlit) access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Helper: Load JSON from file
def load_json_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load {file_path}: {e}")
        return []

# ✅ Routes for each resource
@app.get("/")
def root():
    return {"message": "Marriage Planner Backend Running ✅"}

@app.get("/venues")
def get_venues(city: str = Query(None)):
    data = load_json_data("data/venues.json")
    if city:
        data = [v for v in data if v["location"].lower() == city.lower()]
    return data

@app.get("/caterers")
def get_caterers():
    return load_json_data("data/caterers.json")

@app.get("/photographers")
def get_photographers():
    return load_json_data("data/photographers.json")

@app.get("/invitations")
def get_invitations():
    return load_json_data("data/invitations.json")

# ✅ AI assistant using Together AI
def ask_llm(user_query, context_data):
    prompt = f"""
You are a smart Indian wedding planner AI.

User question: {user_query}

Here is some service data you can use:
{context_data}

Based on this, suggest the best wedding plan with estimated costs.
Include venue, food, photography, and invitations if relevant.
"""

    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
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

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ LLM API request failed:", e)
        return "⚠️ AI failed to generate a response."

# ✅ Main route for AI query
@app.post("/ask")
def ask_planner(query: str):
    try:
        venues = load_json_data("data/venues.json")
        caterers = load_json_data("data/caterers.json")
        photographers = load_json_data("data/photographers.json")
        invitations = load_json_data("data/invitations.json")

        all_data = {
            "venues": venues,
            "caterers": caterers,
            "photographers": photographers,
            "invitations": invitations
        }

        print("📥 User Query:", query)
        print("📦 Combined Data:", all_data)

        llm_response = ask_llm(query, all_data)
        print("🧠 LLM Response:", llm_response)

        return {"response": llm_response}

    except Exception as e:
        print("❌ Backend error:", e)
        return {"response": f"⚠️ Backend Error: {e}"}
