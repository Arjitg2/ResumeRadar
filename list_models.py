from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models
print("Available Gemini Models:")
print("-" * 80)
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model Name: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Supported Methods: {model.supported_generation_methods}")
        print("-" * 80)
