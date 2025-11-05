"""
Breast Cancer Detection - FastAPI Backend

REST API for breast cancer detection model inference.
Built with KAPI FastAPI Components.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cancer Detection API",
    description="AI-powered breast cancer detection from histopathology images",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variables
model = None
model_info = None

# Response models
class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict
    model_info: dict

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: Optional[str]

# Load model on startup
@app.on_event("startup")
async def load_model():
    """Load the trained model on server startup"""
    global model, model_info

    model_path = Path('cancer_detection_model.h5')
    info_path = Path('model_info.json')

    try:
        if model_path.exists():
            logger.info(f"Loading model from {model_path}")
            model = keras.models.load_model(model_path)
            logger.info("Model loaded successfully")

            if info_path.exists():
                with open(info_path, 'r') as f:
                    model_info = json.load(f)
            else:
                model_info = {
                    'model_name': 'MobileNetV2 Transfer Learning',
                    'input_shape': [96, 96, 3],
                    'classes': ['Benign', 'Malignant']
                }
        else:
            logger.warning(f"Model file not found at {model_path}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")

def preprocess_image(image: Image.Image, target_size=(96, 96)) -> np.ndarray:
    """Preprocess image for model inference"""
    # Resize
    image = image.resize(target_size)

    # Convert to array
    img_array = np.array(image)

    # Ensure RGB
    if len(img_array.shape) == 2:  # Grayscale
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[-1] == 4:  # RGBA
        img_array = img_array[:, :, :3]

    # Normalize
    img_array = img_array.astype('float32') / 255.0

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Cancer Detection API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "model_info": "/model/info"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_name": model_info.get('model_name', None) if model_info else None
    }

@app.get("/model/info", response_model=dict)
async def get_model_info():
    """Get model information"""
    if model_info is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return model_info

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Predict cancer type from uploaded histopathology image

    Args:
        file: Image file (PNG, JPG, JPEG)

    Returns:
        Prediction with confidence scores
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Preprocess
        processed_img = preprocess_image(image, target_size=(96, 96))

        # Predict
        prediction_proba = model.predict(processed_img, verbose=0)[0][0]

        # Determine prediction
        is_malignant = prediction_proba > 0.5
        prediction_label = "Malignant" if is_malignant else "Benign"
        confidence = float(prediction_proba if is_malignant else 1 - prediction_proba)

        # Build response
        response = {
            "prediction": prediction_label,
            "confidence": confidence,
            "probabilities": {
                "Benign": float(1 - prediction_proba),
                "Malignant": float(prediction_proba)
            },
            "model_info": {
                "model_name": model_info.get('model_name', 'Unknown'),
                "auc_score": model_info.get('auc_score', None)
            }
        }

        logger.info(f"Prediction: {prediction_label} ({confidence:.2%} confidence)")

        return response

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch", response_model=list)
async def predict_batch(files: list[UploadFile] = File(...)):
    """
    Predict cancer type for multiple images

    Args:
        files: List of image files

    Returns:
        List of predictions
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    results = []

    for file in files:
        try:
            # Read and preprocess
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            processed_img = preprocess_image(image, target_size=(96, 96))

            # Predict
            prediction_proba = model.predict(processed_img, verbose=0)[0][0]
            is_malignant = prediction_proba > 0.5
            prediction_label = "Malignant" if is_malignant else "Benign"
            confidence = float(prediction_proba if is_malignant else 1 - prediction_proba)

            results.append({
                "filename": file.filename,
                "prediction": prediction_label,
                "confidence": confidence,
                "probabilities": {
                    "Benign": float(1 - prediction_proba),
                    "Malignant": float(prediction_proba)
                }
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
