"""
Utility Pro - PDF Split Page
Author: Vivek Srivastava
Description: Split PDF files into individual pages
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt


class PDFSplitPage(QWidget):
    """Page for splitting PDF files into individual pages"""

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
        header_label = QLabel("Split PDF Files")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        description_label = QLabel("Split PDF files into individual pages. Each page will be saved as a separate PDF file in your chosen directory.")
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

        description = QLabel("Add PDF files to split. Each file will be split into individual pages.")
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

        title = QLabel("⚙️ Split Options")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Configure split settings and choose output directory.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Output directory selection
        output_frame = QFrame()
        output_layout = QVBoxLayout(output_frame)

        output_label = QLabel("📁 Output Directory:")
        output_label.setStyleSheet("font-weight: 600; margin-bottom: 5px;")
        output_layout.addWidget(output_label)

        dir_layout = QHBoxLayout()

        self.output_path_label = QLabel("No directory selected")
        self.output_path_label.setStyleSheet("color: #6c757d; font-size: 12px; border: 1px solid #dee2e6; padding: 8px; border-radius: 4px; background-color: #f8f9fa;")
        self.output_path_label.setWordWrap(True)
        dir_layout.addWidget(self.output_path_label, 1)

        self.browse_button = QPushButton("📁 Browse")
        self.browse_button.setObjectName("secondary")
        self.browse_button.clicked.connect(self.browse_output_directory)
        dir_layout.addWidget(self.browse_button)

        output_layout.addLayout(dir_layout)
        layout.addWidget(output_frame)

        # Split info
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)

        info_label = QLabel("ℹ️ Split Information")
        info_label.setStyleSheet("font-weight: 600; margin-bottom: 10px;")
        info_layout.addWidget(info_label)

        self.split_info = QLabel("Select PDF files to see split information")
        self.split_info.setStyleSheet("color: #6c757d; font-size: 12px;")
        self.split_info.setWordWrap(True)
        info_layout.addWidget(self.split_info)

        layout.addWidget(info_frame)

        # Naming convention info
        naming_frame = QFrame()
        naming_layout = QVBoxLayout(naming_frame)

        naming_label = QLabel("📝 File Naming:")
        naming_label.setStyleSheet("font-weight: 600; margin-bottom: 5px;")
        naming_layout.addWidget(naming_label)

        naming_info = QLabel("Files will be named as:\n• filename_page_1.pdf\n• filename_page_2.pdf\n• etc.")
        naming_info.setStyleSheet("color: #6c757d; font-size: 12px;")
        naming_layout.addWidget(naming_info)

        layout.addWidget(naming_frame)

        layout.addStretch()

        # Action buttons
        button_layout = QHBoxLayout()

        self.split_button = QPushButton("✂️ Split PDFs")
        self.split_button.setObjectName("success")
        self.split_button.clicked.connect(self.split_pdfs)
        self.split_button.setEnabled(False)
        button_layout.addWidget(self.split_button)

        layout.addLayout(button_layout)

        return card

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for PDF files
        self.file_manager.set_accepted_extensions(['.pdf'], "PDF documents (*.pdf)")
        self.file_manager.files_changed.connect(self.update_split_info)

        # Initialize output directory to Documents
        self.output_directory = os.path.expanduser("~/Documents")
        self.output_path_label.setText(self.output_directory)

    def browse_output_directory(self):
        """Browse for output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.output_directory
        )

        if directory:
            self.output_directory = directory
            self.output_path_label.setText(directory)
            self.update_split_button_state()

    def update_split_info(self):
        """Update split information display"""
        files = self.file_manager.get_pdf_files()
        file_count = len(files)

        if file_count == 0:
            self.split_info.setText("Select PDF files to see split information")
        else:
            # This would require reading PDF files to get page counts
            # For now, show file count
            if file_count == 1:
                self.split_info.setText(f"✓ Ready to split 1 PDF file\nEach page will be saved as a separate PDF")
            else:
                self.split_info.setText(f"✓ Ready to split {file_count} PDF files\nEach page from each file will be saved as a separate PDF")

        self.update_split_button_state()

    def update_split_button_state(self):
        """Update split button enabled state"""
        has_files = len(self.file_manager.get_pdf_files()) > 0
        has_output_dir = hasattr(self, 'output_directory') and self.output_directory

        self.split_button.setEnabled(has_files and has_output_dir)

    def split_pdfs(self):
        """Start PDF split process"""
        files = self.file_manager.get_pdf_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select PDF files to split.")
            return

        if not hasattr(self, 'output_directory') or not self.output_directory:
            QMessageBox.warning(self, "Error", "Please select an output directory.")
            return

        # Confirm action
        file_count = len(files)
        reply = QMessageBox.question(
            self,
            "Confirm Split",
            f"This will split {file_count} PDF file(s) into individual pages.\n\n"
            f"Output directory: {self.output_directory}\n\n"
            "Do you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Start split task
        success = self.task_manager.start_pdf_task(
            "split",
            input_files=files,
            output_dir=self.output_directory
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")