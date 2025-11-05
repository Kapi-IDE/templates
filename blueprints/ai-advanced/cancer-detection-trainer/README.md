# 🏥 Breast Cancer Detection - AI System

**Deep Learning Classification: Benign vs Malignant Histopathology Images**

Built with KAPI blueprints - Complete ML pipeline from data to deployment in 30-45 minutes.

---

## 🎯 What It Does

This system detects breast cancer from histopathology images using transfer learning:
- **Input**: Breast tissue microscopy images (50x50 or 96x96 pixels)
- **Output**: Binary classification (Benign or Malignant)
- **Architecture**: MobileNetV2 transfer learning
- **Accuracy**: ~85-90% AUC score (depends on training)

---

## 🚀 Quick Start (30 Minutes)

### Prerequisites
- Python 3.10+
- Kaggle account (free)
- Kaggle API credentials
- 4GB+ RAM (GPU recommended but not required)

### Step 1: Setup Kaggle Credentials

```bash
# Download kaggle.json from https://www.kaggle.com/settings/account
# Place it in ~/.kaggle/kaggle.json

# Or set environment variables:
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements_cancer.txt
```

### Step 3: Train the Model (Run Jupyter Notebook)

```bash
jupyter notebook cancer_detection.ipynb
```

**Execute all cells** - this will:
1. Download breast histopathology dataset from Kaggle (~2GB)
2. Organize images into train/validation directories
3. Apply data augmentation
4. Train MobileNetV2 model (two-phase: freeze → fine-tune)
5. Export model as `cancer_detection_model.h5` (~15MB)
6. Generate performance visualizations

**Training time**: 20-30 minutes (GPU) or 45-60 minutes (CPU)

### Step 4: Run Streamlit App

```bash
streamlit run cancer_app.py
```

Visit **http://localhost:8501** and upload histopathology images for instant predictions!

### Step 5: Run FastAPI Backend (Optional)

```bash
python cancer_api.py
# Or: uvicorn cancer_api:app --reload
```

API available at **http://localhost:8000**

Test with:
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@sample_image.png"
```

---

## 📊 How It Works

### Data Pipeline

```
Kaggle Dataset (277K images)
         ↓
Train/Val Split (80/20)
         ↓
Data Augmentation (rotation, flip, zoom)
         ↓
MobileNetV2 Transfer Learning
         ↓
Two-Phase Training (freeze → fine-tune)
         ↓
Model Export (.h5 file)
         ↓
Streamlit + FastAPI Inference
```

### Architecture

**Base Model**: MobileNetV2 (ImageNet pre-trained)
- Input: 96x96x3 RGB images
- Frozen base for initial training
- Fine-tune last 30 layers

**Classification Head**:
- GlobalAveragePooling2D
- Dropout (0.5)
- Dense(128, relu)
- Dropout (0.3)
- Dense(1, sigmoid) → Binary output

**Training Strategy**:
- **Phase 1**: Train top layers only (15 epochs, lr=1e-3)
- **Phase 2**: Fine-tune base model (10 epochs, lr=1e-5)
- Callbacks: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

### Data Augmentation

- Rotation: ±20°
- Width/Height shift: ±20%
- Horizontal flip: Yes
- Vertical flip: Yes
- Zoom range: ±20%
- Rescaling: 1/255

---

## 🎮 Using the Streamlit App

### Features

1. **Image Upload**: Drag & drop or browse for histopathology images
2. **Instant Prediction**: Get Benign/Malignant classification with confidence
3. **Probability Breakdown**: See exact probabilities for each class
4. **Visual Gauge**: Risk meter visualization
5. **Clinical Context**: Interpretation and recommended next steps
6. **Model Performance**: View confusion matrix, ROC curve, training history

### Interpretation

- **Benign (Green)**: Low malignancy risk - routine monitoring recommended
- **Malignant (Red)**: High malignancy risk - immediate medical consultation required

⚠️ **Always consult healthcare professionals - this is an educational tool only.**

---

## 🔬 FastAPI Backend

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/model/info` | GET | Model metadata |
| `/predict` | POST | Single image prediction |
| `/predict/batch` | POST | Batch predictions |

