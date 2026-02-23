import json


import torch
from google import genai

import automation
import detact_data_type
import os

# ================= MEMORY =================

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump({}, f)
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

memory = load_memory()

def handle_memory(query):
    query = query.lower().strip()

    if query.startswith("remember"):
        data = query.replace("remember", "").strip()

        if " is " in data:
            key, value = data.split(" is ", 1)
            memory[key.strip()] = value.strip()
            save_memory(memory)
            return f"I will remember that {key.strip()} is {value.strip()}."

        memory[data] = True
        save_memory(memory)
        return "Noted."

    if query.startswith("what is my"):
        key = query.replace("what is my", "").strip()
        if key in memory:
            return f"Your {key} is {memory[key]}."
        return "I do not have that information yet."

    return None


# ================= TINYLLAMA MODEL =================

def chat():
    import requests

    API_KEY = "your_api_key"

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )

    print(response.json()["choices"][0]["message"]["content"])

# ================= GEMINI FALLBACK (OPTIONAL) =================

GEMINI_KEY = os.getenv("your_api_key")

if GEMINI_KEY:
    client = genai.Client(api_key=GEMINI_KEY)
    chat_history = []

    system_prompt = """
You are Jarvis, an advanced AI assistant.
Respond clearly and stay in context.
"""

    def chat_gemini(prompt):
        global chat_history

        chat_history.append(f"User: {prompt}")
        full_prompt = system_prompt + "\n" + "\n".join(chat_history)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        reply = response.text.strip()
        chat_history.append(f"Jarvis: {reply}")

        return reply
else:
    client = None


# ================= WIKIPEDIA =================

def local_data(search):
    import wikipedia
    wikipedia.set_lang("en")
    try:
        return wikipedia.summary(search, sentences=1)
    except:
        return "I couldn't find reliable information."


# ================= REAL-TIME DATA =================

def get_real_time_data(query):
    from ddgs import DDGS
    import sys

    try:
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)

        sys.stdout.close()
        sys.stdout = old_stdout

        for r in results:
            snippet = r.get("body", "").strip()
            if len(snippet) > 40:
                return snippet[:200]

        return "No news available."

    except:
        return "News service unavailable."


# ================= ROUTER =================

def assistant_router(query):
    intent, confidence = detact_data_type.detect_intent(query)

    if intent == "real_time":
        return get_real_time_data(query)

    elif intent == "knowledge":
        return local_data(query)

    elif intent == "memory":
        return handle_memory(query)

    elif intent == "automation":
        automation.auto(query)
        return None

    elif intent == "chat":
        response = chat(query)

        if client and len(response) < 5:
            return chat_gemini(query)

        return response

    else:
        return chat(query)


# ================= MAIN =================

def run_jarvis(query):
    response = assistant_router(query)
    if response is not None:
        print("Jarvis:", response)
