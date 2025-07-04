import openai

def get_visual_concepts(summary: str) -> list[str]:
    """
    Use GPT-4 to extract 1–3 visual concepts (icon-like) from a summary.
    """
    prompt = (
        "You are a helpful assistant. Based on the following summary, suggest 1 to 3 short visual concepts "
        "that would make good icons, stickers, or illustrations for a poster. These should be simple objects, ideas, or scenes. "
        "Just return a Python list of short keywords.\n\n"
        f"Summary:\n{summary}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    try:
        tags = eval(response.choices[0].message['content'])
        if isinstance(tags, list):
            return tags
    except Exception as e:
        print(f"[WARNING] Failed to parse visual concepts: {e}")

    return ["idea", "student", "app"]  # Fallback
