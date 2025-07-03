from openai import OpenAI
from config.settings import settings
from openai.types.chat import ChatCompletion

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarize_text(text: str, language: str = "English", tone: str = "neutral") -> str:
    """
    Summarizes the transcript in a specified tone and language.

    Args:
        text (str): Transcript text
        language (str): Target language for the summary (default: English)
        tone (str): Desired tone/style e.g., "scientific", "business", "marketing" (default: neutral)

    Returns:
        str: The generated summary
    """
    if not text or not text.strip():
        return "Transcript is empty. No summary generated."

    # Customize system message based on tone
    tone_instruction = {
        "scientific": "Use an academic and analytical tone suitable for researchers or experts.",
        "business": "Use a clear, concise, and executive-friendly tone appropriate for business reports.",
        "marketing": "Use a persuasive, engaging, and energetic tone like a marketing copywriter.",
        "neutral": "Use a neutral and informative tone appropriate for general audiences."
    }.get(tone.lower(), tone_instruction := "Use a neutral tone appropriate for general audiences.")

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
