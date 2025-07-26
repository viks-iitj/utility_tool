"""
Utility Pro - Application Styles
Author: Vivek Srivastava
Description: Light and dark theme definitions
"""

# Light Theme
LIGHT_THEME = """
QMainWindow {
    background-color: #f8f9fa;
    color: #212529;
}

/* Sidebar */
QFrame#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #dee2e6;
}

QLabel#logo {
    padding: 20px;
    font-size: 18px;
    font-weight: bold;
    color: #495057;
}

/* Navigation Buttons */
QPushButton#nav_button {
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    color: #495057;
    border-radius: 8px;
    margin: 2px 10px;
}

QPushButton#nav_button:hover {
    background-color: #e9ecef;
    color: #212529;
}

QPushButton#nav_button:pressed {
    background-color: #dee2e6;
}

QPushButton#nav_button_active {
    background-color: #007bff;
    color: white;
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    border-radius: 8px;
    margin: 2px 10px;
}

/* Dropdown Headers */
QPushButton#dropdown_header {
    background-color: #f8f9fa;
    border: none;
    text-align: left;
    padding: 15px 20px;
    font-size: 16px;
    font-weight: 600;
    color: #212529;
    border-radius: 8px;
    margin: 5px 10px;
}

QPushButton#dropdown_header:hover {
    background-color: #e9ecef;
}

/* Theme Toggle */
QPushButton#theme_toggle {
    background-color: #6c757d;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 20px;
    margin: 10px;
    font-size: 12px;
}

QPushButton#theme_toggle:hover {
    background-color: #5a6268;
}

/* Main Content Area */
QScrollArea {
    background-color: #f8f9fa;
    border: none;
}

QWidget#content_widget {
    background-color: #f8f9fa;
}

/* Cards */
QFrame#card {
    background-color: white;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
}

QLabel#card_title {
    font-size: 20px;
    font-weight: 600;
    color: #212529;
    margin-bottom: 10px;
}

QLabel#card_description {
    font-size: 14px;
    color: #6c757d;
    margin-bottom: 20px;
}

/* File Management */
QFrame#file_management {
    background-color: white;
    border: 2px dashed #dee2e6;
    border-radius: 12px;
    padding: 30px;
    margin: 20px;
}

QFrame#file_management[dragActive="true"] {
    border-color: #007bff;
    background-color: #f8f9ff;
}

QListWidget {
    background-color: white;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    color: #212529;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #f1f3f4;
}

QListWidget::item:selected {
    background-color: #e3f2fd;
    color: #1565c0;
}

/* Buttons */
QPushButton {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #0056b3;
}

QPushButton:pressed {
    background-color: #004085;
}

QPushButton:disabled {
    background-color: #6c757d;
    color: #adb5bd;
}

QPushButton#secondary {
    background-color: #6c757d;
}

QPushButton#secondary:hover {
    background-color: #5a6268;
}

QPushButton#danger {
    background-color: #dc3545;
}

QPushButton#danger:hover {
    background-color: #c82333;
}

QPushButton#success {
    background-color: #28a745;
}

QPushButton#success:hover {
    background-color: #218838;
}

/* Input Fields */
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background-color: white;
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: #212529;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #007bff;
    outline: none;
}

QComboBox::drop-down {
    border: none;
    padding: 5px;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzY5NzU4NyIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
    width: 12px;
    height: 8px;
}

/* Status Bar */
QStatusBar {
    background-color: #f8f9fa;
    border-top: 1px solid #dee2e6;
    padding: 5px;
}

QProgressBar {
    background-color: #e9ecef;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    text-align: center;
    font-size: 12px;
}

QProgressBar::chunk {
    background-color: #007bff;
    border-radius: 5px;
}

/* Labels */
QLabel {
    color: #212529;
    font-size: 14px;
}

QLabel#section_title {
    font-size: 18px;
    font-weight: 600;
    color: #212529;
    margin: 15px 0 10px 0;
}

/* Checkboxes and Radio Buttons */
QCheckBox, QRadioButton {
    color: #212529;
    font-size: 14px;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    background-color: white;
    border: 2px solid #ced4da;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #007bff;
    border: 2px solid #007bff;
    border-radius: 4px;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
}

/* Sliders */
QSlider::groove:horizontal {
    background-color: #e9ecef;
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background-color: #007bff;
    border: 2px solid #007bff;
    width: 18px;
    height: 18px;
    border-radius: 11px;
    margin: -8px 0;
}

QSlider::handle:horizontal:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}
"""

