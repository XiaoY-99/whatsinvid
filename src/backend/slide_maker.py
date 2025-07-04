from pptx import Presentation
from pptx.util import Inches
import os

def generate_slides(summary: str, output_path: str) -> str:
    """
    Generate a PowerPoint file from a translated summary using a template with a pre-inserted logo.

    Args:
        summary (str): Translated summary (multiline).
        output_path (str): Path to save the PPTX file.

    Returns:
        str: Path to the generated slide file.
    """
    base_dir = os.path.dirname(__file__)
    template_path = os.path.join(base_dir, "template_with_logo.pptx")

    # Load the template
    prs = Presentation(template_path)
    slide_layout = prs.slide_layouts[1]  # Usually "Title and Content"

    for idx, bullet in enumerate(summary.split('\n')):
        bullet = bullet.strip()
        if not bullet:
            continue

        slide = prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        content = slide.placeholders[1]

        title.text = f"Point {idx + 1}"
        content.text = bullet

    prs.save(output_path)
    return output_path
