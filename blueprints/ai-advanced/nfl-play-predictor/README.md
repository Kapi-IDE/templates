# 🏈 NFL Play Predictor - ML System

**Predict whether the next play will be RUN or PASS using Machine Learning**

Built with KAPI blueprints - Complete ML pipeline from data to deployment in minutes.

---

## 🎯 What It Does

This system predicts NFL play calling (RUN vs PASS) based on game situation:
- **Down & Distance**: 3rd & 10 → likely PASS
- **Field Position**: Red zone behavior
- **Game Clock**: 4th quarter urgency
- **Score**: Losing teams pass more, winning teams run more

**Accuracy**: ~70-73% on test data (better than random guessing!)

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Kaggle account (free)
- Kaggle API credentials

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
pip install -r requirements.txt
```

### Step 3: Train the Model (Run Jupyter Notebook)

```bash
jupyter notebook nfl_play_prediction.ipynb
```

**Execute all cells** - this will:
1. Download NFL play-by-play data from Kaggle (~450KB)
2. Clean and engineer features (16 features total)
3. Train 3 models: Logistic Regression, Random Forest, XGBoost
4. Export best model as `nfl_play_predictor.pkl` (~5MB)

**Training time**: ~2-5 minutes

### Step 4: Run Streamlit App

```bash
streamlit run nfl_app.py
```

Visit **http://localhost:8501** and start predicting plays!

---

## 📊 How It Works

### Data Pipeline

```
Kaggle Dataset (400K+ plays)
         ↓
Feature Engineering (16 features)
         ↓
Train/Test Split (80/20)
         ↓
Model Training (3 models)
         ↓
Best Model Selection
         ↓
Pickle Export
         ↓
Streamlit Inference App
```

### Features Used

**Base Features** (8):
- Down (1-4)
- Yards to go
- Field position (yards from opponent endzone)
- Quarter (1-4)
- Time remaining (seconds)
- Score differential
- Possession team score
- Defense team score

**Engineered Features** (8):
- Is red zone (≤20 yards)
- Is goal-to-go
- Is short yardage (≤3 yards)
- Is long yardage (≥10 yards)
- Is 4th quarter
- Is close game (within 7 points)
- Is winning
- Is losing

### Models Trained

| Model | Typical Accuracy | Speed | Best For |
|-------|-----------------|-------|----------|
| **Logistic Regression** | ~68% | Fast | Baseline |
| **Random Forest** | ~72% | Medium | Feature importance |
| **XGBoost** | ~73% | Medium | Best performance |

**Best model is automatically selected** based on test accuracy.

---

## 🎮 Using the Streamlit App

### Input Controls

**Game Situation:**
- Down (1-4)
- Yards to go (1-30)
- Field position (slider)
- Quarter (1-4)
- Time remaining (0-15 minutes)
- Score (your team vs opponent)

### Output

**Prediction:**
- RUN or PASS
- Confidence % for each
- Probability breakdown

**Insights:**
- Contextual analysis (e.g., "3rd and long - Pass more likely")
- Situation-specific recommendations
- Historical patterns

**Analysis Tab:**
- Feature importance visualization
- Model performance metrics

---

## 📁 Project Structure

```
nfl-play-predictor/
├── nfl_play_prediction.ipynb    # Training notebook
├── nfl_app.py                    # Streamlit inference app
├── requirements.txt              # Python dependencies
├── nfl_play_predictor.pkl       # Trained model (generated)
├── NFL Play by Play 2009-2017.csv  # Data (downloaded from Kaggle)
└── README.md                     # This file
```

---

## 🔬 Model Performance

### Typical Results

- **Training Accuracy**: ~75%
- **Test Accuracy**: ~70-73%
- **Baseline (Random)**: 50%
- **Baseline (Always Pass)**: ~55% (since NFL is pass-heavy)

### Key Insights from Data

**Pass Rate by Down:**
- 1st down: ~50% pass
- 2nd down: ~55% pass
- 3rd down: ~65% pass (depends on distance)
- 4th down: Varies widely

**Pass Rate by Situation:**
- **3rd & 10+**: 75-80% pass
- **3rd & 1-3**: 40-50% pass
- **Red Zone (1st down)**: ~48% pass
- **Losing by 14+ in 4th**: 70-80% pass
- **Winning by 14+ in 4th**: 35-45% pass

---

## 🎯 Example Predictions

### Scenario 1: Obvious Passing Situation
```
Input:
- 3rd & 12
- Own 25-yard line
- Down by 7
- 4th Quarter, 5 minutes left

Prediction: PASS (85% confidence)
Reason: Long yardage + losing + late game
```

### Scenario 2: Run-Heavy Situation
```
Input:
- 2nd & 2
- Opponent 8-yard line (Red Zone)
- Up by 3
- 4th Quarter, 2 minutes left

Prediction: RUN (70% confidence)
Reason: Short yardage + red zone + winning + clock management
```

### Scenario 3: Neutral Situation
```
Input:
- 1st & 10
- Own 45-yard line
- Tied game
- 2nd Quarter

