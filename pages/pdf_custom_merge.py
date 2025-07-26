"""
Utility Pro - PDF Custom Merge Page
Author: Vivek Srivastava
Description: Create a new PDF from custom page sequences
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QTextEdit, QFileDialog,
                             QMessageBox, QScrollArea, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt


class PDFCustomMergePage(QWidget):
    """Page for custom PDF merging with page sequences"""

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
        header_label = QLabel("Custom PDF Merge")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        description_label = QLabel("Create a new PDF by specifying custom page ranges from multiple PDF files. Use syntax like '1:1-3, 2:4, 1:7-9' where the number before colon is the file number.")
        description_label.setObjectName("card_description")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Main content grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # File Management Card
        file_card = self.create_file_management_card()
        grid_layout.addWidget(file_card, 0, 0)

        # Instructions Card
        instructions_card = self.create_instructions_card()
        grid_layout.addWidget(instructions_card, 0, 1)

        # Page Sequence Card (spans both columns)
        sequence_card = self.create_sequence_card()
        grid_layout.addWidget(sequence_card, 1, 0, 1, 2)

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

        description = QLabel("Add PDF files to use in custom merge. Each file will be numbered for reference.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Add file manager
        layout.addWidget(self.file_manager)

        return card

    def create_instructions_card(self):
        """Create instructions card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("📋 Instructions")
        title.setObjectName("card_title")
        layout.addWidget(title)

        instructions = QLabel("""
<b>Page Range Syntax:</b><br>
• <code>1:1-3</code> - Pages 1-3 from file 1<br>
• <code>2:5</code> - Page 5 from file 2<br>
• <code>1:all</code> - All pages from file 1<br>
• <code>3:2,4,6-8</code> - Pages 2,4,6,7,8 from file 3<br><br>

<b>Examples:</b><br>
• <code>1:1-3, 2:4, 1:7-9</code><br>
• <code>2:all, 1:1, 3:5-10</code><br>
• <code>1:1, 2:1, 3:1</code> (first page from each)
        """)
        instructions.setObjectName("card_description")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        return card

    def create_sequence_card(self):
        """Create page sequence configuration card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("🔧 Page Sequence Configuration")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Define the page sequence for your custom merged PDF.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # File list for reference
        ref_label = QLabel("📄 File Reference:")
        ref_label.setStyleSheet("font-weight: 600; margin-top: 10px;")
        layout.addWidget(ref_label)

        self.file_reference = QLabel("No files selected")
        self.file_reference.setStyleSheet("color: #6c757d; font-size: 12px; margin-bottom: 15px;")
        layout.addWidget(self.file_reference)

        # Sequence input
        sequence_label = QLabel("Page Sequence:")
        sequence_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(sequence_label)

        self.sequence_input = QTextEdit()
        self.sequence_input.setMaximumHeight(100)
        self.sequence_input.setPlaceholderText("Enter page sequence (e.g., 1:1-3, 2:4, 1:7-9)")
        layout.addWidget(self.sequence_input)

        # Preview area
        preview_label = QLabel("📋 Sequence Preview:")
        preview_label.setStyleSheet("font-weight: 600; margin-top: 15px;")
        layout.addWidget(preview_label)

        self.preview_area = QLabel("Enter a sequence to see preview")
        self.preview_area.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 10px; font-family: monospace; color: #6c757d;")
        self.preview_area.setWordWrap(True)
        self.preview_area.setMinimumHeight(60)
        layout.addWidget(self.preview_area)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        preview_button = QPushButton("👁️ Preview Sequence")
        preview_button.setObjectName("secondary")
        preview_button.clicked.connect(self.preview_sequence)
        button_layout.addWidget(preview_button)

        self.merge_button = QPushButton("🔗 Create Custom PDF")
        self.merge_button.setObjectName("success")
        self.merge_button.clicked.connect(self.create_custom_pdf)
        self.merge_button.setEnabled(False)
        button_layout.addWidget(self.merge_button)

        layout.addLayout(button_layout)

        return card

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for PDF files
        self.file_manager.set_accepted_extensions(['.pdf'], "PDF documents (*.pdf)")
        self.file_manager.files_changed.connect(self.update_file_reference)

        # Connect sequence input changes
        self.sequence_input.textChanged.connect(self.on_sequence_changed)

    def update_file_reference(self):
        """Update file reference display"""
        files = self.file_manager.get_pdf_files()

        if not files:
            self.file_reference.setText("No files selected")
            self.merge_button.setEnabled(False)
        else:
            ref_text = []
            for i, file_path in enumerate(files, 1):
                file_name = os.path.basename(file_path)
                ref_text.append(f"{i}. {file_name}")

            self.file_reference.setText("\n".join(ref_text))
            self.update_merge_button_state()

    def on_sequence_changed(self):
        """Handle sequence input changes"""
        self.update_merge_button_state()

    def update_merge_button_state(self):
        """Update merge button enabled state"""
        has_files = len(self.file_manager.get_pdf_files()) > 0
        has_sequence = len(self.sequence_input.toPlainText().strip()) > 0

        self.merge_button.setEnabled(has_files and has_sequence)

    def preview_sequence(self):
        """Preview the page sequence"""
        sequence = self.sequence_input.toPlainText().strip()
        files = self.file_manager.get_pdf_files()

        if not files:
            self.preview_area.setText("❌ No files selected")
            return

        if not sequence:
            self.preview_area.setText("❌ No sequence entered")
            return

        try:
            preview_text = self.parse_sequence_preview(sequence, files)
            self.preview_area.setText(preview_text)
        except Exception as e:
            self.preview_area.setText(f"❌ Invalid sequence: {str(e)}")

    def parse_sequence_preview(self, sequence: str, files: list) -> str:
        """Parse and preview the sequence"""
        parts = [part.strip() for part in sequence.split(',')]
        preview_lines = []

        for i, part in enumerate(parts, 1):
            if ':' not in part:
                raise ValueError(f"Invalid format in part '{part}'. Use format 'file:pages'")

            file_num_str, page_spec = part.split(':', 1)

            try:
                file_num = int(file_num_str)
            except ValueError:
                raise ValueError(f"Invalid file number '{file_num_str}' in part '{part}'")

            if file_num < 1 or file_num > len(files):
                raise ValueError(f"File number {file_num} is out of range (1-{len(files)})")

            file_name = os.path.basename(files[file_num - 1])

            if page_spec.lower() == 'all':
                page_desc = "all pages"
            else:
                page_desc = f"pages {page_spec}"

            preview_lines.append(f"{i}. From '{file_name}': {page_desc}")

        return "\n".join(preview_lines)

    def create_custom_pdf(self):
        """Create custom PDF with specified sequence"""
        files = self.file_manager.get_pdf_files()
        sequence = self.sequence_input.toPlainText().strip()

        if not files:
            QMessageBox.warning(self, "Error", "Please select PDF files first.")
            return

        if not sequence:
            QMessageBox.warning(self, "Error", "Please enter a page sequence.")
            return

        # Parse sequence into merge instructions
        try:
            merge_instructions = self.parse_merge_instructions(sequence, files)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid sequence: {str(e)}")
            return

        # Get output file path
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Custom PDF",
            "custom_merged_document.pdf",
            "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        # Start custom merge task
        success = self.task_manager.start_pdf_task(
            "custom_merge",
            merge_instructions=merge_instructions,
            output_path=output_path
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")

    def parse_merge_instructions(self, sequence: str, files: list) -> list:
        """Parse sequence into merge instructions for the core processor"""
        parts = [part.strip() for part in sequence.split(',')]
        instructions = []

        for part in parts:
            if ':' not in part:
                raise ValueError(f"Invalid format in part '{part}'. Use format 'file:pages'")

            file_num_str, page_spec = part.split(':', 1)

            try:
                file_num = int(file_num_str)
            except ValueError:
                raise ValueError(f"Invalid file number '{file_num_str}' in part '{part}'")

            if file_num < 1 or file_num > len(files):
                raise ValueError(f"File number {file_num} is out of range (1-{len(files)})")

            file_path = files[file_num - 1]

            # Convert page_spec to the format expected by core processor
            if page_spec.lower() == 'all':
                page_range = 'all'
            else:
                page_range = page_spec

            instructions.append((file_path, page_range))

        return instructions