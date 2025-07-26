#!/usr/bin/env python3
"""
Utility Pro - Advanced PDF and Image Manipulation Tool
Author: Vivek Srivastava
Description: Main application entry point with improved error handling
"""

import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon
except ImportError as e:
    print(f"Error importing PyQt6: {e}")
    print("Please install PyQt6 using: pip install PyQt6")
    sys.exit(1)

try:
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Error importing MainWindow: {e}")
    print("Please ensure all project files are present")
    sys.exit(1)

def main():
    """Main application entry point"""
    try:
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("Utility Pro")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Vivek Srivastava")
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        
        # Enable high DPI scaling
        #app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        #app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Create and show main window
        try:
            window = MainWindow()
            window.show()
        except Exception as e:
            logger.error(f"Error creating main window: {e}")
            QMessageBox.critical(None, "Error", f"Failed to create main window: {e}")
            return 1
        
        return app.exec()
        
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        print(f"Critical error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

