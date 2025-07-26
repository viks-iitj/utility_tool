"""
Utility Pro - PDF Shuffle Page
Author: Vivek Srivastava
Description: Reorder pages of a PDF based on custom sequence
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QLabel, QPushButton, QTextEdit, QFileDialog,
                             QMessageBox)
from PyQt6.QtCore import Qt


class PDFShufflePage(QWidget):
    """Page for shuffling PDF pages"""

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
        header_label = QLabel("Shuffle PDF Pages")
        header_label.setObjectName("card_title")
        layout.addWidget(header_label)

        description_label = QLabel("Reorder the pages of the first selected PDF based on a custom sequence. Unspecified pages will be appended in their original order.")
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

        # Sequence Configuration Card (spans both columns)
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

        description = QLabel("Select a PDF file to shuffle. Only the first selected file will be processed.")
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
<b>Page Sequence Syntax:</b><br>
• <code>5</code> - Page 5<br>
• <code>1-3</code> - Pages 1, 2, 3<br>
• <code>5, 1-3, 8</code> - Pages 5, 1, 2, 3, 8<br>
• <code>10-7</code> - Pages 10, 9, 8, 7 (reverse)<br><br>

<b>Examples:</b><br>
• <code>5, 1-3, 8</code><br>
• <code>1, 3, 5, 7-10</code><br>
• <code>10-1</code> (reverse all pages)<br><br>

<b>Note:</b> Unspecified pages will be added at the end in their original order.
        """)
        instructions.setObjectName("card_description")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        return card

    def create_sequence_card(self):
        """Create sequence configuration card"""
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel("🔧 Page Sequence Configuration")
        title.setObjectName("card_title")
        layout.addWidget(title)

        description = QLabel("Define the new order for pages in your PDF.")
        description.setObjectName("card_description")
        description.setWordWrap(True)
        layout.addWidget(description)

        # File info
        self.file_info = QLabel("No file selected")
        self.file_info.setStyleSheet("color: #6c757d; font-size: 12px; margin-bottom: 15px;")
        layout.addWidget(self.file_info)

        # Sequence input
        sequence_label = QLabel("Page Sequence:")
        sequence_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(sequence_label)

        self.sequence_input = QTextEdit()
        self.sequence_input.setMaximumHeight(80)
        self.sequence_input.setPlaceholderText("Enter page sequence (e.g., 5, 1-3, 8)")
        layout.addWidget(self.sequence_input)

        # Quick action buttons
        quick_layout = QHBoxLayout()

        reverse_btn = QPushButton("⬅️ Reverse All")
        reverse_btn.setObjectName("secondary")
        reverse_btn.clicked.connect(self.reverse_all_pages)
        quick_layout.addWidget(reverse_btn)

        odd_pages_btn = QPushButton("1️⃣ Odd Pages First")
        odd_pages_btn.setObjectName("secondary")
        odd_pages_btn.clicked.connect(self.odd_pages_first)
        quick_layout.addWidget(odd_pages_btn)

        even_pages_btn = QPushButton("2️⃣ Even Pages First")
        even_pages_btn.setObjectName("secondary")
        even_pages_btn.clicked.connect(self.even_pages_first)
        quick_layout.addWidget(even_pages_btn)

        quick_layout.addStretch()
        layout.addLayout(quick_layout)

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

        self.shuffle_button = QPushButton("🔀 Shuffle Pages")
        self.shuffle_button.setObjectName("success")
        self.shuffle_button.clicked.connect(self.shuffle_pages)
        self.shuffle_button.setEnabled(False)
        button_layout.addWidget(self.shuffle_button)

        layout.addLayout(button_layout)

        return card

    def setup_connections(self):
        """Setup signal connections"""
        # Configure file manager for PDF files
        self.file_manager.set_accepted_extensions(['.pdf'], "PDF documents (*.pdf)")
        self.file_manager.files_changed.connect(self.update_file_info)

        # Connect sequence input changes
        self.sequence_input.textChanged.connect(self.on_sequence_changed)

    def update_file_info(self):
        """Update file information display"""
        files = self.file_manager.get_pdf_files()

        if not files:
            self.file_info.setText("No file selected")
            self.shuffle_button.setEnabled(False)
        else:
            file_name = os.path.basename(files[0])
            if len(files) > 1:
                self.file_info.setText(f"📄 Processing: {file_name} (and {len(files)-1} more - only first will be processed)")
            else:
                self.file_info.setText(f"📄 Processing: {file_name}")

            self.update_shuffle_button_state()

    def on_sequence_changed(self):
        """Handle sequence input changes"""
        self.update_shuffle_button_state()

    def update_shuffle_button_state(self):
        """Update shuffle button enabled state"""
        has_files = len(self.file_manager.get_pdf_files()) > 0
        has_sequence = len(self.sequence_input.toPlainText().strip()) > 0

        self.shuffle_button.setEnabled(has_files and has_sequence)

    def reverse_all_pages(self):
        """Set sequence to reverse all pages"""
        files = self.file_manager.get_pdf_files()
        if not files:
            QMessageBox.information(self, "Info", "Please select a PDF file first.")
            return

        # This would require reading the PDF to get page count
        # For demo purposes, assume a common range
        self.sequence_input.setText("10-1")
        QMessageBox.information(self, "Info", "Sequence set to reverse pages. Adjust the range as needed for your PDF.")

    def odd_pages_first(self):
        """Set sequence to odd pages first"""
        files = self.file_manager.get_pdf_files()
        if not files:
            QMessageBox.information(self, "Info", "Please select a PDF file first.")
            return

        # Demo sequence for odd pages first
        self.sequence_input.setText("1, 3, 5, 7, 9, 2, 4, 6, 8, 10")
        QMessageBox.information(self, "Info", "Sequence set for odd pages first. Adjust as needed for your PDF.")

    def even_pages_first(self):
        """Set sequence to even pages first"""
        files = self.file_manager.get_pdf_files()
        if not files:
            QMessageBox.information(self, "Info", "Please select a PDF file first.")
            return

        # Demo sequence for even pages first
        self.sequence_input.setText("2, 4, 6, 8, 10, 1, 3, 5, 7, 9")
        QMessageBox.information(self, "Info", "Sequence set for even pages first. Adjust as needed for your PDF.")

    def preview_sequence(self):
        """Preview the page sequence"""
        sequence = self.sequence_input.toPlainText().strip()
        files = self.file_manager.get_pdf_files()

        if not files:
            self.preview_area.setText("❌ No file selected")
            return

        if not sequence:
            self.preview_area.setText("❌ No sequence entered")
            return

        try:
            preview_text = self.parse_sequence_preview(sequence)
            self.preview_area.setText(preview_text)
        except Exception as e:
            self.preview_area.setText(f"❌ Invalid sequence: {str(e)}")

    def parse_sequence_preview(self, sequence: str) -> str:
        """Parse and preview the sequence"""
        parts = [part.strip() for part in sequence.split(',')]
        page_list = []

        for part in parts:
            if '-' in part:
                # Range
                start_str, end_str = part.split('-', 1)
                try:
                    start = int(start_str)
                    end = int(end_str)

                    if start <= end:
                        page_list.extend(range(start, end + 1))
                    else:
                        page_list.extend(range(start, end - 1, -1))
                except ValueError:
                    raise ValueError(f"Invalid range '{part}'")
            else:
                # Single page
                try:
                    page_num = int(part)
                    page_list.append(page_num)
                except ValueError:
                    raise ValueError(f"Invalid page number '{part}'")

        # Create preview
        if len(page_list) <= 20:
            preview = f"New page order: {', '.join(map(str, page_list))}"
        else:
            first_10 = ', '.join(map(str, page_list[:10]))
            last_5 = ', '.join(map(str, page_list[-5:]))
            preview = f"New page order: {first_10}, ..., {last_5} ({len(page_list)} pages total)"

        return f"✓ {preview}\n\nNote: Unspecified pages will be added at the end in original order."

    def shuffle_pages(self):
        """Start PDF shuffle process"""
        files = self.file_manager.get_pdf_files()
        sequence = self.sequence_input.toPlainText().strip()

        if not files:
            QMessageBox.warning(self, "Error", "Please select a PDF file.")
            return

        if not sequence:
            QMessageBox.warning(self, "Error", "Please enter a page sequence.")
            return

        # Validate sequence
        try:
            self.parse_sequence_preview(sequence)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid sequence: {str(e)}")
            return

        # Get output file path
        input_file = files[0]
        default_name = f"shuffled_{os.path.splitext(os.path.basename(input_file))[0]}.pdf"

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Shuffled PDF",
            default_name,
            "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        # Start shuffle task
        success = self.task_manager.start_pdf_task(
            "shuffle",
            input_file=input_file,
            output_path=output_path,
            page_sequence=sequence
        )

        if not success:
            QMessageBox.warning(self, "Error", "Another task is currently running. Please wait for it to complete.")