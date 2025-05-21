import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes video transcripts."},
            {"role": "user", "content": f"Summarize this transcript:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()
