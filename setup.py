#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="utility-pro",
    version="1.0.0",
    author="Vivek Srivastava",
    description="Advanced PDF and Image Manipulation Tool",
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.6.0",
        "PyPDF2>=3.0.1",
        "Pillow>=10.0.0",
        "pdf2docx>=0.5.6",
        "python-docx>=1.1.0",
        "PyMuPDF>=1.23.0",
        "pyinstaller>=6.0.0"
    ],
    entry_points={
        "console_scripts": [
            "utility-pro=main:main"
        ]
    }
)
