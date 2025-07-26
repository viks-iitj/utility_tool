"""
Utility Pro - PDF to Image Page
Author: Vivek Srivastava
Description: Convert PDF pages to various image formats
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QComboBox, QFileDialog,
                             QMessageBox, QButtonGroup, QRadioButton)
from PyQt6.QtCore import Qt


class PDFToImagePage(QWidget):
    """Page for converting PDF to images"""

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
        header_label = QLabel("Convert PDF to Images")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        description_label = QLabel("Export pages from PDF files into various image formats with customizable quality settings.")
        description_label.setObjectName("card_description")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Main content grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # File Management Card
        file_card = self.create_file_management_card()
        grid_layout.addWidget(file_card, 0, 0)

        # Format Options Card
        format_card = self.create_format_options_card()
        grid_layout.addWidget(format_card, 0, 1)

        # Quality Settings Card (spans both columns)
        quality_card = self.create_quality_settings_card()
        grid_layout.addWidget(quality_card, 1, 0, 1, 2)

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

        description = QLabel("Add PDF files to convert to images. Each page will be exported as a separate image file.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Add file manager
        layout.addWidget(self.file_manager)

        return card

    def create_format_options_card(self):
        """Create format options card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("🖼️ Output Format")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Choose the output image format and configure settings.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Format selection
        format_label = QLabel("Image Format:")
        format_label.setStyleSheet("font-weight: 600; margin-bottom: 5px;")
        layout.addWidget(format_label)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG", "TIFF", "WebP", "BMP"])
        self.format_combo.setCurrentText("PNG")
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        layout.addWidget(self.format_combo)

        # Format info
        self.format_info = QLabel()
        self.format_info.setStyleSheet("color: #6c757d; font-size: 11px; margin-top: 5px;")
        self.format_info.setWordWrap(True)
        layout.addWidget(self.format_info)

        # Output directory
        layout.addWidget(QLabel())  # Spacer

        output_label = QLabel("📁 Output Directory:")
        output_label.setStyleSheet("font-weight: 600; margin-bottom: 5px;")
        layout.addWidget(output_label)

        dir_layout = QHBoxLayout()

        self.output_path_label = QLabel("No directory selected")
        self.output_path_label.setStyleSheet("color: #6c757d; font-size: 11px; border: 1px solid #dee2e6; padding: 8px; border-radius: 4px; background-color: #f8f9fa;")
        self.output_path_label.setWordWrap(True)
        dir_layout.addWidget(self.output_path_label, 1)

        self.browse_button = QPushButton("📁 Browse")
        self.browse_button.setObjectName("secondary")
        self.browse_button.clicked.connect(self.browse_output_directory)
        dir_layout.addWidget(self.browse_button)

        layout.addLayout(dir_layout)

        layout.addStretch()

        return card

    def create_quality_settings_card(self):
        """Create quality settings card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("⚙️ Quality Settings")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Choose quality preset and preview the output resolution.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Quality presets
        quality_layout = QHBoxLayout()

        # Quality selection
        preset_frame = QFrame()
        preset_layout = QVBoxLayout(preset_frame)

        preset_label = QLabel("Quality Preset:")
        preset_label.setStyleSheet("font-weight: 600; margin-bottom: 10px;")
        preset_layout.addWidget(preset_label)

        self.quality_group = QButtonGroup(self)

        self.web_radio = QRadioButton("🌐 Web (150 DPI)")
        self.web_radio.setChecked(True)
        self.quality_group.addButton(self.web_radio, 0)
        preset_layout.addWidget(self.web_radio)

        web_desc = QLabel("Optimized for web use and email")
        web_desc.setStyleSheet("color: #6c757d; font-size: 11px; margin-left: 20px; margin-bottom: 10px;")
        preset_layout.addWidget(web_desc)

        self.print_radio = QRadioButton("🖨️ Print (300 DPI)")
        self.quality_group.addButton(self.print_radio, 1)
        preset_layout.addWidget(self.print_radio)

        print_desc = QLabel("High quality for printing")
        print_desc.setStyleSheet("color: #6c757d; font-size: 11px; margin-left: 20px; margin-bottom: 10px;")
        preset_layout.addWidget(print_desc)

        self.archive_radio = QRadioButton("📚 Archive (600 DPI)")
        self.quality_group.addButton(self.archive_radio, 2)
        preset_layout.addWidget(self.archive_radio)

        archive_desc = QLabel("Maximum quality for archival purposes")
        archive_desc.setStyleSheet("color: #6c757d; font-size: 11px; margin-left: 20px;")
        preset_layout.addWidget(archive_desc)

        quality_layout.addWidget(preset_frame)

        # Live preview
        preview_frame = QFrame()
        preview_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px;")
        preview_layout = QVBoxLayout(preview_frame)

        preview_title = QLabel("📊 Output Preview")
        preview_title.setStyleSheet("font-weight: 600; margin-bottom: 10px;")
        preview_layout.addWidget(preview_title)

        self.resolution_label = QLabel()
        self.resolution_label.setStyleSheet("font-size: 14px; font-weight: 500; margin-bottom: 5px;")
        preview_layout.addWidget(self.resolution_label)

        self.file_size_label = QLabel()
        self.file_size_label.setStyleSheet("color: #6c757d; font-size: 12px; margin-bottom: 10px;")
        preview_layout.addWidget(self.file_size_label)

        self.conversion_info = QLabel("Select PDF files to see conversion details")
        self.conversion_info.setStyleSheet("color: #6c757d; font-size: 12px;")
        self.conversion_info.setWordWrap(True)
        preview_layout.addWidget(self.conversion_info)

        quality_layout.addWidget(preview_frame)

        layout.addLayout(quality_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.convert_button = QPushButton("🖼️ Convert to Images")
        self.convert_button.setObjectName("success")
        self.convert_button.clicked.connect(self.convert_to_images)
        self.convert_button.setEnabled(False)
        button_layout.addWidget(self.convert_button)

        layout.addLayout(button_layout)

        return card

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for PDF files
        self.file_manager.set_accepted_extensions(['.pdf'], "PDF documents (*.pdf)")
        self.file_manager.files_changed.connect(self.update_conversion_info)

        # Connect quality radio buttons
        self.quality_group.buttonClicked.connect(self.update_preview)

        # Initialize output directory and format info
        self.output_directory = os.path.expanduser("~/Documents")
        self.output_path_label.setText(self.output_directory)
        self.update_format_info()
        self.update_preview()

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
            self.update_convert_button_state()

    def on_format_changed(self):
        """Handle format selection change"""
        self.update_format_info()
        self.update_preview()

    def update_format_info(self):
        """Update format information"""
        format_info = {
            "PNG": "Lossless compression, supports transparency, larger file size",
            "JPEG": "Lossy compression, smaller file size, no transparency",
            "TIFF": "High quality, lossless, large file size, professional use",
            "WebP": "Modern format, good compression, smaller than PNG",
            "BMP": "Uncompressed, very large file size, maximum quality"
        }

        current_format = self.format_combo.currentText()
        self.format_info.setText(format_info.get(current_format, ""))

    def update_preview(self):
        """Update the live preview of output settings"""
        # Get current quality setting
        if self.web_radio.isChecked():
            dpi = 150
            quality_name = "Web"
        elif self.print_radio.isChecked():
            dpi = 300
            quality_name = "Print"
        else:
            dpi = 600
            quality_name = "Archive"

        # Calculate resolution for standard A4 page (8.27 × 11.69 inches)
        width_px = int(8.27 * dpi)
        height_px = int(11.69 * dpi)

        self.resolution_label.setText(f"Resolution: {width_px} × {height_px} pixels")

        # Estimate file size (rough approximation)
        format_name = self.format_combo.currentText()
        if format_name == "PNG":
            size_mb = (width_px * height_px * 3) / (1024 * 1024)  # RGB
        elif format_name == "JPEG":
            size_mb = (width_px * height_px * 0.5) / (1024 * 1024)  # Compressed
        elif format_name == "TIFF":
            size_mb = (width_px * height_px * 3) / (1024 * 1024)  # RGB
        elif format_name == "WebP":
            size_mb = (width_px * height_px * 0.7) / (1024 * 1024)  # Better compression
        else:  # BMP
            size_mb = (width_px * height_px * 3) / (1024 * 1024)  # Uncompressed

        self.file_size_label.setText(f"Estimated size per page: {size_mb:.1f} MB ({quality_name} quality)")

        self.update_conversion_info()

    def update_conversion_info(self):
        """Update conversion information display"""
        files = self.file_manager.get_pdf_files()
        file_count = len(files)

        if file_count == 0:
            self.conversion_info.setText("Select PDF files to see conversion details")
        else:
            format_name = self.format_combo.currentText()
            # This would ideally count total pages by reading PDFs
            # For now, estimate based on file count
            estimated_pages = file_count * 5  # Assume 5 pages per PDF as estimate

            self.conversion_info.setText(
                f"✓ Ready to convert {file_count} PDF file(s)\n"
                f"Output format: {format_name}\n"
                f"Estimated output: ~{estimated_pages} image files"
            )

        self.update_convert_button_state()

    def update_convert_button_state(self):
        """Update convert button enabled state"""
        has_files = len(self.file_manager.get_pdf_files()) > 0
        has_output_dir = hasattr(self, 'output_directory') and self.output_directory

        self.convert_button.setEnabled(has_files and has_output_dir)

    def convert_to_images(self):
        """Start PDF to image conversion process"""
        files = self.file_manager.get_pdf_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select PDF files to convert.")
            return

        if not hasattr(self, 'output_directory') or not self.output_directory:
            QMessageBox.warning(self, "Error", "Please select an output directory.")
            return

        # Get settings
        format_name = self.format_combo.currentText()

        if self.web_radio.isChecked():
            quality_preset = "Web"
        elif self.print_radio.isChecked():
            quality_preset = "Print"
        else:
            quality_preset = "Archive"

        # Confirm action
        reply = QMessageBox.question(
            self,
            "Confirm Conversion",
            f"This will convert PDF pages to {format_name} images with {quality_preset} quality.\n\n"
            f"Output directory: {self.output_directory}\n\n"
            f"Files will be named as: filename_page_1.{format_name.lower()}\n\n"
            "Do you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Start conversion task
        success = self.task_manager.start_pdf_task(
            "pdf_to_images",
            input_files=files,
            output_dir=self.output_directory,
            format=format_name,
            quality_preset=quality_preset
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")