### Example Usage

**Python**:
```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("sample.png", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.1%}")
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@sample_image.png" \
  | jq
```

---

## 📁 Project Structure

```
cancer-detection/
├── cancer_detection.ipynb     # Training notebook
├── cancer_app.py               # Streamlit inference app
├── cancer_api.py               # FastAPI backend
├── requirements_cancer.txt     # Python dependencies
├── cancer_detection_model.h5   # Trained model (generated)
├── model_info.json            # Model metadata (generated)
├── confusion_matrix.png       # Evaluation (generated)
├── roc_curve.png              # ROC curve (generated)
├── training_history.png       # Training progress (generated)
├── sample_predictions.png     # Test predictions (generated)
└── README.md                  # This file
```

---

## 📊 Dataset Information

**Source**: Kaggle - Breast Histopathology Images
**Link**: https://www.kaggle.com/datasets/paultimothymooney/breast-histopathology-images

**Details**:
- **Size**: ~2GB compressed, 277K+ image patches
- **Image Size**: 50x50 pixels (resized to 96x96)
- **Classes**: Benign (0), Malignant (1)
- **Format**: PNG images
- **License**: CC0 (Public Domain)

**Structure**:
- Patient-level directories
- Class subdirectories (0=Benign, 1=Malignant)
- Original source: IDC (Invasive Ductal Carcinoma) detection

---

## 🔬 Model Performance

### Typical Results

- **Training Accuracy**: ~90-95%
- **Validation Accuracy**: ~85-90%
- **AUC Score**: ~0.85-0.90
- **Inference Time**: ~50-100ms per image

### Evaluation Metrics

- **Confusion Matrix**: True/False positives and negatives
- **ROC Curve**: Sensitivity vs specificity tradeoff
- **Precision/Recall**: Per-class performance
- **F1 Score**: Harmonic mean of precision and recall

### Key Insights

- Transfer learning significantly improves convergence
- Data augmentation critical for generalization
- Two-phase training prevents overfitting
- Medical images benefit from domain-specific preprocessing

---

## 🛠️ Customization

### Change Input Size

In notebook:
```python
IMG_SIZE = 128  # Change from 96 to 128
```

In app and API:
```python
target_size=(128, 128)  # Update preprocessing
```

### Add More Data Augmentation

```python
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,        # Increase rotation
    brightness_range=[0.8, 1.2],  # Add brightness
    shear_range=0.2,          # Add shear
    # ... other augmentations
)
```

### Use Different Base Model

```python
from tensorflow.keras.applications import EfficientNetB0

base_model = EfficientNetB0(
    input_shape=(96, 96, 3),
    include_top=False,
    weights='imagenet'
)
```

### Adjust Training Parameters

```python
# More epochs
history = model.fit(..., epochs=25)

# Different learning rate
optimizer=keras.optimizers.Adam(learning_rate=5e-4)
```

---

## 🚀 Deployment Options

### Option 1: Local Streamlit

```bash
streamlit run cancer_app.py
```