Prediction: PASS (55% confidence)
Reason: Neutral situation, slight pass tendency in modern NFL
```

---

## 🛠️ Customization

### Train with Different Data

Edit the notebook to use different seasons:
```python
# Change this line:
df = pd.read_csv('NFL Play by Play 2009-2017 (v4).csv')

# To filter specific years:
df = df[df['Season'].isin([2015, 2016, 2017])]
```

### Add More Features

Add custom features in the notebook:
```python
# Example: Home field advantage
df_clean['is_home'] = (df_clean['posteam'] == df_clean['HomeTeam']).astype(int)

# Update features list:
features_extended.append('is_home')
```

### Adjust Streamlit UI

Modify `nfl_app.py`:
- Change color scheme in custom CSS
- Add team logos
- Include play history
- Add prediction confidence thresholds

---

## 📊 Dataset Information

**Source**: Kaggle - NFL Play by Play Data (2009-2018)
**Link**: https://www.kaggle.com/datasets/maxhorowitz/nflplaybyplay2009to2016

**Size**: ~450KB compressed, ~50MB uncompressed
**Rows**: 407,688 plays
**Columns**: 255 features
**Years**: 2009-2017 seasons
**License**: CC0 (Public Domain)

**Key Columns Used**:
- `PlayType`: Run, Pass, Punt, Kickoff, etc.
- `down`: 1-4
- `ydstogo`: Yards to first down
- `yardline_100`: Distance from opponent endzone
- `qtr`: Quarter
- `TimeSecs`: Time remaining
- `ScoreDiff`: Score differential
- Plus many more...

---

## 🧪 Testing

### Test Predictions in Notebook

The notebook includes test scenarios:
```python
# Scenario: 3rd & 12, losing, 4th quarter
test_scenario = {
    'down': 3,
    'ydstogo': 12,
    'ScoreDiff': -7,
    'qtr': 4,
    # ...
}

prediction = model.predict([test_scenario])
```

### Validate Model

```bash
# Re-run notebook cells to see:
# - Confusion matrix
# - Classification report
# - ROC curve
# - Feature importance
```

---

## 🚀 Deployment Options

### Option 1: Local Streamlit

```bash
streamlit run nfl_app.py
```

### Option 2: Streamlit Cloud (Free)

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy (https://streamlit.io/cloud)

### Option 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY nfl_app.py nfl_play_predictor.pkl ./
CMD ["streamlit", "run", "nfl_app.py", "--server.port=8501"]
```

### Option 4: Hugging Face Spaces

- Upload to HF Spaces
- Auto-deploys Streamlit apps
- Free hosting

---

## 🐛 Troubleshooting

### Issue: Kaggle credentials not found

**Solution**:
```bash
# Download kaggle.json from https://www.kaggle.com/settings/account
mkdir -p ~/.kaggle
mv kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### Issue: Model file not found

**Solution**: Run the Jupyter notebook first to train and save the model:
```bash
jupyter notebook nfl_play_prediction.ipynb
# Execute all cells
```

### Issue: Import errors

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Streamlit app won't start

**Solution**: Check if model file exists:
```bash
ls -lh nfl_play_predictor.pkl
# Should show ~5MB file

# If missing, retrain in notebook
```

---

## 📚 Learning Resources

**Machine Learning**:
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

**NFL Analytics**:
- [NFL Analytics Resources](https://www.advancedfootballanalytics.com/)
- [Expected Points Added (EPA)](https://www.nflfastr.com/)

**Streamlit**:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

---

## 🎓 Educational Value

This project demonstrates:

### 1. **Complete ML Pipeline**
- Data acquisition (Kaggle API)
- Data cleaning and EDA
- Feature engineering
- Model training and evaluation
- Model persistence (pickle)
- Inference app deployment

### 2. **Real-World ML Concepts**
- Binary classification
- Feature importance
- Model comparison
- Train/test split
- Cross-validation (optional)

### 3. **Production Patterns**
- Model versioning
- Inference optimization
- UI/UX for ML apps
- Error handling
- Model monitoring (can be added)

---

## 🔮 Future Enhancements

**Model Improvements**:
- [ ] Add team-specific features (offensive/defensive rankings)
- [ ] Include weather data
- [ ] Add player personnel (11 vs 12 personnel)
- [ ] Time-series features (recent play history)
- [ ] Deep learning (LSTM for play sequences)

**App Enhancements**:
- [ ] Team logos and colors
- [ ] Play-by-play history visualization
- [ ] Confidence intervals
- [ ] Export predictions to CSV
- [ ] Compare multiple scenarios side-by-side

**Deployment**:
- [ ] REST API endpoint
- [ ] Mobile app
- [ ] Real-time game integration
- [ ] Multi-user support

---

## 📄 License

MIT - Free for personal and educational use

---

## 🙏 Acknowledgments

- **Dataset**: Kaggle NFL Play-by-Play Data
- **ML Libraries**: Scikit-learn, XGBoost
- **UI Framework**: Streamlit
- **Built with**: KAPI Production ML Blueprints

---

**Built with KAPI** - From idea to production in minutes

**Questions?** Check the notebook for detailed explanations and code comments.
