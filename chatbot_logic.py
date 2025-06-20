import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from prompt_utils import clean_prompt

# === Handle path for bundled .env ===
def get_asset_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.abspath(filename)

# === Load environment file correctly ===
dotenv_path = get_asset_path(".env")
load_dotenv(dotenv_path)
api_key = os.getenv("GEMINI_API_KEY")

# DEBUG LOG
with open("log.txt", "a") as f:
    f.write("Loaded GEMINI_API_KEY: " + str(api_key) + "\n")

# === Configure Gemini ===
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# === Define chatbot response logic ===
def get_bot_response(user_input):
    try:
        prompt = clean_prompt(user_input)
        with open("log.txt", "a") as f:
            f.write("[DEBUG] Final Prompt: " + prompt + "\n")
        response = model.generate_content(prompt)
        if response and hasattr(response, "text"):
            return response.text if response.text.strip() else "[I didn't get that.]"
        else:
            return "[I didn't get that.]"
    except Exception as e:
        with open("log.txt", "a") as f:
            f.write("[ERROR] " + str(e) + "\n")
        return "[Oops! Something broke.]"