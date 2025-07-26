# UtilityPro

**Author:** Vivek Srivastava  
**Version:** 1.0.0

## Overview
UtilityPro is a comprehensive desktop application for PDF and image manipulation built with PyQt6.

## Features
- PDF Operations: Merge, Split, Convert to Word/Pages/Images
- Image Operations: Convert to PDF, Resize, Format conversion, Filters
- Drag & Drop Interface
- Batch Processing
- Dark/Light Themes
- Multi-threading

## Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Building Executable
```bash
pyinstaller build.spec
```

## Usage
1. Launch the application
2. Select operation from sidebar
3. Add files via drag & drop
4. Configure settings
5. Process files

## Dependencies
- PyQt6 - GUI framework
- PyPDF2 - PDF manipulation  
- Pillow - Image processing
- pdf2docx - PDF to Word conversion
- python-docx - Word document creation

## Support
For issues or questions, please create a GitHub issue.
