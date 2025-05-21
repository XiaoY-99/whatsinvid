from openai import OpenAI
from config.settings import settings  # if using centralized config

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarize_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes video transcripts."},
            {"role": "user", "content": f"Summarize this transcript:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

