import os
import openai

# Use the new v1 client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_visual_concepts(summary: str) -> list[str]:
    """
    Use GPT-4 to extract 1–3 visual concepts (icon-like) from a summary.
    """
    prompt = (
        "You are a helpful assistant. Based on the following summary, suggest 1 to 3 short visual concepts "
        "that would make good icons or illustrations for a poster. Return a Python list of short keywords only.\n\n"
        f"Summary:\n{summary}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        tags = eval(content)
        if isinstance(tags, list):
            return tags
    except Exception as e:
        print(f"[WARNING] Failed to get or parse GPT response: {e}")

    return ["idea", "student", "app"]  # fallback tags
