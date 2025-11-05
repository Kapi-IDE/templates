#!/usr/bin/env python3
"""
Legal AI Pod - Quick Start Script
One-command setup and launch for the Legal AI system
"""

import os
import sys
import subprocess
import time
import webbrowser
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LegalAIQuickStart:
    """Quick start manager for Legal AI Pod"""
    
    def __init__(self):
        """Initialize quick start manager"""
        self.project_root = Path(__file__).parent.parent
        self.backend_path = self.project_root / "backend"
        self.frontend_path = self.project_root / "frontend"
        self.scripts_path = self.project_root / "scripts"
        
    def print_banner(self):
        """Print Legal AI Pod banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    Legal AI Pod                              ║
║              Case Intelligence System                        ║
║                                                              ║
║    🏛️  Advanced Legal Research & Analysis                    ║
║    ⚖️  Attorney-Client Privilege Protection                  ║
║    🤖  Multi-Agent Legal AI Orchestration                   ║
║    🔒  Professional Responsibility Compliance               ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        logger.info("Starting Legal AI Pod Quick Start...")
    
    def check_system_requirements(self):
        """Check system requirements"""
        logger.info("Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            logger.error("Python 3.8+ required")
            return False
        
        # Check if backend directory exists
        if not self.backend_path.exists():
            logger.error(f"Backend directory not found: {self.backend_path}")
            return False
        
        # Check if requirements.txt exists
        requirements_file = self.backend_path / "requirements.txt"
        if not requirements_file.exists():
            logger.error("requirements.txt not found")
            return False
        
        logger.info("✓ System requirements check passed")
        return True
    
    def setup_virtual_environment(self):
        """Setup Python virtual environment"""
        logger.info("Setting up virtual environment...")
        
        venv_path = self.project_root / "venv"
        
        if not venv_path.exists():
            logger.info("Creating virtual environment...")
            subprocess.run([
                sys.executable, "-m", "venv", str(venv_path)
            ], check=True)
        
        # Determine activation script path
        if os.name == 'nt':  # Windows
            activate_script = venv_path / "Scripts" / "activate.bat"
            python_executable = venv_path / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            activate_script = venv_path / "bin" / "activate"
            python_executable = venv_path / "bin" / "python"
        
        if not python_executable.exists():
            logger.error("Virtual environment setup failed")
            return False
        
        logger.info("✓ Virtual environment ready")
        return str(python_executable)
    
    def install_dependencies(self, python_executable):
        """Install Python dependencies"""
        logger.info("Installing dependencies...")
        
        requirements_file = self.backend_path / "requirements.txt"
        
        try:
            subprocess.run([
                python_executable, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True, cwd=str(self.backend_path))
            
            subprocess.run([
                python_executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, cwd=str(self.backend_path))
            
            logger.info("✓ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def setup_environment_file(self):
        """Setup environment configuration"""
        logger.info("Setting up environment configuration...")
        
        env_file = self.backend_path / ".env"
        
        if not env_file.exists():
            env_content = """# Legal AI Pod Environment Variables
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=legal-ai-pod-development-key
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
SQLITE_DB_PATH=legal_data.db
CHROMADB_PATH=./chromadb_legal

