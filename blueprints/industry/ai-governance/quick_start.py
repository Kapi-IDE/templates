#!/usr/bin/env python3
"""
Quick Start Script for AI Governance Pod (Pod4)
Complete setup and launch of AI Governance system
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python version: {sys.version}")
    return True

def check_environment_variables():
    """Check required environment variables"""
    logger.info("Checking environment variables...")
    
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        logger.warning("⚠️  GOOGLE_API_KEY not found in environment")
        logger.info("Please set GOOGLE_API_KEY for AI agent functionality")
        logger.info("Get your API key from: https://makersuite.google.com/app/apikey")
        
        # Create .env file template
        env_template = """# AI Governance Pod Environment Variables
GOOGLE_API_KEY=your_gemini_api_key_here
SECRET_KEY=change-this-in-production
HOST=0.0.0.0
PORT=5001
DEBUG=True
"""
        with open('.env', 'w') as f:
            f.write(env_template)
        
        logger.info("📝 Created .env template file - please update with your API key")
        return False
    
    logger.info("✅ Environment variables configured")
    return True

def install_dependencies():
    """Install Python dependencies"""
    logger.info("Installing Python dependencies...")
    
    try:
        # Install dependencies
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'
        ], check=True, capture_output=True, text=True)
        
        logger.info("✅ Python dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("❌ requirements.txt not found")
        return False

def setup_directories():
    """Create necessary directories"""
    logger.info("Setting up directories...")
    
    directories = [
        './data',
        './data/chromadb',
        './data/security',
        './logs',
        './frontend/public',
        './frontend/src'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("✅ Directories created")

def setup_databases():
    """Initialize databases"""
    logger.info("Initializing databases...")
    
    try:
        # Setup SQLite database
        logger.info("Setting up SQLite governance database...")
        result = subprocess.run([sys.executable, 'setup_database.py'], 
                              check=True, capture_output=True, text=True)
        logger.info("✅ SQLite database initialized")
        
        # Setup ChromaDB knowledge store
        logger.info("Setting up ChromaDB knowledge store...")
        result = subprocess.run([sys.executable, 'setup_chromadb.py'], 
                              check=True, capture_output=True, text=True)
        logger.info("✅ ChromaDB knowledge store initialized")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Database setup failed: {e.stderr}")
        return False

def start_backend_server():
    """Start the Flask backend server"""
    logger.info("Starting AI Governance backend server...")
    
    try:
        # Add current directory to Python path
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd() + '/backend:' + env.get('PYTHONPATH', '')
        
        # Start Flask server in background
        process = subprocess.Popen([
            sys.executable, 'backend/app.py'
        ], env=env)
        
        # Give server time to start
        time.sleep(3)
        
        # Check if server is still running
        if process.poll() is None:
            logger.info("✅ Backend server started successfully")
            logger.info("🌐 Server running at: http://localhost:5001")
            return True, process
        else:
            logger.error("❌ Backend server failed to start")
            return False, None
            
    except Exception as e:
        logger.error(f"❌ Failed to start backend server: {str(e)}")
        return False, None

def run_health_check():
    """Run system health check"""
    logger.info("Running system health check...")
    
    try:
        import requests
        
        # Wait a moment for server to be ready
        time.sleep(2)
        
        response = requests.get('http://localhost:5001/api/health', timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get('status') == 'healthy':
                logger.info("✅ System health check passed")
                return True
            else:
                logger.warning("⚠️  System health check returned unhealthy status")
                return False
        else:
            logger.error(f"❌ Health check failed with status code: {response.status_code}")
            return False
            
    except ImportError:
        logger.warning("⚠️  requests library not available, skipping health check")
        logger.info("Install requests with: pip install requests")
        return True
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        return False

def display_success_message():
    """Display success message with next steps"""
    print("\n" + "="*70)
    print("🎉 AI GOVERNANCE POD (POD4) SETUP COMPLETE!")
    print("="*70)
    print("🏛️  Enterprise AI Governance - Regulatory Compliance Platform")
    print("="*70)
    print("📡 Backend API Server: http://localhost:5001")
    print("🏥 Health Check: http://localhost:5001/api/health")
    print("📊 Database: ./data/ai_governance.db")
    print("📚 Knowledge Base: ./data/chromadb/")
    print("🔒 Security Logs: ./data/security/audit.log")
    print("="*70)
    print("🔧 API ENDPOINTS:")
    print("   • POST /api/governance/start-assessment")
    print("   • POST /api/governance/assess-system")
    print("   • GET  /api/governance/system-history")
    print("   • GET  /api/governance/dashboard")
    print("   • POST /api/governance/compliance-report")
    print("   • POST /api/governance/policy-search")
    print("   • POST /api/governance/risk-monitoring")
    print("="*70)
    print("🤖 AI AGENTS:")
    print("   • Risk Assessment Agent (Multi-dimensional risk analysis)")
    print("   • Policy Compliance Agent (Regulatory framework compliance)")
    print("   • Bias Detection Agent (Fairness and bias analysis)")
    print("   • Audit Documentation Agent (Comprehensive documentation)")
    print("="*70)
    print("📋 REGULATORY FRAMEWORKS:")
    print("   • EU AI Act 2024 (Complete implementation)")
    print("   • NIST AI Risk Management Framework 1.0")
    print("   • ISO/IEC 42001:2023 AI Management System")
    print("   • GDPR AI-specific requirements")
    print("="*70)
    print("🚀 NEXT STEPS:")
    print("   1. Set your GOOGLE_API_KEY in .env file")
    print("   2. Test with: curl http://localhost:5001/api/health")
    print("   3. Start governance assessment via API")
    print("   4. Review audit documentation and compliance reports")
    print("   5. Monitor AI systems for regulatory compliance")
    print("="*70)
    print("📖 For detailed usage instructions, see Pod4.md")
    print("🎓 Part of Modern AI Pro Practitioner Course")
    print("="*70)

def main():
    """Main setup function"""
    print("🏛️  AI GOVERNANCE POD (POD4) - QUICK START")
    print("Enterprise AI Audit Platform Setup")
    print("="*60)
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Setup directories
    setup_directories()
    
    # Step 3: Check environment variables
    if not check_environment_variables():
        print("\n⚠️  Please update .env file with your GOOGLE_API_KEY and run again")
        return False
    
    # Step 4: Install dependencies
    if not install_dependencies():
        return False
    
    # Step 5: Setup databases
    if not setup_databases():
        return False
    
    # Step 6: Start backend server
    success, process = start_backend_server()
    if not success:
        return False
    
    # Step 7: Run health check
    if run_health_check():
        display_success_message()
        
        # Keep server running
        try:
            print("\n⏳ Server is running. Press Ctrl+C to stop...")
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down AI Governance Pod...")
            process.terminate()
            print("✅ Shutdown complete")
        
        return True
    else:
        if process:
            process.terminate()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)