#!/usr/bin/env python3
"""
Quick Start Script
One-command setup for the Healthcare AI Pod
"""

import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run command and handle errors"""
    logger.info(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} failed: {e.stderr}")
        return False

def main():
    """Quick start setup"""
    logger.info("🏥 Healthcare AI Pod - Quick Start Setup")
    logger.info("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher required")
        return 1
    
    # Setup steps
    steps = [
        ("python setup_database.py", "Setting up SQLite database"),
        ("python setup_chromadb.py", "Setting up ChromaDB vector database"),
    ]
    
    # Run setup steps
    for command, description in steps:
        if not run_command(command, description):
            logger.error("Setup failed. Please check error messages above.")
            return 1
    
    logger.info("=" * 50)
    logger.info("🎉 Healthcare AI Pod setup completed successfully!")
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. Copy .env.example to .env and add your GOOGLE_API_KEY")
    logger.info("2. Run: python backend/app.py")
    logger.info("3. Open another terminal and run: cd frontend && npm start")
    logger.info("")
    logger.info("Your Healthcare AI system will be available at:")
    logger.info("- Backend API: http://localhost:5000")
    logger.info("- Frontend UI: http://localhost:3000")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())