# Legal System Configuration
ATTORNEY_SESSION_TIMEOUT=3600
PRIVILEGE_ENCRYPTION_KEY=dev-encryption-key-change-in-production
ETHICS_MONITORING_ENABLED=True

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/legal_app.log
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            
            logger.info("✓ Environment file created")
            logger.warning("⚠️  Please add your GEMINI_API_KEY to .env file")
        else:
            logger.info("✓ Environment file already exists")
    
    def run_system_setup(self, python_executable):
        """Run complete system setup"""
        logger.info("Running system setup...")
        
        setup_script = self.scripts_path / "setup_legal_system.py"
        
        if setup_script.exists():
            try:
                subprocess.run([
                    python_executable, str(setup_script)
                ], check=True, cwd=str(self.project_root))
                
                logger.info("✓ System setup completed")
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"System setup failed: {e}")
                return False
        else:
            logger.warning("Setup script not found, running basic initialization...")
            
            # Run basic database setup
            setup_db_script = self.backend_path / "setup_legal_database.py"
            if setup_db_script.exists():
                try:
                    subprocess.run([
                        python_executable, str(setup_db_script)
                    ], check=True, cwd=str(self.backend_path))
                    
                    logger.info("✓ Database setup completed")
                    return True
                except subprocess.CalledProcessError as e:
                    logger.error(f"Database setup failed: {e}")
                    return False
            
            return True
    
    def start_backend_server(self, python_executable):
        """Start the Flask backend server"""
        logger.info("Starting Legal AI backend server...")
        
        app_file = self.backend_path / "app.py"
        
        if not app_file.exists():
            logger.error("app.py not found in backend directory")
            return None
        
        try:
            # Start backend server in background
            process = subprocess.Popen([
                python_executable, str(app_file)
            ], cwd=str(self.backend_path))
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is None:
                logger.info("✓ Backend server started successfully")
                return process
            else:
                logger.error("Backend server failed to start")
                return None
                
        except Exception as e:
            logger.error(f"Failed to start backend server: {e}")
            return None
    
    def check_frontend_available(self):
        """Check if frontend is available"""
        return self.frontend_path.exists() and (self.frontend_path / "package.json").exists()
    
    def start_frontend_server(self):
        """Start the React frontend server"""
        if not self.check_frontend_available():
            logger.info("Frontend not available, skipping...")
            return None
        
        logger.info("Starting Legal AI frontend server...")
        
        try:
            # Install npm dependencies if needed
            node_modules = self.frontend_path / "node_modules"
            if not node_modules.exists():
                logger.info("Installing frontend dependencies...")
                subprocess.run([
                    "npm", "install"
                ], check=True, cwd=str(self.frontend_path))
            
            # Start frontend server
            process = subprocess.Popen([
                "npm", "start"
            ], cwd=str(self.frontend_path))
            
            time.sleep(5)  # Wait for frontend to start
            
            if process.poll() is None:
                logger.info("✓ Frontend server started successfully")
                return process
            else:
                logger.error("Frontend server failed to start")
                return None
                
        except Exception as e:
            logger.error(f"Failed to start frontend server: {e}")
            return None
    
    def open_browser(self):
        """Open browser to the application"""
        logger.info("Opening Legal AI Pod in browser...")
        
        try:
            # Try frontend first, then backend
            urls_to_try = [
                "http://localhost:3000",  # React frontend
                "http://localhost:5000"   # Flask backend
            ]
            
            for url in urls_to_try:
                try:
                    webbrowser.open(url)
                    logger.info(f"✓ Opened browser to {url}")
                    break
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
    
    def print_success_message(self):
        """Print success message with instructions"""
        success_message = """
🎉 Legal AI Pod is now running!

📍 Access Points:
   • Frontend: http://localhost:3000 (if available)
   • Backend API: http://localhost:5000
   • API Documentation: http://localhost:5000/docs

🔧 Configuration:
   • Edit backend/.env for API keys and settings
   • Check backend/logs/ for system logs
   • Review data/ directory for legal knowledge base

⚖️ Legal Features:
   • Legal Research & Case Analysis
   • Attorney-Client Privilege Protection  
   • Multi-Agent Legal AI Coordination
   • Professional Responsibility Compliance

📚 Next Steps:
   1. Add your GEMINI_API_KEY to backend/.env
   2. Explore the legal research interface
   3. Test multi-agent legal analysis
   4. Review ethics compliance features

Press Ctrl+C to stop the servers when done.
        """
        print(success_message)
    
    def run_quick_start(self):
        """Run complete quick start process"""
        self.print_banner()
        
        try:
            # Check system requirements
            if not self.check_system_requirements():
                logger.error("System requirements not met")
                return False
            
            # Setup virtual environment
            python_executable = self.setup_virtual_environment()
            if not python_executable:
                logger.error("Virtual environment setup failed")
                return False
            
            # Install dependencies
            if not self.install_dependencies(python_executable):
                logger.error("Dependency installation failed")
                return False
            
            # Setup environment
            self.setup_environment_file()
            
            # Run system setup
            if not self.run_system_setup(python_executable):
                logger.error("System setup failed")
                return False
            
            # Start backend server
            backend_process = self.start_backend_server(python_executable)
            if not backend_process:
                logger.error("Failed to start backend server")
                return False
            
            # Start frontend server (optional)
            frontend_process = self.start_frontend_server()
            
            # Open browser
            self.open_browser()
            
            # Print success message
            self.print_success_message()
            
            # Keep processes running
            try:
                while True:
                    time.sleep(1)
                    
                    # Check if backend is still running
                    if backend_process.poll() is not None:
                        logger.error("Backend server stopped unexpectedly")
                        break
                        
            except KeyboardInterrupt:
                logger.info("Shutting down Legal AI Pod...")
                
                # Terminate processes
                if backend_process:
                    backend_process.terminate()
                if frontend_process:
                    frontend_process.terminate()
                
                logger.info("Legal AI Pod stopped")
            
            return True
            
        except Exception as e:
            logger.error(f"Quick start failed: {e}")
            return False

if __name__ == "__main__":
    quick_start = LegalAIQuickStart()
    success = quick_start.run_quick_start()
    
    if not success:
        sys.exit(1)
