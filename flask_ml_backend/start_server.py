#!/usr/bin/env python3
"""
Startup script for the Flask ML Backend
Handles environment setup and server startup
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors', 
        'pandas',
        'numpy',
        'sklearn',
        'joblib',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        # Try the new installation script first
        try:
            print("Trying advanced installation method...")
            subprocess.check_call([
                sys.executable, 'install_dependencies.py'
            ])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Advanced installation failed, trying standard method...")
            
            # Fallback to standard pip install
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
                ])
                print("✅ Dependencies installed successfully")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies")
                print("\nTroubleshooting tips:")
                print("1. Try running: python install_dependencies.py")
                print("2. Consider using Python 3.11 or 3.12 instead of 3.13")
                print("3. Create a virtual environment:")
                print("   python -m venv venv")
                print("   venv\\Scripts\\activate  # Windows")
                print("   pip install -r requirements.txt")
                return False
    
    return True

def check_data_files():
    """Check if required data files exist"""
    print("\nChecking data files...")
    
    required_files = [
        'tfidf_vectorizer.pkl',
        'processed_movies.csv', 
        'rating.csv'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file) / (1024 * 1024)  # Size in MB
            print(f"✅ {file} ({file_size:.1f} MB)")
        else:
            missing_files.append(file)
            print(f"❌ {file} - MISSING")
    
    if missing_files:
        print(f"\n❌ Missing required data files: {', '.join(missing_files)}")
        print("Please ensure all data files are present in the current directory.")
        return False
    
    return True

def start_server():
    """Start the Flask server"""
    print("\nStarting Flask server...")
    
    try:
        # Import and run the app
        from app import app, load_model_artifacts
        
        print("Loading model artifacts...")
        if load_model_artifacts():
            print("✅ Model loaded successfully")
            print("🚀 Starting Flask server on http://localhost:5000")
            print("Press Ctrl+C to stop the server")
            
            # Start the server
            app.run(debug=True, port=5000, host='0.0.0.0')
        else:
            print("❌ Failed to load model artifacts")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main startup function"""
    print("=" * 50)
    print("FLASK ML BACKEND STARTUP")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ app.py not found. Please run this script from the flask_ml_backend directory.")
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check data files
    if not check_data_files():
        return False
    
    # Start server
    return start_server()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 