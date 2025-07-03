from openai import OpenAI
from config.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def translate_text(text: str, target_language: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Translate the following text into {target_language}."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Translation failed: {str(e)}"
