from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_poster(summary: str, output_path: str) -> str:
    img = Image.new("RGB", (800, 1000), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except:
        font = ImageFont.load_default()

    wrapped_text = textwrap.fill(summary, width=70)
    draw.text((50, 50), wrapped_text, font=font, fill=(0, 0, 0))

    img.save(output_path)
    return output_path
