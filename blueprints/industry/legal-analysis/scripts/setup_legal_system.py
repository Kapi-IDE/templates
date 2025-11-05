#!/usr/bin/env python3
"""
Legal AI Pod - Complete System Setup Script
Initializes all databases, loads legal knowledge, and prepares the system for use
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LegalSystemSetup:
    """Complete setup for Legal AI Pod system"""
    
    def __init__(self):
        """Initialize setup manager"""
        self.project_root = Path(__file__).parent.parent
        self.backend_path = self.project_root / "backend"
        self.data_path = self.backend_path / "data"
        self.scripts_path = self.project_root / "scripts"
        
    def check_prerequisites(self):
        """Check system prerequisites"""
        logger.info("Checking system prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            raise RuntimeError("Python 3.8+ required")
        
        # Check required directories
        required_dirs = [
            self.backend_path,
            self.data_path,
            self.backend_path / "database",
            self.backend_path / "agents",
            self.backend_path / "utils"
        ]
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                logger.error(f"Required directory missing: {dir_path}")
                raise RuntimeError(f"Missing directory: {dir_path}")
        
        # Check data files
        required_data_files = [
            "legal_knowledge.json",
            "legal_entities.json", 
            "legal_ethics_rules.json"
        ]
        
        for file_name in required_data_files:
            file_path = self.data_path / file_name
            if not file_path.exists():
                logger.error(f"Required data file missing: {file_path}")
                raise RuntimeError(f"Missing data file: {file_path}")
        
        logger.info("✓ Prerequisites check passed")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        logger.info("Installing Python dependencies...")
        
        requirements_file = self.backend_path / "requirements.txt"
        if not requirements_file.exists():
            logger.error("requirements.txt not found")
            raise RuntimeError("requirements.txt missing")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, cwd=str(self.backend_path))
            logger.info("✓ Python dependencies installed")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            raise
    
    def setup_environment(self):
        """Setup environment variables"""
        logger.info("Setting up environment...")
        
        env_example = self.backend_path / ".env.example"
        env_file = self.backend_path / ".env"
        
        if not env_file.exists():
            if env_example.exists():
                # Copy example file
                with open(env_example, 'r') as f:
                    env_content = f.read()
                
                with open(env_file, 'w') as f:
                    f.write(env_content)
                
                logger.info("✓ Created .env file from example")
                logger.warning("⚠️  Please edit .env file with your API keys")
            else:
                # Create basic .env file
                env_content = """# Legal AI Pod Environment Variables
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=legal-ai-pod-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
SQLITE_DB_PATH=legal_data.db
CHROMADB_PATH=./chromadb_legal

