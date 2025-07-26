"""
Utility Pro - Image Tools Page
Author: Vivek Srivastava
Description: Comprehensive image editing tools
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QComboBox, QSpinBox,
                             QCheckBox, QFileDialog, QMessageBox, QTabWidget,
                             QButtonGroup, QRadioButton)
from PyQt6.QtCore import Qt


class ImageToolsPage(QWidget):
    """Page for image editing tools"""

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
        header_label = QLabel("Image Editing Tools")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        description_label = QLabel("Comprehensive image editing tools including resize, format conversion, rotation, and filters.")
        description_label.setObjectName("card_description")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Main content
        main_layout = QHBoxLayout()

        # File management (left side)
        file_card = self.create_file_management_card()
        file_card.setMaximumWidth(400)
        main_layout.addWidget(file_card)

        # Tools tabs (right side)
        tools_widget = self.create_tools_widget()
        main_layout.addWidget(tools_widget, 1)

        layout.addLayout(main_layout)

    def create_file_management_card(self):
        """Create file management card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("🖼️ Image Selection")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Add image files to edit. Tools will be applied to all selected images.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Add file manager
        layout.addWidget(self.file_manager)

        # Output directory
        output_frame = QFrame()
        output_layout = QVBoxLayout(output_frame)

        output_label = QLabel("📁 Output Directory:")
        output_label.setStyleSheet("font-weight: 600; margin-bottom: 5px; margin-top: 15px;")
        output_layout.addWidget(output_label)

        dir_layout = QHBoxLayout()

        self.output_path_label = QLabel("Same as source")
        self.output_path_label.setStyleSheet("color: #6c757d; font-size: 11px; border: 1px solid #dee2e6; padding: 8px; border-radius: 4px; background-color: #f8f9fa;")
        self.output_path_label.setWordWrap(True)
        dir_layout.addWidget(self.output_path_label, 1)

        self.browse_output_button = QPushButton("📁 Browse")
        self.browse_output_button.setObjectName("secondary")
        self.browse_output_button.clicked.connect(self.browse_output_directory)
        dir_layout.addWidget(self.browse_output_button)

        output_layout.addLayout(dir_layout)
        layout.addWidget(output_frame)

        return card

    def create_tools_widget(self):
        """Create tools tab widget"""
        tab_widget = QTabWidget()

        # Resize tab
        resize_tab = self.create_resize_tab()
        tab_widget.addTab(resize_tab, "📏 Resize")

        # Convert tab
        convert_tab = self.create_convert_tab()
        tab_widget.addTab(convert_tab, "🔄 Convert")

        # Rotate tab
        rotate_tab = self.create_rotate_tab()
        tab_widget.addTab(rotate_tab, "🔄 Rotate")

        # Filters tab
        filters_tab = self.create_filters_tab()
        tab_widget.addTab(filters_tab, "🎨 Filters")

        return tab_widget

    def create_resize_tab(self):
        """Create resize tool tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Resize card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        title = QLabel("📏 Resize Images")
        title.setObjectName("card_title")
        card_layout.addWidget(title)

        description = QLabel("Change the dimensions of your images with aspect ratio control.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        card_layout.addWidget(description)

        # Resize options
        options_layout = QGridLayout()

        # Width
        width_label = QLabel("Width (pixels):")
        width_label.setStyleSheet("font-weight: 600;")
        options_layout.addWidget(width_label, 0, 0)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(800)
        self.width_spin.valueChanged.connect(self.on_width_changed)
        options_layout.addWidget(self.width_spin, 0, 1)

        # Height
        height_label = QLabel("Height (pixels):")
        height_label.setStyleSheet("font-weight: 600;")
        options_layout.addWidget(height_label, 1, 0)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(600)
        self.height_spin.valueChanged.connect(self.on_height_changed)
        options_layout.addWidget(self.height_spin, 1, 1)

        # Maintain aspect ratio
        self.maintain_aspect = QCheckBox("Maintain aspect ratio")
        self.maintain_aspect.setChecked(True)
        self.maintain_aspect.toggled.connect(self.on_aspect_toggled)
        options_layout.addWidget(self.maintain_aspect, 2, 0, 1, 2)

        card_layout.addLayout(options_layout)

        # Preset sizes
        presets_label = QLabel("📐 Common Presets:")
        presets_label.setStyleSheet("font-weight: 600; margin-top: 15px;")
        card_layout.addWidget(presets_label)

        presets_layout = QHBoxLayout()

        preset_buttons = [
            ("HD (1280×720)", 1280, 720),
            ("Full HD (1920×1080)", 1920, 1080),
            ("4K (3840×2160)", 3840, 2160),
            ("Square (1000×1000)", 1000, 1000)
        ]

        for name, w, h in preset_buttons:
            btn = QPushButton(name)
            btn.setObjectName("secondary")
            btn.clicked.connect(lambda checked, width=w, height=h: self.set_dimensions(width, height))
            presets_layout.addWidget(btn)

        card_layout.addLayout(presets_layout)

        card_layout.addStretch()

        # Resize button
        resize_button = QPushButton("📏 Resize Images")
        resize_button.setObjectName("success")
        resize_button.clicked.connect(self.resize_images)
        card_layout.addWidget(resize_button)

        layout.addWidget(card)
        layout.addStretch()

        return tab

    def create_convert_tab(self):
        """Create format conversion tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Convert card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        title = QLabel("🔄 Convert Format")
        title.setObjectName("card_title")
        card_layout.addWidget(title)

        description = QLabel("Convert images between different formats with quality options.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        card_layout.addWidget(description)

        # Format selection
        format_layout = QHBoxLayout()

        format_label = QLabel("Target Format:")
        format_label.setStyleSheet("font-weight: 600;")
        format_layout.addWidget(format_label)

        self.target_format = QComboBox()
        self.target_format.addItems(["PNG", "JPEG", "TIFF", "WebP", "BMP"])
        self.target_format.currentTextChanged.connect(self.on_format_changed)
        format_layout.addWidget(self.target_format)

        format_layout.addStretch()
        card_layout.addLayout(format_layout)

        # Format info
        self.format_info_label = QLabel()
        self.format_info_label.setStyleSheet("color: #6c757d; font-size: 12px; margin-top: 5px;")
        self.format_info_label.setWordWrap(True)
        card_layout.addWidget(self.format_info_label)

        # Quality settings (for JPEG)
        self.quality_frame = QFrame()
        quality_layout = QVBoxLayout(self.quality_frame)

        quality_label = QLabel("JPEG Quality:")
        quality_label.setStyleSheet("font-weight: 600; margin-top: 15px;")
        quality_layout.addWidget(quality_label)

        quality_options_layout = QHBoxLayout()

        self.quality_group = QButtonGroup(self)

        self.high_quality = QRadioButton("High (95%)")
        self.high_quality.setChecked(True)
        self.quality_group.addButton(self.high_quality, 95)
        quality_options_layout.addWidget(self.high_quality)

        self.medium_quality = QRadioButton("Medium (75%)")
        self.quality_group.addButton(self.medium_quality, 75)
        quality_options_layout.addWidget(self.medium_quality)

        self.low_quality = QRadioButton("Low (50%)")
        self.quality_group.addButton(self.low_quality, 50)
        quality_options_layout.addWidget(self.low_quality)

        quality_layout.addLayout(quality_options_layout)
        card_layout.addWidget(self.quality_frame)

        card_layout.addStretch()

        # Convert button
        convert_button = QPushButton("🔄 Convert Images")
        convert_button.setObjectName("success")
        convert_button.clicked.connect(self.convert_images)
        card_layout.addWidget(convert_button)

        layout.addWidget(card)
        layout.addStretch()

        # Update format info initially
        self.update_format_info()

        return tab

    def create_rotate_tab(self):
        """Create rotation tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Rotate card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        title = QLabel("🔄 Rotate Images")
        title.setObjectName("card_title")
        card_layout.addWidget(title)

        description = QLabel("Rotate images by fixed angles or flip them.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        card_layout.addWidget(description)

        # Rotation options
        rotation_layout = QGridLayout()

        # Common rotations
        rotate_90_btn = QPushButton("↻ 90° Right")
        rotate_90_btn.setObjectName("secondary")
        rotate_90_btn.clicked.connect(lambda: self.rotate_images(90))
        rotation_layout.addWidget(rotate_90_btn, 0, 0)

        rotate_180_btn = QPushButton("↻ 180°")
        rotate_180_btn.setObjectName("secondary")
        rotate_180_btn.clicked.connect(lambda: self.rotate_images(180))
        rotation_layout.addWidget(rotate_180_btn, 0, 1)

        rotate_270_btn = QPushButton("↺ 90° Left")
        rotate_270_btn.setObjectName("secondary")
        rotate_270_btn.clicked.connect(lambda: self.rotate_images(-90))
        rotation_layout.addWidget(rotate_270_btn, 1, 0)

        card_layout.addLayout(rotation_layout)

        card_layout.addStretch()

        layout.addWidget(card)
        layout.addStretch()

        return tab

    def create_filters_tab(self):
        """Create filters tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Filters card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        title = QLabel("🎨 Apply Filters")
        title.setObjectName("card_title")
        card_layout.addWidget(title)

        description = QLabel("Apply various filters and effects to your images.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        card_layout.addWidget(description)

        # Filter selection
        filter_layout = QHBoxLayout()

        filter_label = QLabel("Filter Type:")
        filter_label.setStyleSheet("font-weight: 600;")
        filter_layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Grayscale", "Sepia", "Invert", "Sharpen", "Blur"])
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.filter_combo)

        filter_layout.addStretch()
        card_layout.addLayout(filter_layout)

        # Filter description
        self.filter_description = QLabel()
        self.filter_description.setStyleSheet("color: #6c757d; font-size: 12px; margin-top: 5px;")
        self.filter_description.setWordWrap(True)
        card_layout.addWidget(self.filter_description)

        # Filter preview info
        preview_info = QLabel("📋 Filter Preview:")
        preview_info.setStyleSheet("font-weight: 600; margin-top: 15px;")
        card_layout.addWidget(preview_info)

        preview_desc = QLabel("Filters will be applied to all selected images. Original files will be preserved.")
        preview_desc.setStyleSheet("color: #6c757d; font-size: 12px;")
        preview_desc.setWordWrap(True)
        card_layout.addWidget(preview_desc)

        card_layout.addStretch()

        # Apply filter button
        filter_button = QPushButton("🎨 Apply Filter")
        filter_button.setObjectName("success")
        filter_button.clicked.connect(self.apply_filter)
        card_layout.addWidget(filter_button)

        layout.addWidget(card)
        layout.addStretch()

        # Update filter info initially
        self.update_filter_info()

        return tab

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp', '.gif']
        self.file_manager.set_accepted_extensions(
            image_extensions,
            "Image files (PNG, JPEG, TIFF, BMP, WebP, GIF)"
        )

        # Initialize output directory
        self.output_directory = None  # None means same as source

    def browse_output_directory(self):
        """Browse for output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            os.path.expanduser("~/Documents")
        )

        if directory:
            self.output_directory = directory
            self.output_path_label.setText(directory)
        else:
            self.output_directory = None
            self.output_path_label.setText("Same as source")

    def set_dimensions(self, width, height):
        """Set specific dimensions"""
        self.width_spin.setValue(width)
        self.height_spin.setValue(height)

    def on_width_changed(self):
        """Handle width change for aspect ratio"""
        if self.maintain_aspect.isChecked():
            # Simple 4:3 ratio for demo
            new_height = int(self.width_spin.value() * 3 / 4)
            self.height_spin.blockSignals(True)
            self.height_spin.setValue(new_height)
            self.height_spin.blockSignals(False)

    def on_height_changed(self):
        """Handle height change for aspect ratio"""
        if self.maintain_aspect.isChecked():
            # Simple 4:3 ratio for demo
            new_width = int(self.height_spin.value() * 4 / 3)
            self.width_spin.blockSignals(True)
            self.width_spin.setValue(new_width)
            self.width_spin.blockSignals(False)

    def on_aspect_toggled(self):
        """Handle aspect ratio toggle"""
        pass  # Could implement more sophisticated aspect ratio handling

    def on_format_changed(self):
        """Handle format change"""
        self.update_format_info()

        # Show/hide quality options for JPEG
        is_jpeg = self.target_format.currentText() == "JPEG"
        self.quality_frame.setVisible(is_jpeg)

    def update_format_info(self):
        """Update format information"""
        format_descriptions = {
            "PNG": "Lossless compression, supports transparency, larger files",
            "JPEG": "Lossy compression, smaller files, no transparency, quality options",
            "TIFF": "High quality, lossless, very large files, professional use",
            "WebP": "Modern format, excellent compression, smaller than PNG",
            "BMP": "Uncompressed, very large files, maximum quality"
        }

        current_format = self.target_format.currentText()
        self.format_info_label.setText(format_descriptions.get(current_format, ""))

    def on_filter_changed(self):
        """Handle filter change"""
        self.update_filter_info()

    def update_filter_info(self):
        """Update filter information"""
        filter_descriptions = {
            "Grayscale": "Convert image to black and white",
            "Sepia": "Apply vintage sepia tone effect",
            "Invert": "Invert all colors (negative effect)",
            "Sharpen": "Enhance edges and details",
            "Blur": "Apply blur effect to soften image"
        }

        current_filter = self.filter_combo.currentText()
        self.filter_description.setText(filter_descriptions.get(current_filter, ""))

    def get_output_files(self, input_files, suffix="", extension=None):
        """Generate output file paths"""
        output_files = []

        for input_file in input_files:
            dir_path = self.output_directory if self.output_directory else os.path.dirname(input_file)
            base_name = os.path.splitext(os.path.basename(input_file))[0]

            if extension:
                ext = f".{extension.lower()}"
            else:
                ext = os.path.splitext(input_file)[1]

            output_file = os.path.join(dir_path, f"{base_name}{suffix}{ext}")
            output_files.append(output_file)

        return output_files

    def resize_images(self):
        """Resize selected images"""
        files = self.file_manager.get_image_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select image files to resize.")
            return

        width = self.width_spin.value()
        height = self.height_spin.value()
        maintain_aspect = self.maintain_aspect.isChecked()

        output_files = self.get_output_files(files, "_resized")

        # Start resize task
        success = self.task_manager.start_image_task(
            "resize",
            input_files=files,
            output_files=output_files,
            width=width,
            height=height,
            maintain_aspect=maintain_aspect
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")

    def convert_images(self):
        """Convert image formats"""
        files = self.file_manager.get_image_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select image files to convert.")
            return

        target_format = self.target_format.currentText()
        output_files = self.get_output_files(files, f"_converted", target_format)

        # Start convert task
        success = self.task_manager.start_image_task(
            "convert_format",
            input_files=files,
            output_files=output_files,
            target_format=target_format
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")

    def rotate_images(self, angle):
        """Rotate images by specified angle"""
        files = self.file_manager.get_image_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select image files to rotate.")
            return

        output_files = self.get_output_files(files, f"_rotated_{angle}")

        # Start rotate task
        success = self.task_manager.start_image_task(
            "rotate",
            input_files=files,
            output_files=output_files,
            angle=angle
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")

    def apply_filter(self):
        """Apply selected filter to images"""
        files = self.file_manager.get_image_files()

        if not files:
            QMessageBox.warning(self, "Error", "Please select image files to apply filter.")
            return

        filter_type = self.filter_combo.currentText()
        output_files = self.get_output_files(files, f"_{filter_type.lower()}")

        # Start filter task
        success = self.task_manager.start_image_task(
            "apply_filter",
            input_files=files,
            output_files=output_files,
            filter_type=filter_type
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")