# Dark Theme
DARK_THEME = """
QMainWindow {
    background-color: #1a1a1a;
    color: #e0e0e0;
}

/* Sidebar */
QFrame#sidebar {
    background-color: #2d2d2d;
    border-right: 1px solid #404040;
}

QLabel#logo {
    padding: 20px;
    font-size: 18px;
    font-weight: bold;
    color: #e0e0e0;
}

/* Navigation Buttons */
QPushButton#nav_button {
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    color: #b0b0b0;
    border-radius: 8px;
    margin: 2px 10px;
}

QPushButton#nav_button:hover {
    background-color: #404040;
    color: #e0e0e0;
}

QPushButton#nav_button:pressed {
    background-color: #4d4d4d;
}

QPushButton#nav_button_active {
    background-color: #0d7377;
    color: white;
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    border-radius: 8px;
    margin: 2px 10px;
}

/* Dropdown Headers */
QPushButton#dropdown_header {
    background-color: #333333;
    border: none;
    text-align: left;
    padding: 15px 20px;
    font-size: 16px;
    font-weight: 600;
    color: #e0e0e0;
    border-radius: 8px;
    margin: 5px 10px;
}

QPushButton#dropdown_header:hover {
    background-color: #404040;
}

/* Theme Toggle */
QPushButton#theme_toggle {
    background-color: #ffd700;
    color: #1a1a1a;
    border: none;
    padding: 10px;
    border-radius: 20px;
    margin: 10px;
    font-size: 12px;
}

QPushButton#theme_toggle:hover {
    background-color: #ffed4e;
}

/* Main Content Area */
QScrollArea {
    background-color: #1a1a1a;
    border: none;
}

QWidget#content_widget {
    background-color: #1a1a1a;
}

/* Cards */
QFrame#card {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
}

QLabel#card_title {
    font-size: 20px;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 10px;
}

QLabel#card_description {
    font-size: 14px;
    color: #b0b0b0;
    margin-bottom: 20px;
}

/* File Management */
QFrame#file_management {
    background-color: #2d2d2d;
    border: 2px dashed #404040;
    border-radius: 12px;
    padding: 30px;
    margin: 20px;
}

QFrame#file_management[dragActive="true"] {
    border-color: #0d7377;
    background-color: #1a2e2e;
}

QListWidget {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    color: #e0e0e0;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #404040;
}

QListWidget::item:selected {
    background-color: #0d4f52;
    color: #ffffff;
}

/* Buttons */
QPushButton {
    background-color: #0d7377;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #0a5d61;
}

QPushButton:pressed {
    background-color: #08484b;
}

QPushButton:disabled {
    background-color: #4d4d4d;
    color: #808080;
}

QPushButton#secondary {
    background-color: #4d4d4d;
}

QPushButton#secondary:hover {
    background-color: #5d5d5d;
}

QPushButton#danger {
    background-color: #dc3545;
}

QPushButton#danger:hover {
    background-color: #c82333;
}

QPushButton#success {
    background-color: #28a745;
}

QPushButton#success:hover {
    background-color: #218838;
}

/* Input Fields */
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: #e0e0e0;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #0d7377;
    outline: none;
}

QComboBox::drop-down {
    border: none;
    padding: 5px;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iI2IwYjBiMCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
    width: 12px;
    height: 8px;
}

/* Status Bar */
QStatusBar {
    background-color: #1a1a1a;
    border-top: 1px solid #404040;
    padding: 5px;
}

QProgressBar {
    background-color: #404040;
    border: 1px solid #4d4d4d;
    border-radius: 6px;
    text-align: center;
    font-size: 12px;
    color: #e0e0e0;
}

QProgressBar::chunk {
    background-color: #0d7377;
    border-radius: 5px;
}

/* Labels */
QLabel {
    color: #e0e0e0;
    font-size: 14px;
}

QLabel#section_title {
    font-size: 18px;
    font-weight: 600;
    color: #e0e0e0;
    margin: 15px 0 10px 0;
}

/* Checkboxes and Radio Buttons */
QCheckBox, QRadioButton {
    color: #e0e0e0;
    font-size: 14px;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    background-color: #2d2d2d;
    border: 2px solid #404040;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #0d7377;
    border: 2px solid #0d7377;
    border-radius: 4px;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
}

/* Sliders */
QSlider::groove:horizontal {
    background-color: #404040;
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background-color: #0d7377;
    border: 2px solid #0d7377;
    width: 18px;
    height: 18px;
    border-radius: 11px;
    margin: -8px 0;
}

QSlider::handle:horizontal:hover {
    background-color: #0a5d61;
    border-color: #0a5d61;
}
"""
