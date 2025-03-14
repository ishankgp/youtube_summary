import subprocess
import os
import sys
import time
import webbrowser
import signal
import logging
from typing import List, Optional
from pathlib import Path
import pkg_resources
import platform
import json
import logging.handlers
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_logging():
    """Configure logging to both file and console"""
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"app_{timestamp}.log"

    # Configure logging format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Create formatters and handlers
    console_formatter = logging.Formatter(log_format)
    file_formatter = logging.Formatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)

    # Get the root logger and set its level
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers and add our handlers
    root_logger.handlers = []
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logger.info(f"Logging to file: {log_file}")
    return log_file

class AppManager:
    def __init__(self):
        self.frontend_process: Optional[subprocess.Popen] = None
        self.backend_process: Optional[subprocess.Popen] = None
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:8000"
        
        # Get the project root directory
        self.root_dir = Path(__file__).parent
        self.frontend_dir = self.root_dir / "frontend" / "new-app"
        
        # Check if we're on Windows
        self.is_windows = platform.system() == "Windows"
        
        # Initialize npm command
        self.npm_cmd = "npm"

    def check_dependencies(self) -> None:
        """Check if all required dependencies are installed"""
        try:
            logger.info("Checking dependencies...")
            
            # Check Python version
            python_version = sys.version.split()[0]
            logger.info(f"Python version: {python_version}")
            
            # Check Node.js and npm
            try:
                node_version = subprocess.run(
                    ["node", "--version"],
                    capture_output=True,
                    text=True,
                    shell=True
                ).stdout.strip()
                npm_version = subprocess.run(
                    ["npm", "--version"],
                    capture_output=True,
                    text=True,
                    shell=True
                ).stdout.strip()
                logger.info(f"Node.js version: {node_version}")
                logger.info(f"npm version: {npm_version}")
            except Exception as e:
                logger.error(f"Failed to check Node.js/npm: {str(e)}")
                logger.error("Please install Node.js and npm before running this application")
                sys.exit(1)

            # Check Python packages
            required_packages = {
                'fastapi': 'latest',
                'uvicorn': 'latest',
                'python-dotenv': 'latest',
                'google-generativeai': 'latest',
                'youtube-transcript-api': 'latest'
            }
            
            for package, version in required_packages.items():
                try:
                    pkg_resources.require(package)
                    logger.info(f"Found {package}")
                except pkg_resources.DistributionNotFound:
                    logger.info(f"Installing {package}...")
                    try:
                        subprocess.check_call([
                            sys.executable, "-m", "pip", "install", 
                            f"{package}=={version}" if version != 'latest' else package
                        ])
                        logger.info(f"Successfully installed {package}")
                    except subprocess.CalledProcessError as e:
                        logger.error(f"Failed to install {package}: {str(e)}")
                        raise
                
        except Exception as e:
            logger.error(f"Dependency check failed: {str(e)}")
            raise

    def start_backend(self) -> None:
        """Start the FastAPI backend server"""
        try:
            logger.info("Starting backend server...")
            command = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
            
            # Use shell=True on Windows to handle command properly
            self.backend_process = subprocess.Popen(
                command,
                cwd=self.root_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=self.is_windows
            )
            
            # Wait for backend to be ready
            self._wait_for_service(self.backend_url)
            logger.info("Backend server started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start backend: {str(e)}")
            self.cleanup()
            sys.exit(1)

    def start_frontend(self) -> None:
        """Start the Next.js frontend development server"""
        try:
            logger.info("Starting frontend development server...")
            
            # First, ensure all dependencies are installed
            logger.info("Installing frontend dependencies...")
            try:
                logger.info("Running npm install...")
                subprocess.run(
                    ["npm", "install"],
                    cwd=self.frontend_dir,
                    check=True,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                logger.info("Frontend dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install frontend dependencies: {e.stderr}")
                logger.error("Please try running 'npm install' manually in the frontend/new-app directory")
                raise

            # Clean .next directory
            logger.info("Cleaning Next.js build directory...")
            next_dir = self.frontend_dir / ".next"
            if next_dir.exists():
                import shutil
                try:
                    shutil.rmtree(next_dir)
                    logger.info("Successfully cleaned .next directory")
                except Exception as e:
                    logger.warning(f"Failed to clean .next directory: {e}")
                    logger.warning("Continuing with existing .next directory...")
            
            # Build the application
            logger.info("Building Next.js application...")
            try:
                subprocess.run(
                    ["npm", "run", "build"],
                    cwd=self.frontend_dir,
                    check=True,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                logger.info("Next.js build completed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to build Next.js application: {e.stderr}")
                logger.error("Please check for any TypeScript or build errors in your frontend code")
                raise
            
            # Start the development server
            logger.info("Starting Next.js development server...")
            command = "npm run dev"
            
            # Set environment variables including PATH
            env = {
                **os.environ,
                'FORCE_COLOR': 'true',
                'NODE_ENV': 'development',
                'NEXT_TELEMETRY_DISABLED': '1'  # Disable telemetry
            }
            
            self.frontend_process = subprocess.Popen(
                command,
                cwd=self.frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
                env=env
            )
            
            # Monitor startup with increased timeout
            success = False
            start_time = time.time()
            timeout = 120  # Increased timeout to 120 seconds
            startup_output = []

            while time.time() - start_time < timeout:
                if self.frontend_process.poll() is not None:
                    error_output = self.frontend_process.stderr.read() if self.frontend_process.stderr else "No error output"
                    stdout_output = self.frontend_process.stdout.read() if self.frontend_process.stdout else "No stdout output"
                    logger.error(f"Frontend process exited with code {self.frontend_process.returncode}")
                    logger.error(f"Frontend stdout: {stdout_output}")
                    logger.error(f"Frontend stderr: {error_output}")
                    raise RuntimeError(f"Frontend process failed to start: {error_output}")

                if self.frontend_process.stdout:
                    line = self.frontend_process.stdout.readline()
                    if line:
                        startup_output.append(line.strip())
                        logger.info(f"Frontend stdout: {line.strip()}")
                        # Check for various success indicators
                        if any(indicator in line.lower() for indicator in [
                            "ready started server",
                            "localhost:3000",
                            "ready - started server",
                            "successfully compiled",
                            "ready in",
                            "compiled successfully",
                            "compiled client and server successfully"
                        ]):
                            success = True
                            break

                if self.frontend_process.stderr:
                    line = self.frontend_process.stderr.readline()
                    if line and not "deprecated" in line.lower():  # Ignore deprecation warnings
                        startup_output.append(line.strip())
                        logger.warning(f"Frontend stderr: {line.strip()}")

                time.sleep(0.1)

            if not success:
                logger.error("Frontend startup failed. Complete output:")
                for line in startup_output:
                    logger.error(line)
                raise TimeoutError("Frontend server failed to start within timeout period")

            logger.info("Frontend development server started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start frontend: {str(e)}")
            self.cleanup()
            sys.exit(1)

    def _wait_for_service(self, url: str, timeout: int = 30) -> None:
        """Wait for a service to be ready"""
        import urllib.request
        import urllib.error
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Add error handling for different URL schemes
                if url.startswith('http://localhost'):
                    port = url.split(':')[-1]
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('localhost', int(port)))
                    sock.close()
                    if result == 0:
                        return
                else:
                    urllib.request.urlopen(url)
                    return
            except (urllib.error.URLError, socket.error):
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Service check error: {str(e)}")
                time.sleep(1)
        raise TimeoutError(f"Service at {url} did not start within {timeout} seconds")

    def open_browser(self) -> None:
        """Open the application in the default web browser"""
        try:
            logger.info("Opening application in browser...")
            webbrowser.open(self.frontend_url)
        except Exception as e:
            logger.error(f"Failed to open browser: {str(e)}")

    def cleanup(self) -> None:
        """Cleanup processes on shutdown"""
        logger.info("Cleaning up processes...")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait(timeout=5)
            
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait(timeout=5)

    def monitor_output(self) -> None:
        """Monitor and log output from both processes"""
        while True:
            # Monitor backend output
            if self.backend_process and self.backend_process.stdout:
                backend_output = self.backend_process.stdout.readline()
                if backend_output:
                    logger.info(f"Backend: {backend_output.strip()}")

            # Monitor frontend output
            if self.frontend_process and self.frontend_process.stdout:
                frontend_output = self.frontend_process.stdout.readline()
                if frontend_output:
                    logger.info(f"Frontend: {frontend_output.strip()}")

            # Check if either process has terminated
            if (self.backend_process and self.backend_process.poll() is not None) or \
               (self.frontend_process and self.frontend_process.poll() is not None):
                logger.error("One of the processes has terminated unexpectedly")
                self.cleanup()
                sys.exit(1)

            time.sleep(0.1)

    def run(self) -> None:
        """Run the application"""
        try:
            # Register signal handlers
            signal.signal(signal.SIGINT, lambda s, f: self.cleanup())
            signal.signal(signal.SIGTERM, lambda s, f: self.cleanup())

            # Check frontend structure
            logger.info("Checking frontend structure...")
            self.check_frontend_structure()

            # Verify frontend environment
            self.verify_frontend_env()

            # Install frontend dependencies if needed
            if not (self.frontend_dir / "node_modules").exists():
                self.install_frontend_deps()

            # Start services
            self.start_backend()
            self.start_frontend()
            
            # Open browser after a short delay
            time.sleep(2)
            self.open_browser()

            # Monitor output
            self.monitor_output()

        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Application startup failed: {str(e)}")
            self.cleanup()
            sys.exit(1)
        finally:
            self.cleanup()

    def check_frontend_structure(self) -> None:
        """Check if frontend structure is correct"""
        try:
            # Check frontend directory
            if not self.frontend_dir.exists():
                logger.error(f"Frontend directory not found at {self.frontend_dir}")
                raise FileNotFoundError(f"Frontend directory not found at {self.frontend_dir}")

            # Check for package.json only
            if not (self.frontend_dir / "package.json").exists():
                logger.error("package.json not found in frontend directory")
                raise FileNotFoundError("package.json not found in frontend directory")
                
            logger.info("Frontend structure check passed")
                
        except Exception as e:
            logger.error(f"Frontend structure check failed: {str(e)}")
            raise

    def create_react_app(self) -> None:
        """Create a new React app using Vite"""
        try:
            logger.info("Creating new React app with Vite...")
            subprocess.run(
                [self.npm_cmd, "create", "vite@latest", "new-app", "--", "--template", "react-ts"],
                cwd=self.root_dir / "frontend",
                check=True,
                shell=True
            )
            logger.info("React app created successfully")
        except Exception as e:
            logger.error(f"Failed to create React app: {str(e)}")
            raise

    def install_frontend_deps(self) -> None:
        """Install frontend dependencies"""
        try:
            logger.info("Installing frontend dependencies...")
            subprocess.run(
                [self.npm_cmd, "install"],
                cwd=self.frontend_dir,
                check=True,
                shell=True,
                capture_output=True,
                text=True
            )
            logger.info("Frontend dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install frontend dependencies: {e.stderr}")
            raise

    def verify_frontend_env(self) -> None:
        """Verify frontend environment and dependencies"""
        try:
            logger.info("Verifying frontend environment...")
            
            # Check if frontend directory exists
            if not self.frontend_dir.exists():
                logger.error(f"Frontend directory not found at: {self.frontend_dir}")
                logger.info("Creating frontend directory structure...")
                self.frontend_dir.mkdir(parents=True, exist_ok=True)
                
                # Initialize new Next.js project
                logger.info("Initializing new Next.js project...")
                subprocess.run(
                    [self.npm_cmd, "create", "next-app@latest", "new-app", "--typescript", "--tailwind", "--eslint"],
                    cwd=self.root_dir / "frontend",
                    check=True,
                    shell=True
                )
                logger.info("Next.js project initialized successfully")
                return

            # Check package.json
            package_json_path = self.frontend_dir / "package.json"
            if not package_json_path.exists():
                raise FileNotFoundError(f"package.json not found at {package_json_path}")
            
            # Read and log package.json contents
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_json = json.load(f)
                    logger.info("package.json contents:")
                    logger.info(json.dumps(package_json, indent=2))
                    
                    scripts = package_json.get('scripts', {})
                    logger.info(f"Available scripts: {scripts}")
                    
                    if 'dev' not in scripts:
                        logger.error("No 'dev' script found in package.json")
                        logger.info("Available scripts: " + ", ".join(scripts.keys()))
                        raise RuntimeError("Required 'dev' script not found in package.json")
                    else:
                        logger.info(f"Found dev script: {scripts['dev']}")
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing package.json: {e}")
                raise
            except Exception as e:
                logger.error(f"Error reading package.json: {e}")
                raise

            # Check for Next.js dependencies
            dependencies = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}
            if 'next' not in dependencies:
                logger.warning("Next.js dependency not found in package.json")

            logger.info("Frontend environment verification complete")
            
        except Exception as e:
            logger.error(f"Frontend environment verification failed: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {str(e)}")
            raise

def main():
    """Main entry point"""
    try:
        # Setup logging first
        log_file = setup_logging()
        logger.info("Starting application...")
        logger.info(f"Working directory: {os.getcwd()}")

        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Run YouTube Summary Application')
        parser.add_argument('--backend', action='store_true', help='Run only the backend server')
        parser.add_argument('--frontend', action='store_true', help='Run only the frontend server')
        args = parser.parse_args()
        
        app_manager = AppManager()
        
        # Check dependencies first
        logger.info("Checking dependencies...")
        app_manager.check_dependencies()
        
        if args.backend:
            # Run only backend
            app_manager.start_backend()
            logger.info("Backend server is running. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Stopping backend server...")
                app_manager.cleanup()
                
        elif args.frontend:
            # Verify frontend environment before starting
            app_manager.verify_frontend_env()
            # Run only frontend
            app_manager.start_frontend()
            logger.info("Frontend server is running. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Stopping frontend server...")
                app_manager.cleanup()
                
        else:
            # Run both (default behavior)
            app_manager.run()
        
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)
    finally:
        logger.info(f"Log file location: {log_file}")

if __name__ == "__main__":
    main() 