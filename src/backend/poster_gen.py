from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


def generate_poster(summary: str, output_path: str) -> str:
    """
    Create a PNG poster containing a translated summary with dynamic height support.

    Args:
        summary (str): Translated summary text.
        output_path (str): Path to save the poster image.

    Returns:
        str: Path to the poster image.
    """
    width = 800
    margin = 60
    spacing = 40
    background_color = (245, 245, 245)
    text_color = (30, 30, 30)
    title_color = (0, 102, 204)

    # Load fonts with multilingual support
    try:
        font_dir = "/usr/share/fonts/truetype"
        title_font_path = os.path.join(font_dir, "dejavu/DejaVuSans-Bold.ttf")
        body_font_path = os.path.join(font_dir, "noto/NotoSansCJK-Regular.ttc")

        print(f"[INFO] Loading fonts from:\n - {title_font_path}\n - {body_font_path}")
        title_font = ImageFont.truetype(title_font_path, size=40)
        body_font = ImageFont.truetype(body_font_path, size=26)
    except Exception as e:
        print(f"[ERROR] Failed to load custom fonts: {e}")
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Wrap text and estimate height
    dummy_img = Image.new("RGB", (width, 1000))
    draw_dummy = ImageDraw.Draw(dummy_img)

    wrapped_summary = textwrap.wrap(summary, width=60)
    text_height = sum(draw_dummy.textsize(line, font=body_font)[1] + 10 for line in wrapped_summary)
    total_height = text_height + margin * 3 + 40  # +title +margins

    # Create image canvas with computed height
    img = Image.new("RGB", (width, total_height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Draw title
    title_text = "Video Summary"
    title_w, title_h = draw.textsize(title_text, font=title_font)
    draw.text((margin, margin), title_text, fill=title_color, font=title_font)

    # Draw wrapped summary
    y = margin + title_h + spacing
    for line in wrapped_summary:
        draw.text((margin, y), line, fill=text_color, font=body_font)
        y += draw.textsize(line, font=body_font)[1] + 10

    # Optional logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((120, 120))
            img.paste(logo, (width - logo.width - margin, margin), logo)
            print(f"[INFO] Logo added from {logo_path}")
        except Exception as e:
            print(f"[WARNING] Failed to add logo: {e}")
    else:
        print("[INFO] No logo file found.")

    img.save(output_path)
    print(f"[INFO] Poster saved to {output_path}")
    return output_path
