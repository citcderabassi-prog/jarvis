import json


import torch
from google import genai

import automation
import detact_data_type
import os
os.environ.pop("HF_HOME", None)
os.environ.pop("HUGGINGFACE_HUB_CACHE", None)
os.environ.pop("HF_TOKEN", None)
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



from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/DialoGPT-small"# small GPT model

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

chat_history_ids = None

def chat_gemini(user_input):
    global chat_history_ids

    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt').to(device)

    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_new_tokens=60,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )

    return response.strip()


# ================= GEMINI FALLBACK (OPTIONAL) =================

GEMINI_KEY = os.getenv("AIzaSyD6obmlHV3qWxfz0uQ_6zx-jAHQQksOcNA")

if GEMINI_KEY:
    client = genai.Client(api_key=GEMINI_KEY)
    chat_history = []

    system_prompt = """
You are Jarvis, an advanced AI assistant.
Respond clearly and stay in context.
"""

    def chat(prompt):
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