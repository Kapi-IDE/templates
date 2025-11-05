#!/usr/bin/env python3
"""
Legal AI Pod - Startup Script
Comprehensive startup script for the Legal AI Case Intelligence System
"""

import os
import sys
import subprocess
import signal
import time
import logging
from pathlib import Path
import argparse
import threading
import webbrowser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LegalAIPodLauncher:
    """Manages startup and coordination of Legal AI Pod services"""
    
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.setup_complete = False
        self.base_dir = Path(__file__).parent
        self.backend_dir = self.base_dir / "backend"
        self.frontend_dir = self.base_dir / "frontend"
        
    def check_requirements(self):
        """Check system requirements and dependencies"""
        logger.info("Checking system requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            logger.error("Python 3.8 or higher is required")
            return False
        
        # Check if directories exist
        if not self.backend_dir.exists():
            logger.error(f"Backend directory not found: {self.backend_dir}")
            return False
            
        if not self.frontend_dir.exists():
            logger.warning(f"Frontend directory not found: {self.frontend_dir}")
        
        logger.info("System requirements check passed")
        return True
    
    def setup_environment(self):
        """Set up environment variables and configuration"""
        logger.info("Setting up environment...")
        
        # Set essential environment variables if not already set
        env_vars = {
            'FLASK_APP': 'app.py',
            'FLASK_ENV': 'development',
            'PYTHONPATH': str(self.backend_dir),
            'LEGAL_AI_MODE': 'development'
        }
        
        for key, value in env_vars.items():
            if key not in os.environ:
                os.environ[key] = value
                logger.debug(f"Set environment variable: {key}={value}")
        
        # Create logs directory
        logs_dir = self.backend_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Create data directories
        (self.backend_dir / "legal_chroma_db").mkdir(exist_ok=True)
        
        logger.info("Environment setup completed")
    
    def install_backend_dependencies(self):
        """Install backend Python dependencies"""
        logger.info("Installing backend dependencies...")
        
        requirements_file = self.backend_dir / "requirements.txt"
        if not requirements_file.exists():
            logger.error(f"Requirements file not found: {requirements_file}")
            return False
        
        try:
            # Install requirements
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, cwd=self.backend_dir)
            
            logger.info("Backend dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install backend dependencies: {e}")
            return False
    
    def install_frontend_dependencies(self):
        """Install frontend Node.js dependencies"""
        if not self.frontend_dir.exists():
            logger.info("Frontend directory not found, skipping frontend setup")
            return True
            
        logger.info("Installing frontend dependencies...")
        
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            logger.error(f"package.json not found: {package_json}")
            return False
        
        try:
            # Check if npm is available
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            
            # Install dependencies
            subprocess.run([
                "npm", "install"
            ], check=True, cwd=self.frontend_dir)
            
            logger.info("Frontend dependencies installed successfully")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.warning(f"Failed to install frontend dependencies: {e}")
            logger.warning("Frontend will not be available")
            return True  # Don't fail the whole setup
    
    def setup_database(self):
        """Initialize and seed the legal database"""
        logger.info("Setting up legal database...")
        
        setup_script = self.backend_dir / "setup_legal_database.py"
        if not setup_script.exists():
            logger.warning("Database setup script not found, skipping initial data seeding")
            return True
        
        try:
            # Change to backend directory and run setup
            original_cwd = os.getcwd()
            os.chdir(self.backend_dir)
            
            subprocess.run([
                sys.executable, str(setup_script)
            ], check=True)
            
            os.chdir(original_cwd)
            logger.info("Legal database setup completed")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Database setup failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Database setup error: {e}")
            return False
    
    def start_backend(self):
        """Start the Flask backend server"""
        logger.info("Starting Legal AI Pod backend...")
        
        app_file = self.backend_dir / "app.py"
        if not app_file.exists():
            logger.error(f"Backend app.py not found: {app_file}")
            return False
        
        try:
            # Start Flask development server
            self.backend_process = subprocess.Popen([
                sys.executable, str(app_file)
            ], cwd=self.backend_dir)
            
            # Give the server time to start
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                logger.info("Backend server started successfully on http://localhost:5000")
                return True
            else:
                logger.error("Backend server failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the React frontend development server"""
        if not self.frontend_dir.exists():
            logger.info("Frontend not available")
            return True
            
        logger.info("Starting Legal AI Pod frontend...")
        
        try:
            # Start React development server
            self.frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=self.frontend_dir)
            
            # Give the server time to start
            time.sleep(5)
            
            if self.frontend_process.poll() is None:
                logger.info("Frontend server started successfully on http://localhost:3000")
                return True
            else:
                logger.warning("Frontend server failed to start")
                return True  # Don't fail the whole startup
                
        except Exception as e:
            logger.warning(f"Failed to start frontend: {e}")
            return True  # Don't fail the whole startup
    
    def open_browser(self):
        """Open the application in the default browser"""
        def delayed_open():
            time.sleep(8)  # Wait for servers to fully start
            try:
                if self.frontend_process and self.frontend_process.poll() is None:
                    webbrowser.open("http://localhost:3000")
                    logger.info("Opened application in browser")
                else:
                    webbrowser.open("http://localhost:5000")
                    logger.info("Opened backend API in browser")
            except Exception as e:
                logger.debug(f"Failed to open browser: {e}")
        
        # Open browser in a separate thread
        threading.Thread(target=delayed_open, daemon=True).start()
    
    def handle_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        logger.info("Shutting down Legal AI Pod...")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
            logger.info("Frontend server stopped")
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
            logger.info("Backend server stopped")
        
        logger.info("Legal AI Pod shutdown complete")
        sys.exit(0)
    
    def run_setup(self, skip_deps=False, skip_db=False):
        """Run the complete setup process"""
        logger.info("Starting Legal AI Pod setup...")
        
        if not self.check_requirements():
            return False
        
        self.setup_environment()
        
        if not skip_deps:
            if not self.install_backend_dependencies():
                return False
            
            if not self.install_frontend_dependencies():
                return False
        
        if not skip_db:
            if not self.setup_database():
                return False
        
        self.setup_complete = True
        logger.info("Legal AI Pod setup completed successfully")
        return True
    
    def run_application(self, open_browser=True):
        """Start the complete Legal AI Pod application"""
        if not self.setup_complete:
            logger.error("Setup not completed. Run setup first.")
            return False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Start frontend
        self.start_frontend()
        
        # Open browser
        if open_browser:
            self.open_browser()
        
        # Display startup information
        self.print_startup_info()
        
        # Keep the main process running
        try:
            while True:
                time.sleep(1)
                
                # Check if backend is still running
                if self.backend_process and self.backend_process.poll() is not None:
                    logger.error("Backend process has stopped")
                    break
                    
        except KeyboardInterrupt:
            self.handle_shutdown(None, None)
        
        return True
    
    def print_startup_info(self):
        """Print application startup information"""
        print("\n" + "="*60)
        print("Legal AI Pod - Case Intelligence System")
        print("="*60)
        print(f"Backend API:  http://localhost:5000")
        
        if self.frontend_process and self.frontend_process.poll() is None:
            print(f"Frontend UI:  http://localhost:3000")
        else:
            print("Frontend:     Not available")
        
        print("\nFeatures Available:")
        print("  • Legal Research & Case Analysis")
        print("  • Document Review & Risk Assessment") 
        print("  • Precedent Mining & Citation Analysis")
        print("  • Attorney-Client Privilege Protection")
        print("  • Legal Ethics Compliance Monitoring")
        print("  • Multi-Agent AI Orchestration")
        
        print("\nAPI Endpoints:")
        print("  • /api/health - System health check")
        print("  • /api/attorney/start-session - Begin attorney session")
        print("  • /api/legal/research - Legal research queries")
        print("  • /api/legal/case-analysis - Case strength analysis")
        print("  • /api/legal/document-review - Document review")
        print("  • /api/legal/precedent-search - Precedent mining")
        
        print("\nPress Ctrl+C to stop the application")
        print("="*60)

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Legal AI Pod Startup Script")
    parser.add_argument("--skip-deps", action="store_true", 
                       help="Skip dependency installation")
    parser.add_argument("--skip-db", action="store_true",
                       help="Skip database setup")
    parser.add_argument("--no-browser", action="store_true",
                       help="Don't open browser automatically")
    parser.add_argument("--setup-only", action="store_true",
                       help="Run setup only, don't start application")
    
    args = parser.parse_args()
    
    launcher = LegalAIPodLauncher()
    
    # Run setup
    if not launcher.run_setup(skip_deps=args.skip_deps, skip_db=args.skip_db):
        logger.error("Setup failed")
        sys.exit(1)
    
    if args.setup_only:
        logger.info("Setup completed. Use --no-setup to start the application.")
        return
    
    # Start application
    if not launcher.run_application(open_browser=not args.no_browser):
        logger.error("Failed to start application")
        sys.exit(1)

if __name__ == "__main__":
    main()