### Option 2: Streamlit Cloud (Free)

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy (https://streamlit.io/cloud)

### Option 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements_cancer.txt .
RUN pip install -r requirements_cancer.txt

COPY cancer_app.py cancer_detection_model.h5 model_info.json ./
CMD ["streamlit", "run", "cancer_app.py", "--server.port=8501"]
```

```bash
docker build -t cancer-detection .
docker run -p 8501:8501 cancer-detection
```

### Option 4: FastAPI + Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements_cancer.txt .
RUN pip install -r requirements_cancer.txt

COPY cancer_api.py cancer_detection_model.h5 model_info.json ./
CMD ["uvicorn", "cancer_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option 5: Hugging Face Spaces

- Upload to HF Spaces
- Auto-deploys Streamlit apps
- Free hosting

---

## 🐛 Troubleshooting

### Issue: Kaggle credentials not found

**Solution**:
```bash
mkdir -p ~/.kaggle
mv kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### Issue: Model file not found

**Solution**: Run Jupyter notebook first to train and save model:
```bash
jupyter notebook cancer_detection.ipynb
# Execute all cells
```

### Issue: Out of memory during training

**Solutions**:
- Reduce batch size: `BATCH_SIZE = 16`
- Reduce image size: `IMG_SIZE = 64`
- Use mixed precision: `tf.keras.mixed_precision.set_global_policy('mixed_float16')`

### Issue: TensorFlow/GPU errors

**Solution**: Install GPU-specific TensorFlow:
```bash
pip install tensorflow[and-cuda]  # For NVIDIA GPUs
```

### Issue: Slow inference

**Solutions**:
- Use TensorFlow Lite for mobile/edge
- Quantize model: `converter = tf.lite.TFLiteConverter.from_keras_model(model)`
- Batch predictions instead of single images

---

## 📚 Learning Resources

**Medical Imaging AI**:
- [Stanford ML for Healthcare](https://ml4health.stanford.edu/)
- [Medical Image Analysis Papers](https://www.sciencedirect.com/journal/medical-image-analysis)

**Transfer Learning**:
- [TensorFlow Transfer Learning Guide](https://www.tensorflow.org/tutorials/images/transfer_learning)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)

**Streamlit**:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

**FastAPI**:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ML Model Deployment with FastAPI](https://fastapi.tiangolo.com/deployment/)

---

## 🎓 Educational Value

This project demonstrates:

### 1. **Complete Deep Learning Pipeline**
- Data acquisition (Kaggle API)
- Data preprocessing and organization
- Transfer learning implementation
- Model training and evaluation
- Model deployment (Streamlit + FastAPI)

### 2. **Medical AI Best Practices**
- Data augmentation for medical images
- Two-phase training strategy
- Proper validation split
- Clinical interpretation guidelines
- Ethical disclaimers

### 3. **Production Patterns**
- Model versioning and metadata
- REST API design
- Interactive web UI
- Batch processing
- Error handling
- Logging and monitoring

---

## 🔮 Future Enhancements

**Model Improvements**:
- [ ] Multi-class classification (tumor grades)
- [ ] Attention mechanisms for interpretability
- [ ] Ensemble models for higher accuracy
- [ ] Grad-CAM visualization (show what model sees)

**App Enhancements**:
- [ ] Upload multiple images at once
- [ ] Patient history tracking
- [ ] Report generation (PDF export)
- [ ] Comparison with radiologist annotations
- [ ] Confidence thresholds (adjustable)

**Deployment**:
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Model monitoring and drift detection
- [ ] A/B testing framework
- [ ] Mobile app (React Native + TF Lite)

---

## ⚠️ Medical Disclaimer

**THIS MODEL IS FOR EDUCATIONAL PURPOSES ONLY.**

- **NOT FDA approved**: This is a research/educational tool
- **NOT for clinical diagnosis**: Always consult qualified medical professionals
- **Limited validation**: Trained on specific dataset, may not generalize
- **Requires oversight**: Medical AI must be used under expert supervision
- **Liability**: Authors assume no responsibility for medical decisions based on this tool

**Proper Clinical Use Would Require**:
- Extensive validation on diverse datasets
- Clinical trials and FDA approval
- Integration with hospital IT systems
- Pathologist oversight and verification
- Continuous monitoring and updates

---

## 📄 License

MIT - Free for personal and educational use

---

## 🙏 Acknowledgments

- **Dataset**: Kaggle Breast Histopathology Images
- **Framework**: TensorFlow/Keras
- **UI**: Streamlit
- **API**: FastAPI
- **Base Model**: MobileNetV2 (Google Research)
- **Built with**: KAPI Production ML Blueprints

---

**Built with KAPI** - From idea to production in 30-45 minutes

**Questions?** Check the notebook for detailed explanations and code comments.
