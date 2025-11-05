"""
NFL Play Prediction - Streamlit Inference App

Predicts whether the next play will be a RUN or PASS based on game situation.
Built with KAPI Streamlit Components.
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="NFL Play Predictor",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for NFL theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #013369;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #D50A0A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .run-prediction {
        background-color: #4CAF50;
        color: white;
    }
    .pass-prediction {
        background-color: #2196F3;
        color: white;
    }
    .confidence-bar {
        height: 30px;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #013369;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #D50A0A;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    """Load the trained NFL play prediction model"""
    model_path = Path('nfl_play_predictor.pkl')

    if not model_path.exists():
        st.error(f"❌ Model file not found: {model_path}")
        st.info("Please run the Jupyter notebook first to train and save the model.")
        return None

    try:
        with open(model_path, 'rb') as f:
            model_package = pickle.load(f)
        return model_package
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

# Helper function to engineer features
def engineer_features(data):
    """Add engineered features to match training data"""
    data['is_red_zone'] = int(data['yardline_100'] <= 20)
    data['is_goal_to_go'] = int(data['ydstogo'] >= data['yardline_100'])
    data['is_short_yardage'] = int(data['ydstogo'] <= 3)
    data['is_long_yardage'] = int(data['ydstogo'] >= 10)
    data['is_4th_quarter'] = int(data['qtr'] == 4)
    data['is_close_game'] = int(abs(data['ScoreDiff']) <= 7)
    data['is_winning'] = int(data['ScoreDiff'] > 0)
    data['is_losing'] = int(data['ScoreDiff'] < 0)
    return data

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🏈 NFL Play Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Predict RUN or PASS using Machine Learning</p>', unsafe_allow_html=True)

    # Load model
    model_package = load_model()

    if model_package is None:
        st.stop()

    # Display model info
    st.sidebar.success(f"""
    **Model Loaded Successfully!**

    - **Model**: {model_package['model_name']}
    - **Accuracy**: {model_package['accuracy']*100:.2f}%
    - **Features**: {len(model_package['features'])}
    """)

    # Sidebar - Input controls
    st.sidebar.header("⚙️ Game Situation")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        down = st.selectbox("Down", [1, 2, 3, 4], index=0)
        qtr = st.selectbox("Quarter", [1, 2, 3, 4], index=1)

    with col2:
        ydstogo = st.number_input("Yards to Go", min_value=1, max_value=30, value=10)
        yardline_100 = st.slider("Field Position (yds from opp endzone)", 1, 99, 75)

    st.sidebar.markdown("---")
    st.sidebar.subheader("⏱️ Time & Score")

    time_mins = st.sidebar.slider("Time Remaining (minutes)", 0, 15, 10)
    time_secs = time_mins * 60

    col3, col4 = st.sidebar.columns(2)
    with col3:
        pos_score = st.number_input("Your Score", min_value=0, max_value=99, value=17)
    with col4:
        def_score = st.number_input("Opponent Score", min_value=0, max_value=99, value=14)

    score_diff = pos_score - def_score

    # Predict button
    predict_button = st.sidebar.button("🔮 PREDICT PLAY", type="primary")

    # Main content area
    tab1, tab2, tab3 = st.tabs(["📊 Prediction", "📈 Analysis", "ℹ️ About"])

    with tab1:
        # Create feature dictionary
        features = {
            'down': down,
            'ydstogo': ydstogo,
            'yardline_100': yardline_100,
            'qtr': qtr,
            'TimeSecs': time_secs,
            'ScoreDiff': score_diff,
            'PosTeamScore': pos_score,
            'DefTeamScore': def_score,
        }

        # Engineer additional features
        features = engineer_features(features)

        # Display game situation
        st.subheader("🏟️ Game Situation")

        situation_col1, situation_col2, situation_col3 = st.columns(3)

        with situation_col1:
            st.metric("Down & Distance", f"{down} & {ydstogo}")
            st.metric("Field Position", f"Own {100-yardline_100} yd line")

        with situation_col2:
            st.metric("Score", f"{pos_score} - {def_score}")
            score_status = "Winning" if score_diff > 0 else ("Tied" if score_diff == 0 else "Losing")
            st.metric("Status", f"{score_status} by {abs(score_diff)}")

        with situation_col3:
            st.metric("Quarter", qtr)
            st.metric("Time Remaining", f"{time_mins}:00")

        st.markdown("---")

        # Make prediction
        if predict_button or 'first_load' not in st.session_state:
            st.session_state.first_load = True

            # Prepare data
            input_df = pd.DataFrame([features])[model_package['features']]

            # Make prediction
            prediction = model_package['model'].predict(input_df)[0]
            probabilities = model_package['model'].predict_proba(input_df)[0]

            run_prob = probabilities[0] * 100
            pass_prob = probabilities[1] * 100

            # Display prediction
            st.subheader("🎯 Prediction Result")

            pred_col1, pred_col2 = st.columns(2)

            with pred_col1:
                st.markdown(f"""
                <div class="prediction-box {'run-prediction' if prediction == 0 else 'pass-prediction'}">
                    <h2>{'🏃 RUN' if prediction == 0 else '🎯 PASS'}</h2>
                    <p style="font-size: 2rem; margin: 0;">
                        {run_prob if prediction == 0 else pass_prob:.1f}%
                    </p>
                    <p style="font-size: 1rem; opacity: 0.9;">Confidence</p>
                </div>
                """, unsafe_allow_html=True)

            with pred_col2:
                st.markdown("**Probability Breakdown:**")

                st.markdown(f"**RUN**: {run_prob:.1f}%")
                st.progress(run_prob / 100)

                st.markdown(f"**PASS**: {pass_prob:.1f}%")
                st.progress(pass_prob / 100)

            # Contextual insights
            st.markdown("---")
            st.subheader("💡 Contextual Insights")

            insights = []

            if features['is_long_yardage']:
                insights.append("📏 **Long yardage** situation - Pass more likely")
            if features['is_short_yardage']:
                insights.append("📏 **Short yardage** - Run more likely")
            if features['is_red_zone']:
                insights.append("🔴 **Red Zone** - Play calling less predictable")
            if features['is_4th_quarter'] and abs(score_diff) <= 7:
                insights.append("⏰ **Close game, 4th quarter** - Critical situation!")
            if features['is_losing'] and qtr >= 3:
                insights.append("📉 **Losing late** - More passing to catch up")
            if features['is_winning'] and qtr == 4:
                insights.append("📈 **Winning in 4th** - May run to use clock")
            if down == 3 and ydstogo > 7:
                insights.append("🎯 **3rd and long** - Obvious passing down")

            if insights:
                for insight in insights:
                    st.info(insight)
            else:
                st.info("⚡ **Neutral situation** - Play calling could go either way")

    with tab2:
        st.subheader("📈 Feature Importance")

        if model_package['feature_importance']:
            import plotly.express as px

            importance_df = pd.DataFrame(model_package['feature_importance']).head(10)

            fig = px.bar(
                importance_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title='Top 10 Most Important Features',
                color='Importance',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Feature importance not available for this model type.")

        st.markdown("---")
        st.subheader("📊 Model Performance")

        perf_col1, perf_col2, perf_col3 = st.columns(3)

        with perf_col1:
            st.metric("Model Type", model_package['model_name'])
        with perf_col2:
            st.metric("Test Accuracy", f"{model_package['accuracy']*100:.2f}%")
        with perf_col3:
            st.metric("Features Used", len(model_package['features']))

    with tab3:
        st.subheader("About This App")

        st.markdown("""
        ## 🏈 NFL Play Predictor

        This app uses machine learning to predict whether an NFL team will call a **RUN** or **PASS** play
        based on the current game situation.

        ### 📊 How It Works

        1. **Training Data**: NFL play-by-play data from 2009-2018 (400,000+ plays)
        2. **Features**: Down, distance, field position, score, time, and engineered features
        3. **Models**: Logistic Regression, Random Forest, XGBoost
        4. **Best Model**: Automatically selected based on test accuracy (~70-73%)

        ### 🎯 Key Insights

        - **3rd & Long** → High pass probability (70-80%)
        - **Short Yardage** → Higher run probability (60-70%)
        - **Losing + 4th Quarter** → Pass more often
        - **Winning + 4th Quarter** → Run to use clock
        - **Red Zone** → More balanced play calling

        ### 🔬 Model Features

        **Base Features:**
        - Down (1-4)
        - Yards to go
        - Field position
        - Quarter
        - Time remaining
        - Score differential

        **Engineered Features:**
        - Red zone indicator
        - Goal-to-go indicator
        - Short/long yardage indicators
        - 4th quarter indicator
        - Close game indicator
        - Winning/losing indicators

        ### 🛠️ Built With

        - **ML Framework**: Scikit-learn, XGBoost
        - **UI Framework**: Streamlit (KAPI Components)
        - **Data**: Kaggle NFL Play-by-Play Dataset
        - **Visualization**: Plotly

        ### 📝 Notes

        - Predictions are based on historical data patterns
        - Actual play calling depends on many factors not captured (personnel, tendencies, etc.)
        - Use for entertainment and analysis purposes

        ---

        **Built with KAPI** - Production-ready ML blueprints
        """)

if __name__ == "__main__":
    main()
