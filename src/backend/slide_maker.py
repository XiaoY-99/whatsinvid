from pptx import Presentation
from pptx.util import Inches
import os

def generate_slides(summary: str, output_path: str) -> str:
    prs = Presentation()
    slide_layout = prs.slide_layouts[1]

    for idx, bullet in enumerate(summary.split('\n')):
        if bullet.strip():
            slide = prs.slides.add_slide(slide_layout)
            title = slide.shapes.title
            content = slide.placeholders[1]
            title.text = f"Point {idx+1}"
            content.text = bullet.strip()

    prs.save(output_path)
    return output_path
