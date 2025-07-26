"""
Utility Pro - PDF Merge Page
Author: Vivek Srivastava
Description: Merge multiple PDF files into one
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt


class PDFMergePage(QWidget):
    """Page for merging PDF files"""

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
        header_label = QLabel("Merge PDF Files")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        description_label = QLabel("Combine multiple PDF files into a single document. Files will be merged in the order they appear in the list.")
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

        description = QLabel("Add PDF files to merge. You can drag and drop files or use the upload button.")
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

        title = QLabel("⚙️ Merge Options")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Configure merge settings and start the process.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Merge info
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)

        info_label = QLabel("ℹ️ Merge Information")
        info_label.setStyleSheet("font-weight: 600; margin-bottom: 10px;")
        info_layout.addWidget(info_label)

        self.merge_info = QLabel("Select PDF files to see merge information")
        self.merge_info.setStyleSheet("color: #6c757d; font-size: 12px;")
        self.merge_info.setWordWrap(True)
        info_layout.addWidget(self.merge_info)

        layout.addWidget(info_frame)

        layout.addStretch()

        # Action buttons
        button_layout = QHBoxLayout()

        self.merge_button = QPushButton("🔗 Merge PDFs")
        self.merge_button.setObjectName("success")
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.merge_button.setEnabled(False)
        button_layout.addWidget(self.merge_button)

        layout.addLayout(button_layout)

        return card

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for PDF files
        self.file_manager.set_accepted_extensions(['.pdf'], "PDF documents (*.pdf)")
        self.file_manager.files_changed.connect(self.update_merge_info)

    def update_merge_info(self):
        """Update merge information display"""
        files = self.file_manager.get_pdf_files()
        file_count = len(files)

        if file_count == 0:
            self.merge_info.setText("Select PDF files to see merge information")
            self.merge_button.setEnabled(False)
        elif file_count == 1:
            self.merge_info.setText("⚠️ At least 2 PDF files are required for merging")
            self.merge_button.setEnabled(False)
        else:
            # Calculate total pages (this would require reading each PDF)
            self.merge_info.setText(
                f"✓ Ready to merge {file_count} PDF files\n"
                f"Files will be combined in the order shown above"
            )
            self.merge_button.setEnabled(True)

    def merge_pdfs(self):
        """Start PDF merge process"""
        files = self.file_manager.get_pdf_files()

        if len(files) < 2:
            QMessageBox.warning(self, "Error", "Please select at least 2 PDF files to merge.")
            return

        # Get output file path
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Merged PDF",
            "merged_document.pdf",
            "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        # Start merge task
        success = self.task_manager.start_pdf_task(
            "merge",
            input_files=files,
            output_path=output_path
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")