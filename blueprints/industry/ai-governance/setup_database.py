#!/usr/bin/env python3
"""
Database Setup Script for AI Governance Pod (Pod4)
Initializes SQLite database with sample AI systems and governance data
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database.sqlite_manager import GovernanceDataManager
from models.ai_system import AISystem, SystemType, SystemStatus, RiskCategory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Initialize governance database with sample data"""
    try:
        logger.info("Initializing AI Governance Database...")
        
        # Create data directory
        os.makedirs('./data', exist_ok=True)
        
        # Initialize database manager
        governance_db = GovernanceDataManager('./data/ai_governance.db')
        
        logger.info("✅ AI Governance database initialized successfully!")
        logger.info("✅ Sample AI systems and compliance frameworks loaded")
        logger.info("✅ Encryption keys generated for sensitive data")
        logger.info("✅ Audit trail tables created")
        
        # Display summary
        dashboard_data = governance_db.get_governance_dashboard_data()
        
        print("\n" + "="*60)
        print("🏛️  AI GOVERNANCE DATABASE SETUP COMPLETE")
        print("="*60)
        print(f"📊 Total AI Systems: {dashboard_data.get('total_systems', 0)}")
        print(f"🏭 Production Systems: {dashboard_data.get('status_distribution', {}).get('production', 0)}")
        print(f"⚠️  High-Risk Systems: {dashboard_data.get('risk_distribution', {}).get('high_risk', 0)}")
        print(f"✅ Compliant Systems: {dashboard_data.get('compliance_distribution', {}).get('compliant', 0)}")
        print("="*60)
        print("📍 Database Location: ./data/ai_governance.db")
        print("🔐 Encryption Keys: ./data/encryption.key")
        print("📝 Security Audit Logs: ./data/security/audit.log")
        print("="*60)
        print("🚀 Ready for AI Governance Assessments!")
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)