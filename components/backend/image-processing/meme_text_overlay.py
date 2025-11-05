"""
Image Processing Component for Meme Generator

Features:
- Text overlay on images
- Multiple meme templates
- Custom font support
- Image resizing and optimization
- PIL-based processing (no external dependencies)
"""

from PIL import Image, ImageDraw, ImageFont
import io
import os
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class MemeTemplate:
    """Pre-defined meme template"""
    id: str
    name: str
    image_url: str
    text_positions: list  # [(x, y, max_width), ...]


# Common meme templates (using placeholder images)
TEMPLATES = {
    "drake": MemeTemplate(
        id="drake",
        name="Drake Hotline Bling",
        image_url="https://i.imgflip.com/30b1gx.jpg",
        text_positions=[(350, 100, 400), (350, 350, 400)]
    ),
    "distracted": MemeTemplate(
        id="distracted",
        name="Distracted Boyfriend",
        image_url="https://i.imgflip.com/1ur9b0.jpg",
        text_positions=[(150, 50, 200), (350, 50, 200), (550, 50, 200)]
    ),
    "two_buttons": MemeTemplate(
        id="two_buttons",
        name="Two Buttons",
        image_url="https://i.imgflip.com/1g8my4.jpg",
        text_positions=[(100, 50, 150), (350, 50, 150), (250, 400, 300)]
    ),
    "success_kid": MemeTemplate(
        id="success_kid",
        name="Success Kid",
        image_url="https://i.imgflip.com/1bhk.jpg",
        text_positions=[(250, 50, 400), (250, 450, 400)]
    ),
}


class ImageProcessor:
    """Process images for meme generation"""

    def __init__(self, font_path: Optional[str] = None, font_size: int = 40):
        """Initialize image processor

        Args:
            font_path: Path to custom font file (uses default if None)
            font_size: Default font size
        """
        self.font_size = font_size

        # Try to load custom font, fall back to default
        try:
            if font_path and os.path.exists(font_path):
                self.font = ImageFont.truetype(font_path, font_size)
            else:
                # Try common font locations
                font_paths = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
                    "/System/Library/Fonts/Helvetica.ttc",  # macOS
                    "C:\\Windows\\Fonts\\Arial.ttf",  # Windows
                ]
                loaded = False
                for path in font_paths:
                    if os.path.exists(path):
                        self.font = ImageFont.truetype(path, font_size)
                        loaded = True
                        break

                if not loaded:
                    self.font = ImageFont.load_default()
        except Exception as e:
            print(f"Error loading font: {e}")
            self.font = ImageFont.load_default()

    def wrap_text(self, text: str, max_width: int, draw: ImageDraw.Draw) -> list:
        """Wrap text to fit within max width

        Args:
            text: Text to wrap
            max_width: Maximum width in pixels
            draw: ImageDraw object for text measurement

        Returns:
            List of wrapped text lines
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=self.font)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw_text_with_outline(
        self,
        draw: ImageDraw.Draw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        text_color: str = "white",
        outline_color: str = "black",
        outline_width: int = 2
    ):
        """Draw text with outline for better visibility

        Args:
            draw: ImageDraw object
            position: (x, y) position
            text: Text to draw
            font: Font to use
            text_color: Main text color
            outline_color: Outline color
            outline_width: Outline thickness
        """
        x, y = position

        # Draw outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)

        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)

    def add_text_to_image(
        self,
        image: Image.Image,
        texts: list,
        positions: Optional[list] = None,
        text_color: str = "white",
        outline_color: str = "black"
    ) -> Image.Image:
        """Add text overlay to image

        Args:
            image: PIL Image object
            texts: List of text strings to add
            positions: Optional list of (x, y, max_width) tuples
            text_color: Text color
            outline_color: Outline color

        Returns:
            Modified PIL Image
        """
        # Create a copy to avoid modifying original
        img = image.copy()
        draw = ImageDraw.Draw(img)

        # Default positions (top and bottom)
        if positions is None:
            img_width, img_height = img.size
            positions = [
                (img_width // 2, 50, img_width - 100),  # Top
                (img_width // 2, img_height - 100, img_width - 100),  # Bottom
            ]

        # Add each text
        for i, text in enumerate(texts):
            if i >= len(positions):
                break

            x, y, max_width = positions[i]

            # Wrap text if needed
            lines = self.wrap_text(text, max_width, draw)

            # Calculate total text height
            line_height = self.font_size + 10
            total_height = len(lines) * line_height

            # Center text vertically around y position
            current_y = y - (total_height // 2)

            # Draw each line
            for line in lines:
                # Calculate text width for centering
                bbox = draw.textbbox((0, 0), line, font=self.font)
                text_width = bbox[2] - bbox[0]

                # Center text horizontally around x position
                text_x = x - (text_width // 2)

                # Draw with outline
                self.draw_text_with_outline(
                    draw,
                    (text_x, current_y),
                    line,
                    self.font,
                    text_color,
                    outline_color
                )

                current_y += line_height

        return img

    def resize_image(
        self,
        image: Image.Image,
        max_width: int = 800,
        max_height: int = 800
    ) -> Image.Image:
        """Resize image while maintaining aspect ratio

        Args:
            image: PIL Image object
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Resized PIL Image
        """
        img_width, img_height = image.size

        # Calculate scaling factor
        width_ratio = max_width / img_width
        height_ratio = max_height / img_height
        scale = min(width_ratio, height_ratio, 1.0)  # Don't upscale

        if scale < 1.0:
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return image

    def create_meme(
        self,
        image_input,  # Can be PIL.Image, bytes, or file path
        texts: list,
        template_id: Optional[str] = None,
        resize: bool = True,
        output_format: str = "PNG"
    ) -> bytes:
        """Create a meme from image and text

        Args:
            image_input: Image source (PIL.Image, bytes, or file path)
            texts: List of text strings to overlay
            template_id: Optional template ID for predefined positioning
            resize: Whether to resize image
            output_format: Output format (PNG, JPEG)

        Returns:
            Image bytes
        """
        # Load image
        if isinstance(image_input, Image.Image):
            img = image_input
        elif isinstance(image_input, bytes):
            img = Image.open(io.BytesIO(image_input))
        elif isinstance(image_input, str):
            img = Image.open(image_input)
        else:
            raise ValueError("Invalid image input type")

        # Convert to RGB if needed (for JPEG)
        if img.mode != 'RGB' and output_format == 'JPEG':
            img = img.convert('RGB')

        # Resize if requested
        if resize:
            img = self.resize_image(img)

        # Get text positions
        positions = None
        if template_id and template_id in TEMPLATES:
            template = TEMPLATES[template_id]
            positions = template.text_positions

        # Add text overlay
        img = self.add_text_to_image(img, texts, positions)

        # Convert to bytes
        output = io.BytesIO()
        img.save(output, format=output_format, quality=95)
        output.seek(0)

        return output.getvalue()


# Simple usage example
if __name__ == "__main__":
    processor = ImageProcessor(font_size=50)

    # Example: Create meme from template
    print("Image processor ready")
    print(f"Available templates: {list(TEMPLATES.keys())}")

    # This would be used in the API like:
    # meme_bytes = processor.create_meme(
    #     image_input=uploaded_file,
    #     texts=["Top text", "Bottom text"],
    #     template_id="drake"
    # )
