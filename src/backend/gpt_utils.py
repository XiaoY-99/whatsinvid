from openai import OpenAI
from config.settings import settings  # if using centralized config

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarize_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that produces short, concise abstracts of video/audio transcripts. "
                    "Summarize the key topic, purpose, and main points of the content in 1-2 paragraphs."
                ),
            },
            {"role": "user", "content": f"Transcript:\n{text}\n\nGenerate an abstract:"}
        ]
    )
    return response.choices[0].message.content.strip()

