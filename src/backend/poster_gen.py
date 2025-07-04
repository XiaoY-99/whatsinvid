from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def generate_poster(summary: str, output_path: str) -> str:
    """
    Create a PNG poster containing a translated summary.

    Args:
        summary (str): Translated summary text.
        output_path (str): Path to save the poster image.

    Returns:
        str: Path to the poster image.
    """
    width, height = 800, 1000
    background_color = (245, 245, 245)
    text_color = (30, 30, 30)
    title_color = (0, 102, 204)
    margin = 60
    spacing = 40

    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=40)
        body_font = ImageFont.truetype("DejaVuSans.ttf", size=24)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Optional logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((120, 120))
        img.paste(logo, (width - logo.width - margin, margin), logo)

    # Draw title
    title_text = "Video Summary"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]
    title_x = (width - title_w) // 2
    draw.text((title_x, margin), title_text, fill=title_color, font=title_font)
    
    # Draw wrapped translated summary
    wrapped_summary = textwrap.fill(summary, width=70)
    summary_y = margin + title_h + spacing
    draw.text((margin, summary_y), wrapped_summary, fill=text_color, font=body_font)

    img.save(output_path)
    return output_path
