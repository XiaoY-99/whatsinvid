import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

# Create client
client = OpenAI(api_key=api_key)

# Test the GPT-4 or GPT-3.5 model
try:
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": "Say hello from GPT!"}]
    )
    print("✅ GPT Response:\n", response.choices[0].message.content.strip())

except Exception as e:
    print("❌ Error:", str(e))