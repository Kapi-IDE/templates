# Usage Guide

This guide provides instructions on how to set up and run the Financial Services AI Pod project.

## Prerequisites

Make sure you have the following installed:
- Python 3.8+
- Node.js 14+ and npm

## Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    (This only needs to be done once)
    ```bash
    python3 init_db.py
    ```

5.  **Run the Flask server:**
    ```bash
    flask run
    ```
    The backend will be running at `http://127.0.0.1:5000`.

## Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Start the React development server:**
    ```bash
    npm start
    ```
    The frontend will open automatically in your browser at `http://localhost:3000`.
