"""
Utility Pro - Image to PDF Page
Author: Vivek Srivastava
Description: Convert images to PDF documents
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QFileDialog, QMessageBox,
                             QCheckBox, QComboBox)
from PyQt6.QtCore import Qt


class ImageToPDFPage(QWidget):
    """Page for converting images to PDF"""

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
        header_label = QLabel("Convert Images to PDF")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        description_label = QLabel("Create a single PDF document from multiple image files. Images will be added as separate pages in the order they appear.")
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

        title = QLabel("🖼️ Image Selection")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Add image files to convert to PDF. Each image will become a separate page in the PDF.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Supported formats info
        formats_label = QLabel("📋 Supported Formats:")
        formats_label.setStyleSheet("font-weight: 600; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(formats_label)

        formats_info = QLabel("PNG, JPEG, JPG, TIFF, BMP, WebP, GIF")
        formats_info.setStyleSheet("color: #6c757d; font-size: 12px; margin-bottom: 15px;")
        layout.addWidget(formats_info)

        # Add file manager
        layout.addWidget(self.file_manager)

        return card

    def create_options_card(self):
        """Create options and action card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("⚙️ PDF Options")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Configure PDF creation settings.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Page orientation
        orientation_frame = QFrame()
        orientation_layout = QVBoxLayout(orientation_frame)

        orientation_label = QLabel("📄 Page Orientation:")
        orientation_label.setStyleSheet("font-weight: 600; margin-bottom: 5px;")
        orientation_layout.addWidget(orientation_label)

        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems(["Auto (fit to image)", "Portrait", "Landscape"])
        self.orientation_combo.setCurrentText("Auto (fit to image)")
        orientation_layout.addWidget(self.orientation_combo)

        orientation_desc = QLabel("Auto adjusts orientation based on image dimensions")
        orientation_desc.setStyleSheet("color: #6c757d; font-size: 11px; margin-top: 2px;")
        orientation_layout.addWidget(orientation_desc)

        layout.addWidget(orientation_frame)

        # Image fitting
        fitting_frame = QFrame()
        fitting_layout = QVBoxLayout(fitting_frame)

        fitting_label = QLabel("🖼️ Image Fitting:")
        fitting_label.setStyleSheet("font-weight: 600; margin-bottom: 5px; margin-top: 15px;")
        fitting_layout.addWidget(fitting_label)

        self.fit_combo = QComboBox()
        self.fit_combo.addItems(["Fit to page", "Fill page", "Actual size"])
        self.fit_combo.setCurrentText("Fit to page")
        fitting_layout.addWidget(self.fit_combo)

        fitting_desc = QLabel("Fit to page maintains aspect ratio with margins")
        fitting_desc.setStyleSheet("color: #6c757d; font-size: 11px; margin-top: 2px;")
        fitting_layout.addWidget(fitting_desc)

        layout.addWidget(fitting_frame)

        # Quality settings
        quality_frame = QFrame()
        quality_layout = QVBoxLayout(quality_frame)

        quality_label = QLabel("📊 Image Quality:")
        quality_label.setStyleSheet("font-weight: 600; margin-bottom: 5px; margin-top: 15px;")
        quality_layout.addWidget(quality_label)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["High (no compression)", "Medium (balanced)", "Low (smaller file)"])
        self.quality_combo.setCurrentText("High (no compression)")
        quality_layout.addWidget(self.quality_combo)

        layout.addWidget(quality_frame)

        # Conversion info
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)

        info_label = QLabel("ℹ️ Conversion Information")
        info_label.setStyleSheet("font-weight: 600; margin-bottom: 10px; margin-top: 15px;")
        info_layout.addWidget(info_label)

        self.conversion_info = QLabel("Select image files to see conversion information")
        self.conversion_info.setStyleSheet("color: #6c757d; font-size: 12px;")
        self.conversion_info.setWordWrap(True)
        info_layout.addWidget(self.conversion_info)

        layout.addWidget(info_frame)

        layout.addStretch()

        # Action buttons
        button_layout = QHBoxLayout()

        self.convert_button = QPushButton("📄 Create PDF")
        self.convert_button.setObjectName("success")
        self.convert_button.clicked.connect(self.create_pdf)
        self.convert_button.setEnabled(False)
        button_layout.addWidget(self.convert_button)

        layout.addLayout(button_layout)

        return card

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp', '.gif']
        self.file_manager.set_accepted_extensions(
            image_extensions,
            "Image files (PNG, JPEG, TIFF, BMP, WebP, GIF)"
        )
        self.file_manager.files_changed.connect(self.update_conversion_info)

        # Connect combo box changes
        self.fit_combo.currentTextChanged.connect(self.update_fitting_description)

    def update_fitting_description(self):
        """Update fitting method description"""
        descriptions = {
            "Fit to page": "Maintains aspect ratio with margins",
            "Fill page": "Scales to fill entire page, may crop image",
            "Actual size": "Uses original image dimensions"
        }

        current_fit = self.fit_combo.currentText()
        # Update the description label if needed
        # For now, we'll handle this in the UI

    def update_conversion_info(self):
        """Update conversion information display"""
        files = self.file_manager.get_image_files()
        file_count = len(files)

        if file_count == 0:
            self.conversion_info.setText("Select image files to see conversion information")
            self.convert_button.setEnabled(False)
        elif file_count == 1:
            file_name = os.path.basename(files[0])
            self.conversion_info.setText(f"✓ Ready to create PDF from 1 image\nSource: {file_name}")
            self.convert_button.setEnabled(True)
        else:
            # Calculate estimated PDF size
            total_size = sum(os.path.getsize(f) for f in files if os.path.exists(f))
            size_mb = total_size / (1024 * 1024)

            self.conversion_info.setText(
                f"✓ Ready to create PDF from {file_count} images\n"
                f"Total source size: {size_mb:.1f} MB\n"
                f"Each image will be a separate page"
            )
            self.convert_button.setEnabled(True)

    def create_pdf(self):
        """Start image to PDF conversion process"""
        files = self.file_manager.get_image_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select image files to convert.")
            return

        # Get output file path
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Document",
            "images_document.pdf",
            "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        # Get settings
        orientation = self.orientation_combo.currentText()
        fitting = self.fit_combo.currentText()
        quality = self.quality_combo.currentText()

        # Show conversion info
        reply = QMessageBox.question(
            self,
            "Confirm Conversion",
            f"This will create a PDF with {len(files)} pages from your selected images.\n\n"
            f"Settings:\n"
            f"• Orientation: {orientation}\n"
            f"• Image fitting: {fitting}\n"
            f"• Quality: {quality}\n\n"
            f"Output: {os.path.basename(output_path)}\n\n"
            "Do you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Start conversion task
        success = self.task_manager.start_image_task(
            "images_to_pdf",
            input_files=files,
            output_path=output_path
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")