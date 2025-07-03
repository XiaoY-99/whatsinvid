from openai import OpenAI
from config.settings import settings
from openai.types.chat import ChatCompletion

# Correct way to initialize OpenAI client with new SDK (v1.x+)
client = OpenAI()  # Don't pass api_key here

def summarize_text(text: str, language: str = "English", tone: str = "neutral") -> str:
    if not text or not text.strip():
        return "Transcript is empty. No summary generated."

    tone_instruction = {
        "scientific": "Use an academic and analytical tone suitable for researchers or experts.",
        "business": "Use a clear, concise, and executive-friendly tone appropriate for business reports.",
        "marketing": "Use a persuasive, engaging, and energetic tone like a marketing copywriter.",
        "neutral": "Use a neutral and informative tone appropriate for general audiences."
    }.get(tone.lower(), "Use a neutral tone appropriate for general audiences.")

    try:
        response: ChatCompletion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are an assistant that produces short, high-quality summaries of video/audio transcripts. "
                        f"{tone_instruction} Summarize the key topic, purpose, and main points in 1-2 paragraphs. "
                        f"Respond in {language}."
                    ),
                },
                {"role": "user", "content": f"Transcript:\n{text.strip()}\n\nGenerate an abstract:"}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Summary generation failed: {str(e)}"
