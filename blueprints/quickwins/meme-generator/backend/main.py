"""
Meme Generator FastAPI Server

Features:
- Upload custom images or use templates
- Add text overlay with customization
- Download generated memes
- Gallery of recent memes
- RESTful API
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import Response, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from pathlib import Path

from image_processor import ImageProcessor, TEMPLATES
from storage import create_storage

# Initialize
app = FastAPI(
    title="Meme Generator API",
    description="Create memes with custom images and text overlays",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
processor = ImageProcessor(font_size=50)
storage = create_storage()

# Mount uploads directory for static file serving
uploads_dir = Path("./uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# ============================================================================
# MODELS
# ============================================================================

class MemeRequest(BaseModel):
    """Meme creation request"""
    texts: List[str]
    template_id: Optional[str] = None
    resize: bool = True
    output_format: str = "PNG"


class MemeResponse(BaseModel):
    """Meme creation response"""
    file_id: str
    url: str
    message: str


class TemplateInfo(BaseModel):
    """Template information"""
    id: str
    name: str
    image_url: str
    text_count: int


# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Meme Generator API",
        "version": "1.0.0",
        "endpoints": {
            "create_meme": "POST /api/create",
            "create_from_template": "POST /api/create/template/{template_id}",
            "get_templates": "GET /api/templates",
            "get_meme": "GET /api/memes/{file_id}",
            "list_memes": "GET /api/memes",
            "delete_meme": "DELETE /api/memes/{file_id}",
            "health": "GET /health",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "processor": "ready",
        "storage": type(storage).__name__,
        "templates": len(TEMPLATES)
    }


@app.get("/api/templates", response_model=List[TemplateInfo])
async def get_templates():
    """Get list of available meme templates"""
    templates = []

    for template in TEMPLATES.values():
        templates.append(TemplateInfo(
            id=template.id,
            name=template.name,
            image_url=template.image_url,
            text_count=len(template.text_positions)
        ))

    return templates


@app.post("/api/create", response_model=MemeResponse)
async def create_meme(
    image: UploadFile = File(...),
    top_text: str = Form(""),
    bottom_text: str = Form(""),
    resize: bool = Form(True),
    output_format: str = Form("PNG")
):
    """Create meme from uploaded image

    Args:
        image: Image file upload
        top_text: Text for top of image
        bottom_text: Text for bottom of image
        resize: Whether to resize image (default: True)
        output_format: Output format (PNG or JPEG)

    Returns:
        Meme response with file URL
    """
    try:
        # Read uploaded file
        contents = await image.read()

        # Prepare texts (filter empty strings)
        texts = [t for t in [top_text, bottom_text] if t.strip()]

        if not texts:
            raise HTTPException(
                status_code=400,
                detail="At least one text field is required"
            )

        # Generate meme
        meme_bytes = processor.create_meme(
            image_input=contents,
            texts=texts,
            resize=resize,
            output_format=output_format
        )

        # Save to storage
        file_id, url = storage.save_meme(meme_bytes, image.filename)

        return MemeResponse(
            file_id=file_id,
            url=url,
            message="Meme created successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/create/template/{template_id}", response_model=MemeResponse)
async def create_meme_from_template(
    template_id: str,
    texts: List[str],
    resize: bool = True,
    output_format: str = "PNG"
):
    """Create meme from predefined template

    Args:
        template_id: Template identifier
        texts: List of text strings to overlay
        resize: Whether to resize image
        output_format: Output format (PNG or JPEG)

    Returns:
        Meme response with file URL
    """
    # Validate template
    if template_id not in TEMPLATES:
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_id}' not found"
        )

    template = TEMPLATES[template_id]

    # Validate text count
    if len(texts) != len(template.text_positions):
        raise HTTPException(
            status_code=400,
            detail=f"Template '{template_id}' requires {len(template.text_positions)} texts"
        )

    try:
        # For templates, we need to download the image
        # In production, cache these template images
        import requests
        response = requests.get(template.image_url)
        response.raise_for_status()
        template_image = response.content

        # Generate meme
        meme_bytes = processor.create_meme(
            image_input=template_image,
            texts=texts,
            template_id=template_id,
            resize=resize,
            output_format=output_format
        )

        # Save to storage
        file_id, url = storage.save_meme(meme_bytes, f"{template_id}_meme.png")

        return MemeResponse(
            file_id=file_id,
            url=url,
            message=f"Meme created from template '{template.name}'"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/memes/{file_id}")
async def get_meme(file_id: str):
    """Get meme image by file ID

    Args:
        file_id: File identifier

    Returns:
        Image file
    """
    # Check if using local storage
    if hasattr(storage, 'get_meme'):
        meme_bytes = storage.get_meme(file_id)
        if meme_bytes is None:
            raise HTTPException(status_code=404, detail="Meme not found")

        return Response(content=meme_bytes, media_type="image/png")

    # For cloud storage, redirect to URL
    raise HTTPException(status_code=404, detail="Meme not found")


@app.get("/api/memes")
async def list_memes(limit: int = 50):
    """List recent memes

    Args:
        limit: Maximum number of results (default: 50)

    Returns:
        List of meme info
    """
    if hasattr(storage, 'list_memes'):
        memes = storage.list_memes(limit=limit)
        return {
            "total": len(memes),
            "memes": memes
        }

    return {"total": 0, "memes": []}


@app.delete("/api/memes/{file_id}")
async def delete_meme(file_id: str):
    """Delete meme by file ID

    Args:
        file_id: File identifier

    Returns:
        Success message
    """
    success = storage.delete_meme(file_id)

    if not success:
        raise HTTPException(status_code=404, detail="Meme not found")

    return {"message": "Meme deleted successfully"}


# ============================================================================
# SERVER
# ============================================================================

if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
