from config.settings import settings
from openai import OpenAI

def test_openai_response():
    assert settings.OPENAI_API_KEY is not None, "❌ OPENAI_API_KEY not loaded from config/default.env"

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say hello from GPT!"}]
    )

    content = response.choices[0].message.content.strip().lower()
    assert "hello" in content
    print("✅ GPT Response:", content)

