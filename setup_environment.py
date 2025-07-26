#!/usr/bin/env python3
"""
UtilityPro Environment Setup Script
Author: Vivek Srivastava
Description: Set up the development environment and install dependencies
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version.split()[0]} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path('.venv')
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")

    return venv_path

def get_pip_command(venv_path):
    """Get the pip command for the virtual environment"""
    if platform.system() == "Windows":
        return str(venv_path / "Scripts" / "pip")
    else:
        return str(venv_path / "bin" / "pip")

def install_dependencies(pip_cmd):
    """Install required dependencies"""
    dependencies = [
        "PyQt6>=6.5.0",
        "PyPDF2>=3.0.1",
        "PyMuPDF>=1.23.0",
        "pdf2docx>=0.5.8",
        "python-docx>=0.8.11",
        "Pillow>=10.0.0",
        "typing-extensions>=4.0.0"
    ]

    print("Installing dependencies...")
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.run([pip_cmd, "install", dep], check=True, capture_output=True)
            print(f"✓ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {dep}: {e}")
            return False

    return True

def create_requirements_file():
    """Create requirements.txt file"""
    requirements_content = """# UtilityPro Requirements
# Core GUI Framework
PyQt6>=6.5.0

# PDF Processing
PyPDF2>=3.0.1
PyMuPDF>=1.23.0

# PDF to Word Conversion
pdf2docx>=0.5.8
python-docx>=0.8.11

# Image Processing
Pillow>=10.0.0

# Additional utilities
typing-extensions>=4.0.0
"""

    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    print("✓ requirements.txt created")

def create_run_script():
    """Create platform-specific run scripts"""
    if platform.system() == "Windows":
        run_script = """@echo off
.venv\\Scripts\\python.exe main.py
pause
"""
        with open('run_utility_pro.bat', 'w') as f:
            f.write(run_script)
        print("✓ run_utility_pro.bat created")
    else:
        run_script = """#!/bin/bash
.venv/bin/python main.py
"""
        with open('run_utility_pro.sh', 'w') as f:
            f.write(run_script)
        os.chmod('run_utility_pro.sh', 0o755)
        print("✓ run_utility_pro.sh created")

def verify_installation(venv_path):
    """Verify that all dependencies are installed correctly"""
    python_cmd = str(venv_path / "bin" / "python") if platform.system() != "Windows" else str(venv_path / "Scripts" / "python.exe")

    test_imports = [
        "PyQt6.QtWidgets",
        "PyPDF2",
        "PIL",
        "pdf2docx",
        "docx",
        "fitz"
    ]

    print("\nVerifying installations...")
    for module in test_imports:
        try:
            result = subprocess.run([python_cmd, "-c", f"import {module}; print('✓ {module}')"],
                                    capture_output=True, text=True, check=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError:
            print(f"✗ {module} - Import failed")
            return False

    return True

def main():
    """Main setup function"""
    print("UtilityPro Environment Setup")
    print("=" * 30)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create virtual environment
    try:
        venv_path = create_virtual_environment()
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        sys.exit(1)

    # Get pip command
    pip_cmd = get_pip_command(venv_path)

    # Upgrade pip first
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True, capture_output=True)
        print("✓ pip upgraded")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not upgrade pip: {e}")

    # Install dependencies
    if not install_dependencies(pip_cmd):
        print("Error: Failed to install some dependencies")
        sys.exit(1)

    # Create requirements file
    create_requirements_file()

    # Create run script
    create_run_script()

    # Verify installation
    if verify_installation(venv_path):
        print("\n" + "=" * 50)
        print("✓ Setup completed successfully!")
        print("\nTo run UtilityPro:")
        if platform.system() == "Windows":
            print("  Double-click run_utility_pro.bat")
            print("  Or run: .venv\\Scripts\\python.exe main.py")
        else:
            print("  Run: ./run_utility_pro.sh")
            print("  Or run: .venv/bin/python main.py")
        print("=" * 50)
    else:
        print("\n✗ Setup completed with errors. Please check the installation.")
        sys.exit(1)

if __name__ == "__main__":
    main()