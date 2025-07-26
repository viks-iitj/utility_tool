"""
Utility Pro - Main Window
Author: Vivek Srivastava
Description: Main application window with sidebar navigation
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QScrollArea, QFrame, QLabel, QPushButton, QStatusBar,
                             QProgressBar, QMessageBox, QSplitter)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon

from ui.styles import LIGHT_THEME, DARK_THEME
from components.file_manager import FileManager
from worker import TaskManager

# Import pages
from pages.pdf_merge import PDFMergePage
from pages.pdf_custom_merge import PDFCustomMergePage
from pages.pdf_split import PDFSplitPage
from pages.pdf_shuffle import PDFShufflePage
from pages.pdf_to_word import PDFToWordPage
from pages.pdf_to_pages import PDFToPagesPage
from pages.pdf_to_image import PDFToImagePage
from pages.image_to_pdf import ImageToPDFPage
from pages.image_tools import ImageToolsPage


class Sidebar(QFrame):
    """Sidebar navigation component"""

    page_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(280)
        self.current_page = None

        self.init_ui()

    def init_ui(self):
        """Initialize sidebar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        self.setup_logo(layout)

        # Navigation
        self.setup_navigation(layout)

        # Spacer
        layout.addStretch()

        # Theme toggle
        self.setup_theme_toggle(layout)

    def setup_logo(self, layout):
        """Setup application logo"""
        logo_label = QLabel("🔧 Utility Pro")
        logo_label.setObjectName("logo")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Try to load custom icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.png")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setText("")

        layout.addWidget(logo_label)

    def setup_navigation(self, layout):
        """Setup navigation menu"""
        # PDF Utility Section
        pdf_header = QPushButton("📄 PDF Utility")
        pdf_header.setObjectName("dropdown_header")
        pdf_header.clicked.connect(lambda: self.toggle_section("pdf"))
        layout.addWidget(pdf_header)

        self.pdf_section = QFrame()
        self.pdf_section.setObjectName("nav_section")
        pdf_layout = QVBoxLayout(self.pdf_section)
        pdf_layout.setContentsMargins(0, 0, 0, 0)
        pdf_layout.setSpacing(2)

        pdf_pages = [
            ("Merge PDF", "pdf_merge"),
            ("Custom Merge", "pdf_custom_merge"),
            ("Split PDF", "pdf_split"),
            ("Shuffle Pages", "pdf_shuffle"),
            ("Convert to Word", "pdf_to_word"),
            ("Convert to Pages", "pdf_to_pages"),
            ("PDF to Image", "pdf_to_image"),
        ]

        self.pdf_buttons = {}
        for title, page_id in pdf_pages:
            btn = QPushButton(title)
            btn.setObjectName("nav_button")
            btn.clicked.connect(lambda checked, p=page_id: self.navigate_to_page(p))
            pdf_layout.addWidget(btn)
            self.pdf_buttons[page_id] = btn

        layout.addWidget(self.pdf_section)

        # Image Utility Section
        image_header = QPushButton("🖼️ Image Utility")
        image_header.setObjectName("dropdown_header")
        image_header.clicked.connect(lambda: self.toggle_section("image"))
        layout.addWidget(image_header)

        self.image_section = QFrame()
        self.image_section.setObjectName("nav_section")
        image_layout = QVBoxLayout(self.image_section)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(2)

        image_pages = [
            ("Image to PDF", "image_to_pdf"),
            ("Image Tools", "image_tools"),
        ]

        self.image_buttons = {}
        for title, page_id in image_pages:
            btn = QPushButton(title)
            btn.setObjectName("nav_button")
            btn.clicked.connect(lambda checked, p=page_id: self.navigate_to_page(p))
            image_layout.addWidget(btn)
            self.image_buttons[page_id] = btn

        layout.addWidget(self.image_section)

        # Initially show all sections
        self.pdf_section.setVisible(True)
        self.image_section.setVisible(True)

    def setup_theme_toggle(self, layout):
        """Setup theme toggle button"""
        self.theme_toggle = QPushButton("🌙 Dark Mode")
        self.theme_toggle.setObjectName("theme_toggle")
        layout.addWidget(self.theme_toggle)

    def toggle_section(self, section):
        """Toggle visibility of navigation sections"""
        if section == "pdf":
            self.pdf_section.setVisible(not self.pdf_section.isVisible())
        elif section == "image":
            self.image_section.setVisible(not self.image_section.isVisible())

    def navigate_to_page(self, page_id):
        """Navigate to a specific page"""
        # Update button states
        self.update_active_button(page_id)

        # Emit signal
        self.page_requested.emit(page_id)
        self.current_page = page_id

    def update_active_button(self, active_page):
        """Update active button styling"""
        all_buttons = {**self.pdf_buttons, **self.image_buttons}

        for page_id, button in all_buttons.items():
            if page_id == active_page:
                button.setObjectName("nav_button_active")
            else:
                button.setObjectName("nav_button")
            button.style().unpolish(button)
            button.style().polish(button)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.settings = QSettings("UtilityPro", "Settings")
        self.is_dark_mode = self.settings.value("dark_mode", False, type=bool)

        # Initialize task manager
        self.task_manager = TaskManager()
        self.setup_task_manager()

        # Initialize file manager
        self.file_manager = FileManager()

        # Pages dictionary
        self.pages = {}

        self.init_ui()
        self.apply_theme()

        # Navigate to first page
        self.sidebar.navigate_to_page("pdf_merge")

    def init_ui(self):
        """Initialize main UI"""
        self.setWindowTitle("Utility Pro - Advanced PDF & Image Tools")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_requested.connect(self.navigate_to_page)
        self.sidebar.theme_toggle.clicked.connect(self.toggle_theme)
        splitter.addWidget(self.sidebar)

        # Main content area
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.content_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.content_widget = QWidget()
        self.content_widget.setObjectName("content_widget")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.content_area.setWidget(self.content_widget)
        splitter.addWidget(self.content_area)

        # Set splitter proportions
        splitter.setSizes([280, 1120])
        splitter.setCollapsible(0, False)

        # Status bar
        self.setup_status_bar()

        # Initialize pages
        self.init_pages()

    def setup_status_bar(self):
        """Setup status bar with progress indicator"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)

        # Abort button
        self.abort_button = QPushButton("Abort")
        self.abort_button.setObjectName("danger")
        self.abort_button.setVisible(False)
        self.abort_button.clicked.connect(self.abort_current_task)

        self.status_bar.addPermanentWidget(self.progress_bar)
        self.status_bar.addPermanentWidget(self.abort_button)

        # Initial status
        self.status_bar.showMessage("Ready")

    def init_pages(self):
        """Initialize all application pages"""
        self.pages = {
            "pdf_merge": PDFMergePage(self.file_manager, self.task_manager),
            "pdf_custom_merge": PDFCustomMergePage(self.file_manager, self.task_manager),
            "pdf_split": PDFSplitPage(self.file_manager, self.task_manager),
            "pdf_shuffle": PDFShufflePage(self.file_manager, self.task_manager),
            "pdf_to_word": PDFToWordPage(self.file_manager, self.task_manager),
            "pdf_to_pages": PDFToPagesPage(self.file_manager, self.task_manager),
            "pdf_to_image": PDFToImagePage(self.file_manager, self.task_manager),
            "image_to_pdf": ImageToPDFPage(self.file_manager, self.task_manager),
            "image_tools": ImageToolsPage(self.file_manager, self.task_manager),
        }

    def navigate_to_page(self, page_id):
        """Navigate to a specific page"""
        # Clear current content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        # Add new page
        if page_id in self.pages:
            self.content_layout.addWidget(self.pages[page_id])

            # Update window title
            page_titles = {
                "pdf_merge": "Merge PDF Files",
                "pdf_custom_merge": "Custom PDF Merge",
                "pdf_split": "Split PDF Files",
                "pdf_shuffle": "Shuffle PDF Pages",
                "pdf_to_word": "Convert PDF to Word",
                "pdf_to_pages": "Convert PDF to Pages",
                "pdf_to_image": "Convert PDF to Images",
                "image_to_pdf": "Convert Images to PDF",
                "image_tools": "Image Editing Tools",
            }

            title = page_titles.get(page_id, "Utility Pro")
            self.setWindowTitle(f"Utility Pro - {title}")

    def setup_task_manager(self):
        """Setup task manager connections"""
        self.task_manager.task_started.connect(self.on_task_started)
        self.task_manager.task_finished.connect(self.on_task_finished)
        self.task_manager.task_progress.connect(self.on_task_progress)
        self.task_manager.task_error.connect(self.on_task_error)

    def on_task_started(self, operation):
        """Handle task start"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.abort_button.setVisible(True)
        self.status_bar.showMessage(f"Processing: {operation}")

    def on_task_finished(self, success, message):
        """Handle task completion"""
        self.progress_bar.setVisible(False)
        self.abort_button.setVisible(False)

        if success:
            self.status_bar.showMessage(f"✓ {message}", 5000)
            QMessageBox.information(self, "Success", message)
        else:
            self.status_bar.showMessage(f"✗ {message}", 5000)
            QMessageBox.warning(self, "Error", message)

    def on_task_progress(self, value):
        """Handle progress update"""
        self.progress_bar.setValue(value)

    def on_task_error(self, error_message):
        """Handle task error"""
        self.progress_bar.setVisible(False)
        self.abort_button.setVisible(False)
        self.status_bar.showMessage(f"✗ Error: {error_message}", 5000)
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_message}")

    def abort_current_task(self):
        """Abort the currently running task"""
        self.task_manager.cancel_current_task()
        self.progress_bar.setVisible(False)
        self.abort_button.setVisible(False)
        self.status_bar.showMessage("Task aborted", 3000)

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_mode = not self.is_dark_mode
        self.settings.setValue("dark_mode", self.is_dark_mode)
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme"""
        if self.is_dark_mode:
            self.setStyleSheet(DARK_THEME)
            self.sidebar.theme_toggle.setText("☀️ Light Mode")
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.sidebar.theme_toggle.setText("🌙 Dark Mode")

        # Force style refresh
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def closeEvent(self, event):
        """Handle application close"""
        # Cancel any running tasks
        if self.task_manager.is_running:
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "A task is currently running. Do you want to cancel it and exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.task_manager.cancel_current_task()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()