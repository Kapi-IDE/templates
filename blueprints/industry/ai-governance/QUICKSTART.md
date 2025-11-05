# 🚀 Quick Start Guide - AI Governance Platform

Get the AI Governance platform running in under 5 minutes.

## Prerequisites

- Python 3.10+
- Node.js 18+
- pip or uv

## Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Install dependencies
pip install -e .
# OR with uv
uv pip install -e .

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running on: **http://localhost:8000**
✅ API docs: **http://localhost:8000/docs**

## Step 2: Frontend Setup (2 minutes)

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Start Next.js
npm run dev
```

✅ Frontend running on: **http://localhost:3000**
✅ Dashboard: **http://localhost:3000/dashboard**

## Step 3: Test It Out (1 minute)

### View Dashboard
Open: http://localhost:3000/dashboard

You should see:
- ✅ 3 AI models from database
- ✅ Live stats (total models, risk levels, compliance)
- ✅ Risk distribution chart
- ✅ Interactive model table

### Test Bias Detection
Click "Analyze Bias" button on any model in the table.

You'll see:
- Bias score (0-1)
- Fairness metrics
- Group comparisons
- Recommendations

### Test Risk Assessment
Click "Assess Risk" button on any model.

You'll see:
- Risk level (Low/Medium/High)
- Risk score (0-10)
- Risk factors breakdown
- Mitigation strategies

## What's Running

### Sample Data (Pre-loaded)
1. **Customer Credit Scoring Model** (High Risk, Production)
2. **HR Resume Screening Assistant** (High Risk, Testing)
3. **Customer Service Chatbot** (Limited Risk, Production)

### Real Features
✅ SQLite database with encryption
✅ Bias detection with fairness metrics
✅ Risk assessment (6 dimensions)
✅ Compliance checking (EU AI Act, GDPR, NIST)
✅ Audit trails for all assessments
✅ Real-time dashboard updates

## Test via API

### Get all models
```bash
curl http://localhost:8000/api/v1/governance/models
```

### Analyze bias
```bash
curl -X POST http://localhost:8000/api/v1/governance/bias/analyze \
  -H "Content-Type: application/json" \
  -d '{"model_id": "ai_sys_001", "protected_attributes": ["gender", "age"]}'
```

### Assess risk
```bash
curl -X POST http://localhost:8000/api/v1/governance/risk/assess \
  -H "Content-Type: application/json" \
  -d '{"model_id": "ai_sys_001"}'
```

### Check compliance
```bash
curl -X POST http://localhost:8000/api/v1/governance/compliance/check \
  -H "Content-Type: application/json" \
  -d '{"model_id": "ai_sys_001", "regulations": ["EU_AI_ACT", "GDPR"]}'
```

## Troubleshooting

### Backend won't start
```bash
# Make sure dependencies are installed
pip install cryptography
```

### Frontend shows "Failed to load dashboard data"
- Check backend is running on port 8000
- Visit http://localhost:8000/docs to confirm

### Database errors
```bash
# Delete and recreate database
rm backend/data/governance_data.db
# Restart backend - it will auto-create with sample data
```

## Next Steps

✅ Explore the dashboard UI
✅ Test all 3 agents (bias, risk, compliance)
✅ View API docs at http://localhost:8000/docs
✅ Check IMPLEMENTATION_COMPLETE.md for full details
✅ See README.md for architecture overview

---

**You're ready to go!** 🎉
