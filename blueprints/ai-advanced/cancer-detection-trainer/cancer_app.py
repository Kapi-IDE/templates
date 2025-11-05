"""
Breast Cancer Detection - Streamlit Inference App

Upload histopathology images and get instant predictions (Benign vs Malignant).
Built with KAPI Streamlit Components.
"""

import streamlit as st
import numpy as np
import json
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Cancer Detection AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for medical theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2C5F2D;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #97BC62;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .benign-prediction {
        background-color: #4CAF50;
        color: white;
    }
    .malignant-prediction {
        background-color: #F44336;
        color: white;
    }
    .stButton>button {
        width: 100%;
        background-color: #2C5F2D;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #97BC62;
    }
    .disclaimer {
        background-color: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    """Load trained cancer detection model"""
    model_path = Path('cancer_detection_model.h5')
    info_path = Path('model_info.json')

    if not model_path.exists():
        st.error(f"❌ Model file not found: {model_path}")
        st.info("Please run the Jupyter notebook first to train and save the model.")
        return None, None

    try:
        model = keras.models.load_model(model_path)

        if info_path.exists():
            with open(info_path, 'r') as f:
                model_info = json.load(f)
        else:
            model_info = {
                'model_name': 'MobileNetV2 Transfer Learning',
                'input_shape': [96, 96, 3],
                'classes': ['Benign', 'Malignant']
            }

        return model, model_info
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None

def preprocess_image(image, target_size=(96, 96)):
    """Preprocess uploaded image for model inference"""
    # Resize image
    image = image.resize(target_size)

    # Convert to array
    img_array = np.array(image)

    # Ensure RGB (in case of RGBA or grayscale)
    if len(img_array.shape) == 2:  # Grayscale
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[-1] == 4:  # RGBA
        img_array = img_array[:, :, :3]

    # Normalize to [0, 1]
    img_array = img_array.astype('float32') / 255.0

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Breast Cancer Detection AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Histopathology Image Classification using Deep Learning</p>', unsafe_allow_html=True)

    # Load model
    model, model_info = load_model()

    if model is None:
        st.stop()

    # Sidebar - Model info and controls
    st.sidebar.header("📊 Model Information")
    st.sidebar.success(f"""
    **Model**: {model_info.get('model_name', 'N/A')}

    **Architecture**: Transfer Learning

    **Input Size**: {model_info.get('input_shape', [96, 96, 3])[0]}x{model_info.get('input_shape', [96, 96, 3])[1]}

    **Classes**: {', '.join(model_info.get('classes', ['Benign', 'Malignant']))}

    **AUC Score**: {model_info.get('auc_score', 'N/A'):.3f if isinstance(model_info.get('auc_score'), (int, float)) else 'N/A'}
    """)

    st.sidebar.markdown("---")
    st.sidebar.header("📤 Upload Image")

    # File uploader
    uploaded_file = st.sidebar.file_uploader(
        "Choose a histopathology image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a breast histopathology image (50x50 or similar)"
    )

    # Medical disclaimer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div class="disclaimer">
    <strong>⚠️ Medical Disclaimer</strong><br>
    This tool is for educational purposes only.
    Do NOT use for actual medical diagnosis.
    Always consult qualified healthcare professionals.
    </div>
    """, unsafe_allow_html=True)

    # Main content area
    tab1, tab2, tab3 = st.tabs(["🔬 Prediction", "📈 Model Performance", "ℹ️ About"])

    with tab1:
        if uploaded_file is not None:
            # Display uploaded image
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📸 Uploaded Image")
                image = Image.open(uploaded_file)
                st.image(image, caption="Original Image", use_container_width=True)

                # Image info
                st.info(f"""
                **Image Details:**
                - Size: {image.size[0]}x{image.size[1]} pixels
                - Mode: {image.mode}
                - Format: {image.format}
                """)

            with col2:
                st.subheader("🎯 Prediction Result")

                # Preprocess and predict
                with st.spinner("Analyzing image..."):
                    processed_img = preprocess_image(image, target_size=(96, 96))
                    prediction_proba = model.predict(processed_img, verbose=0)[0][0]

                    # Determine prediction
                    is_malignant = prediction_proba > 0.5
                    prediction_label = "Malignant" if is_malignant else "Benign"
                    confidence = prediction_proba if is_malignant else 1 - prediction_proba

                    # Display prediction
                    pred_class = "malignant-prediction" if is_malignant else "benign-prediction"
                    st.markdown(f"""
                    <div class="prediction-box {pred_class}">
                        <h2>{'⚠️ MALIGNANT' if is_malignant else '✅ BENIGN'}</h2>
                        <p style="font-size: 2rem; margin: 0;">
                            {confidence*100:.1f}%
                        </p>
                        <p style="font-size: 1rem; opacity: 0.9;">Confidence</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Probability breakdown
                    st.markdown("**Probability Breakdown:**")

                    benign_prob = (1 - prediction_proba) * 100
                    malignant_prob = prediction_proba * 100

                    st.markdown(f"**Benign**: {benign_prob:.1f}%")
                    st.progress(benign_prob / 100)

                    st.markdown(f"**Malignant**: {malignant_prob:.1f}%")
                    st.progress(malignant_prob / 100)

                    # Gauge chart
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=malignant_prob,
                        title={'text': "Malignancy Risk"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkred" if is_malignant else "darkgreen"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgreen"},
                                {'range': [50, 100], 'color': "lightcoral"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 50
                            }
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

            # Medical interpretation
            st.markdown("---")
            st.subheader("💡 Clinical Context")

            if is_malignant:
                st.warning(f"""
                **High Malignancy Risk Detected ({confidence*100:.1f}% confidence)**

                The model indicates characteristics consistent with malignant tissue. This finding should be:
                - Reviewed by a pathologist
                - Correlated with clinical presentation
                - Confirmed with additional diagnostic tests
                - Discussed with the patient's oncology team

                **Next Steps**: Immediate consultation with medical professionals for comprehensive evaluation.
                """)
            else:
                st.success(f"""
                **Low Malignancy Risk ({confidence*100:.1f}% confidence)**

                The model indicates characteristics more consistent with benign tissue. However:
                - Pathological review is still recommended
                - Clinical correlation is essential
                - Follow-up may be necessary based on other factors
                - Not all benign findings rule out cancer

                **Next Steps**: Continue routine monitoring as recommended by healthcare provider.
                """)

        else:
            st.info("👈 Please upload a histopathology image using the sidebar to get started.")

            # Example images section
            st.markdown("---")
            st.subheader("📚 Example Use Case")
            st.markdown("""
            This AI model analyzes **breast histopathology images** to classify tissue as:
            - **Benign** (Non-cancerous)
            - **Malignant** (Cancerous)

            **How it works:**
            1. Upload a histopathology image (ideally 50x50 pixels or similar)
            2. The model processes the image using MobileNetV2 architecture
            3. Get instant prediction with confidence scores
            4. Review clinical interpretation and recommendations

            **Training Data**: 277K+ image patches from Kaggle's Breast Histopathology Images dataset
            """)

    with tab2:
        st.subheader("📊 Model Performance Metrics")

        # Check if performance images exist
        perf_images = {
            'Confusion Matrix': 'confusion_matrix.png',
            'ROC Curve': 'roc_curve.png',
            'Training History': 'training_history.png',
            'Sample Predictions': 'sample_predictions.png'
        }

        available_images = {k: v for k, v in perf_images.items() if Path(v).exists()}

        if available_images:
            selected_metric = st.selectbox("Select Metric to View", list(available_images.keys()))

            st.image(available_images[selected_metric], caption=selected_metric, use_container_width=True)
        else:
            st.info("Performance metrics will be available after training the model in the Jupyter notebook.")

        # Model statistics
        st.markdown("---")
        st.subheader("📈 Model Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Model Architecture", model_info.get('model_name', 'N/A'))
        with col2:
            auc_score = model_info.get('auc_score', 0)
            st.metric("AUC Score", f"{auc_score:.3f}" if isinstance(auc_score, (int, float)) else "N/A")
        with col3:
            total_params = model_info.get('total_params', 0)
            st.metric("Total Parameters", f"{total_params:,}" if total_params else "N/A")

    with tab3:
        st.subheader("ℹ️ About This Application")

        st.markdown("""
        ## 🏥 Breast Cancer Detection AI

        This application uses **deep learning** to classify breast histopathology images as benign or malignant.

        ### 🔬 Technical Details

        **Model Architecture:**
        - Base: MobileNetV2 (pre-trained on ImageNet)
        - Training: Two-phase transfer learning
        - Input: 96x96 RGB images
        - Output: Binary classification (Benign/Malignant)

        **Training Process:**
        - **Phase 1**: Train top layers with frozen base model
        - **Phase 2**: Fine-tune last 30 layers of base model
        - Data augmentation: Rotation, flips, shifts, zoom
        - Callbacks: Early stopping, learning rate reduction

        **Dataset:**
        - Source: Kaggle Breast Histopathology Images
        - Size: 277K+ image patches
        - Original size: 50x50 pixels
        - Classes: Benign (0), Malignant (1)

        ### 🎯 Use Cases

        - **Educational**: Learn about AI in medical imaging
        - **Research**: Prototype for histopathology analysis
        - **Demonstration**: Showcase transfer learning capabilities

        ### ⚠️ Important Limitations

        - **Not for clinical use**: This is an educational tool
        - **No medical advice**: Always consult healthcare professionals
        - **Limited scope**: Trained on specific dataset, may not generalize
        - **Requires validation**: Medical AI must be rigorously validated

        ### 🛠️ Built With

        - **ML Framework**: TensorFlow/Keras
        - **UI Framework**: Streamlit (KAPI Components)
        - **Visualization**: Plotly
        - **Dataset**: Kaggle Breast Histopathology Images

        ---

        **Built with KAPI** - Production-ready ML blueprints
        """)

if __name__ == "__main__":
    main()
