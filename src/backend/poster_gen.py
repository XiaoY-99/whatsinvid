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
        font_dir = "/usr/share/fonts/truetype/dejavu"
        title_font_path = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
        body_font_path = os.path.join(font_dir, "DejaVuSans.ttf")

        print(f"[INFO] Loading fonts from {title_font_path} and {body_font_path}")

        title_font = ImageFont.truetype(title_font_path, size=40)
        body_font = ImageFont.truetype(body_font_path, size=24)
    except Exception as e:
        print(f"[ERROR] Failed to load fonts: {e}")
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

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

    # Draw title
    title_text = "Video Summary"
    title_w, title_h = draw.textsize(title_text, font=title_font)
    draw.text((margin, margin), title_text, fill=title_color, font=title_font)

    # Draw wrapped translated summary
    wrapped_summary = textwrap.fill(summary, width=70)
    summary_y = margin + title_h + spacing
    draw.text((margin, summary_y), wrapped_summary, fill=text_color, font=body_font)

    # Save image
    img.save(output_path)
    print(f"[INFO] Poster saved to {output_path}")
    return output_path
