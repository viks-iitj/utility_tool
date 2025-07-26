"""
Utility Pro - PDF to Pages Page
Author: Vivek Srivastava
Description: Convert PDF files to Apple Pages documents (macOS only)
"""

import os
import platform
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt


class PDFToPagesPage(QWidget):
    """Page for converting PDF to Apple Pages documents"""

    def __init__(self, file_manager, task_manager):
        super().__init__()
        self.file_manager = file_manager
        self.task_manager = task_manager

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Page header
        header_label = QLabel("Convert PDF to Pages")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        # Check if running on macOS
        if platform.system() != "Darwin":
            description_label = QLabel("⚠️ This feature is only available on macOS systems with Apple Pages installed.")
            description_label.setObjectName("card_description")
            description_label.setStyleSheet("color: #dc3545; font-weight: 600;")
        else:
            description_label = QLabel("Convert PDF files to Apple Pages documents (.pages). Multiple PDFs will be merged into a single Pages document with OCR support for editable text.")

        description_label.setObjectName("card_description")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Main content grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # File Management Card
        file_card = self.create_file_management_card()
        grid_layout.addWidget(file_card, 0, 0)

        # Options Card
        options_card = self.create_options_card()
        grid_layout.addWidget(options_card, 0, 1)

        layout.addLayout(grid_layout)
        layout.addStretch()

    def create_file_management_card(self):
        """Create file management card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("📄 File Selection")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Add PDF files to convert to Apple Pages format. Multiple files will be merged into one document.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Add file manager
        layout.addWidget(self.file_manager)

        return card

    def create_options_card(self):
        """Create options and action card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("⚙️ Conversion Options")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Configure conversion settings and start the process.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # System requirements
        req_frame = QFrame()
        req_layout = QVBoxLayout(req_frame)

        req_label = QLabel("📋 Requirements:")
        req_label.setStyleSheet("font-weight: 600; margin-bottom: 5px;")
        req_layout.addWidget(req_label)

        if platform.system() == "Darwin":
            req_info = QLabel("""
✓ macOS system detected
• Apple Pages app must be installed
• OCR will make text in images editable
• Supports complex layouts and graphics
• Native .pages format output
            """)
            req_info.setStyleSheet("color: #28a745; font-size: 12px; margin-bottom: 15px;")
        else:
            req_info = QLabel("""
❌ macOS required for this feature
• This conversion requires Apple Pages
• Feature not available on current system
• Use 'Convert to Word' as alternative
            """)
            req_info.setStyleSheet("color: #dc3545; font-size: 12px; margin-bottom: 15px;")

        req_layout.addWidget(req_info)
        layout.addWidget(req_frame)

        # Conversion info
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)

        info_label = QLabel("ℹ️ Conversion Information")
        info_label.setStyleSheet("font-weight: 600; margin-bottom: 10px;")
        info_layout.addWidget(info_label)

        self.conversion_info = QLabel("Select PDF files to see conversion information")
        self.conversion_info.setStyleSheet("color: #6c757d; font-size: 12px;")
        self.conversion_info.setWordWrap(True)
        info_layout.addWidget(self.conversion_info)

        layout.addWidget(info_frame)

        layout.addStretch()

        # Action buttons
        button_layout = QHBoxLayout()

        self.convert_button = QPushButton("📄 Convert to Pages")
        self.convert_button.setObjectName("success")
        self.convert_button.clicked.connect(self.convert_to_pages)
        self.convert_button.setEnabled(False)

        # Disable button if not on macOS
        if platform.system() != "Darwin":
            self.convert_button.setEnabled(False)
            self.convert_button.setText("❌ macOS Required")
            self.convert_button.setObjectName("secondary")

        button_layout.addWidget(self.convert_button)

        layout.addLayout(button_layout)

        return card

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for PDF files
        self.file_manager.set_accepted_extensions(['.pdf'], "PDF documents (*.pdf)")
        self.file_manager.files_changed.connect(self.update_conversion_info)

    def update_conversion_info(self):
        """Update conversion information display"""
        files = self.file_manager.get_pdf_files()
        file_count = len(files)

        if platform.system() != "Darwin":
            self.conversion_info.setText("❌ Pages conversion is only available on macOS")
            return

        if file_count == 0:
            self.conversion_info.setText("Select PDF files to see conversion information")
            self.convert_button.setEnabled(False)
        elif file_count == 1:
            file_name = os.path.basename(files[0])
            self.conversion_info.setText(f"✓ Ready to convert 1 PDF file to Pages\nOutput: {os.path.splitext(file_name)[0]}.pages")
            self.convert_button.setEnabled(True)
        else:
            self.conversion_info.setText(f"✓ Ready to convert {file_count} PDF files\nFiles will be merged into a single Pages document")
            self.convert_button.setEnabled(True)

    def convert_to_pages(self):
        """Start PDF to Pages conversion process"""
        if platform.system() != "Darwin":
            QMessageBox.warning(self, "Error", "This feature is only available on macOS systems.")
            return

        files = self.file_manager.get_pdf_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select PDF files to convert.")
            return

        # Get output file path
        if len(files) == 1:
            default_name = f"{os.path.splitext(os.path.basename(files[0]))[0]}.pages"
        else:
            default_name = "converted_document.pages"

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Pages Document",
            default_name,
            "Pages Documents (*.pages)"
        )

        if not output_path:
            return

        # Show conversion warning
        reply = QMessageBox.question(
            self,
            "Confirm Conversion",
            "PDF to Pages conversion will:\n\n"
            "• Launch Apple Pages application\n"
            "• Merge PDFs if multiple files selected\n"
            "• Apply OCR to make text in images editable\n"
            "• May take several minutes for large files\n\n"
            "Make sure Apple Pages is installed and you have sufficient disk space.\n\n"
            "Do you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Start conversion task
        success = self.task_manager.start_pdf_task(
            "convert_to_pages",
            input_files=files,
            output_path=output_path
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")