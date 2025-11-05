FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY .env.example .env

# Copy component dependency
COPY ../../../components/backend/langgraph-agent-framework ./components/backend/langgraph-agent-framework

# Expose Gradio port
EXPOSE 7860

# Run application
CMD ["python", "backend/app.py"]
