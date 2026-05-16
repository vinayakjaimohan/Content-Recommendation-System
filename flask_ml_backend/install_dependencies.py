#!/usr/bin/env python3
"""
Dependency installation script for Flask ML Backend
Handles Python 3.13 compatibility issues
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check Python version and provide warnings"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Python 3.13 detected. Some packages may have compatibility issues.")
        print("   If installation fails, consider using Python 3.11 or 3.12.")
        return True
    elif version.major == 3 and version.minor >= 11:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.11+ is required")
        return False

def install_setuptools():
    """Install/upgrade setuptools first"""
    print("Installing/upgrading setuptools...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--upgrade', 'setuptools', 'wheel'
        ])
        print("✅ setuptools installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install setuptools")
        return False

def install_dependencies():
    """Install dependencies with fallback options"""
    print("Installing dependencies...")
    
    # Try different installation methods
    methods = [
        # Method 1: Standard installation
        lambda: subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ]),
        
        # Method 2: Install with --no-deps flag for problematic packages
        lambda: subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--no-deps', '-r', 'requirements.txt'
        ]),
        
        # Method 3: Install packages individually
        lambda: install_packages_individually(),
        
        # Method 4: Use conda if available
        lambda: install_with_conda()
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"Trying installation method {i}...")
            method()
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Method {i} failed: {e}")
            continue
        except Exception as e:
            print(f"❌ Method {i} failed with exception: {e}")
            continue
    
    print("❌ All installation methods failed")
    return False

def install_packages_individually():
    """Install packages one by one to identify problematic ones"""
    packages = [
        'Flask>=2.3.0,<3.0.0',
        'Flask-CORS>=4.0.0,<5.0.0',
        'pandas>=2.0.0,<3.0.0',
        'numpy>=1.24.0,<2.0.0',
        'scikit-learn>=1.3.0,<2.0.0',
        'joblib>=1.3.0,<2.0.0',
        'Werkzeug>=2.3.0,<3.0.0',
        'requests>=2.28.0,<3.0.0'
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package
            ])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            # Try with --no-deps
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--no-deps', package
                ])
                print(f"✅ {package} installed (no deps)")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package} even with --no-deps")
                raise

def install_with_conda():
    """Try installing with conda if available"""
    try:
        # Check if conda is available
        subprocess.run(['conda', '--version'], check=True, capture_output=True)
        print("Conda found, trying conda installation...")
        
        # Install packages with conda
        packages = ['flask', 'flask-cors', 'pandas', 'numpy', 'scikit-learn', 'joblib', 'requests']
        for package in packages:
            subprocess.check_call(['conda', 'install', '-y', package])
        
        print("✅ Dependencies installed with conda")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Conda not available or failed")
        raise

def create_virtual_environment():
    """Create a virtual environment"""
    print("Creating virtual environment...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'venv', 'venv'
        ])
        print("✅ Virtual environment created")
        
        # Activate virtual environment
        if platform.system() == "Windows":
            activate_script = os.path.join("venv", "Scripts", "activate.bat")
            print(f"To activate: {activate_script}")
        else:
            activate_script = os.path.join("venv", "bin", "activate")
            print(f"To activate: source {activate_script}")
        
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def main():
    """Main installation function"""
    print("=" * 50)
    print("FLASK ML BACKEND DEPENDENCY INSTALLER")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install setuptools first
    if not install_setuptools():
        print("⚠️  setuptools installation failed, but continuing...")
    
    # Try to install dependencies
    if install_dependencies():
        print("\n🎉 All dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Run: python start_server.py")
        print("2. Or run: python app.py")
        return True
    else:
        print("\n❌ Installation failed. Try these alternatives:")
        print("\nAlternative 1: Use Python 3.11 or 3.12")
        print("Alternative 2: Create a virtual environment:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # Windows")
        print("   source venv/bin/activate  # Linux/Mac")
        print("   pip install -r requirements.txt")
        print("\nAlternative 3: Install packages manually:")
        print("   pip install Flask Flask-CORS pandas numpy scikit-learn joblib requests")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 