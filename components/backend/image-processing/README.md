# Meme Text Overlay (Python)

Image processing helper built on Pillow for adding meme-style text (top/bottom captions) with outlines.

## Install
```bash
pip install pillow
```

## Usage
```python
from meme_text_overlay import ImageProcessor

processor = ImageProcessor(font_path="./Impact.ttf", font_size=48)
with open("input.jpg", "rb") as f:
    meme_bytes = processor.create_meme(
        image_input=f.read(),
        texts=["Top text", "Bottom text"],
        output_format="PNG",
    )
```

Supports PNG/JPEG input, automatic resizing, and configurable outline thickness.
