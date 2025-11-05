#!/usr/bin/env python3
"""
Database Setup Script
Initializes the SQLite database with proper tables
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database.sqlite_manager import PatientDataManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize SQLite database"""
    try:
        logger.info("Initializing SQLite database...")
        
        # Create patient data manager (this creates tables)
        patient_db = PatientDataManager()
        
        # Get database stats
        stats = patient_db.get_database_stats()
        logger.info(f"Database initialized with tables: {list(stats.keys())}")
        
        # Test database connection
        if patient_db.health_check():
            logger.info("Database health check passed")
        else:
            logger.error("Database health check failed")
            return 1
        
        logger.info("Database setup completed!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())