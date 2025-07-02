from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def generate_poster(summary: str, output_path: str) -> str:
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

    # Optional: paste logo (make sure logo.png is in the working directory)
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((120, 120))
        img.paste(logo, (width - logo.width - margin, margin), logo)  # paste with transparency

    # Draw title
    title_text = "Video Summary"
    title_w, title_h = draw.textsize(title_text, font=title_font)
    draw.text((margin, margin), title_text, fill=title_color, font=title_font)

    # Wrap and draw summary text
    wrapped_summary = textwrap.fill(summary, width=70)
    summary_y = margin + title_h + spacing
    draw.text((margin, summary_y), wrapped_summary, fill=text_color, font=body_font)

    # Save the poster
    img.save(output_path)
    return output_path