# Legal System Configuration
ATTORNEY_SESSION_TIMEOUT=3600
PRIVILEGE_ENCRYPTION_KEY=generate-secure-key-here
ETHICS_MONITORING_ENABLED=True

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/legal_app.log
"""
                with open(env_file, 'w') as f:
                    f.write(env_content)
                
                logger.info("✓ Created basic .env file")
                logger.warning("⚠️  Please edit .env file with your API keys")
        else:
            logger.info("✓ Environment file already exists")
    
    def create_directories(self):
        """Create necessary directories"""
        logger.info("Creating necessary directories...")
        
        directories = [
            self.backend_path / "logs",
            self.backend_path / "chromadb_legal",
            self.backend_path / "uploads",
            self.backend_path / "exports"
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            logger.info(f"✓ Created directory: {directory}")
    
    def initialize_databases(self):
        """Initialize SQLite and ChromaDB databases"""
        logger.info("Initializing databases...")
        
        try:
            # Import database managers
            from database.sqlite_legal_manager import LegalDataManager
            from database.chromadb_legal_manager import LegalKnowledgeStore
            
            # Initialize SQLite database
            logger.info("Setting up SQLite legal database...")
            legal_db = LegalDataManager()
            legal_db.initialize_database()
            logger.info("✓ SQLite database initialized")
            
            # Initialize ChromaDB
            logger.info("Setting up ChromaDB legal knowledge store...")
            knowledge_store = LegalKnowledgeStore()
            knowledge_store.initialize_collections()
            logger.info("✓ ChromaDB initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def load_legal_knowledge(self):
        """Load legal knowledge into databases"""
        logger.info("Loading legal knowledge...")
        
        try:
            from database.chromadb_legal_manager import LegalKnowledgeStore
            
            knowledge_store = LegalKnowledgeStore()
            
            # Load legal knowledge data
            legal_knowledge_file = self.data_path / "legal_knowledge.json"
            with open(legal_knowledge_file, 'r') as f:
                legal_data = json.load(f)
            
            # Load case law
            if 'case_law' in legal_data:
                logger.info("Loading case law...")
                for case in legal_data['case_law']:
                    knowledge_store.add_case_law(case)
                logger.info(f"✓ Loaded {len(legal_data['case_law'])} cases")
            
            # Load statutes
            if 'statutes' in legal_data:
                logger.info("Loading statutes...")
                for statute in legal_data['statutes']:
                    knowledge_store.add_statute(statute)
                logger.info(f"✓ Loaded {len(legal_data['statutes'])} statutes")
            
            # Load precedents
            if 'legal_precedents' in legal_data:
                logger.info("Loading legal precedents...")
                for precedent in legal_data['legal_precedents']:
                    knowledge_store.add_precedent(precedent)
                logger.info(f"✓ Loaded {len(legal_data['legal_precedents'])} precedents")
            
            # Load contract templates
            if 'contract_templates' in legal_data:
                logger.info("Loading contract templates...")
                for template in legal_data['contract_templates']:
                    knowledge_store.add_contract_template(template)
                logger.info(f"✓ Loaded {len(legal_data['contract_templates'])} contract templates")
            
        except Exception as e:
            logger.error(f"Failed to load legal knowledge: {e}")
            raise
    
    def load_legal_entities(self):
        """Load legal entities data"""
        logger.info("Loading legal entities...")
        
        try:
            from database.sqlite_legal_manager import LegalDataManager
            
            legal_db = LegalDataManager()
            
            # Load legal entities data
            entities_file = self.data_path / "legal_entities.json"
            with open(entities_file, 'r') as f:
                entities_data = json.load(f)
            
            # Load courts
            if 'courts' in entities_data:
                for court in entities_data['courts']:
                    legal_db.add_court(court)
                logger.info(f"✓ Loaded {len(entities_data['courts'])} courts")
            
            # Load judges
            if 'judges' in entities_data:
                for judge in entities_data['judges']:
                    legal_db.add_judge(judge)
                logger.info(f"✓ Loaded {len(entities_data['judges'])} judges")
            
            # Load law firms
            if 'law_firms' in entities_data:
                for firm in entities_data['law_firms']:
                    legal_db.add_law_firm(firm)
                logger.info(f"✓ Loaded {len(entities_data['law_firms'])} law firms")
            
        except Exception as e:
            logger.error(f"Failed to load legal entities: {e}")
            raise
    
    def setup_ethics_monitoring(self):
        """Setup legal ethics monitoring"""
        logger.info("Setting up legal ethics monitoring...")
        
        try:
            from utils.legal_ethics import LegalEthicsMonitoring
            
            ethics_monitor = LegalEthicsMonitoring()
            
            # Load ethics rules
            ethics_file = self.data_path / "legal_ethics_rules.json"
            with open(ethics_file, 'r') as f:
                ethics_data = json.load(f)
            
            ethics_monitor.load_ethics_rules(ethics_data)
            logger.info("✓ Legal ethics monitoring configured")
            
        except Exception as e:
            logger.error(f"Failed to setup ethics monitoring: {e}")
            raise
    
    def verify_setup(self):
        """Verify system setup"""
        logger.info("Verifying system setup...")
        
        try:
            # Test database connections
            from database.sqlite_legal_manager import LegalDataManager
            from database.chromadb_legal_manager import LegalKnowledgeStore
            
            legal_db = LegalDataManager()
            knowledge_store = LegalKnowledgeStore()
            
            # Test basic operations
            test_query = "contract law"
            results = knowledge_store.search_legal_knowledge(test_query, limit=1)
            
            if results:
                logger.info("✓ Database connections verified")
            else:
                logger.warning("⚠️  Database verification returned no results")
            
            # Test agents
            from agents.research_agent import LegalResearchAgent
            
            research_agent = LegalResearchAgent(knowledge_store, legal_db)
            logger.info("✓ Legal agents initialized successfully")
            
        except Exception as e:
            logger.error(f"System verification failed: {e}")
            raise
    
    def run_complete_setup(self):
        """Run complete system setup"""
        logger.info("Starting Legal AI Pod system setup...")
        
        try:
            self.check_prerequisites()
            self.install_dependencies()
            self.setup_environment()
            self.create_directories()
            self.initialize_databases()
            self.load_legal_knowledge()
            self.load_legal_entities()
            self.setup_ethics_monitoring()
            self.verify_setup()
            
            logger.info("🎉 Legal AI Pod setup completed successfully!")
            logger.info("Next steps:")
            logger.info("1. Edit .env file with your API keys")
            logger.info("2. Run: python backend/app.py")
            logger.info("3. Access the system at http://localhost:5000")
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    setup = LegalSystemSetup()
    setup.run_complete_setup()
