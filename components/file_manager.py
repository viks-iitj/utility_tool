"""
Utility Pro - File Manager Component
Author: Vivek Srivastava
Description: Drag-and-drop file management with multi-selection support
"""

import os
from typing import List, Optional
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QListWidget, QListWidgetItem,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon


class FileListWidget(QListWidget):
    """Custom list widget with drag and drop support"""

    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.DropOnly)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Handle drag move event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        if event.mimeData().hasUrls():
            file_paths = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_paths.append(url.toLocalFile())

            if file_paths:
                self.files_dropped.emit(file_paths)
            event.acceptProposedAction()
        else:
            event.ignore()


class FileManager(QFrame):
    """File management component with drag-and-drop support"""

    files_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("file_management")

        self.files = []  # List of file paths
        self.accepted_extensions = []  # Will be set by pages

        self.init_ui()

    def init_ui(self):
        """Initialize the file manager UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("File Management")
        title_label.setObjectName("section_title")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Action buttons
        self.upload_btn = QPushButton("📁 Upload Files")
        self.upload_btn.clicked.connect(self.upload_files)
        header_layout.addWidget(self.upload_btn)

        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setEnabled(False)
        header_layout.addWidget(self.delete_btn)

        self.clear_btn = QPushButton("🗑️ Clear All")
        self.clear_btn.setObjectName("secondary")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setEnabled(False)
        header_layout.addWidget(self.clear_btn)

        layout.addLayout(header_layout)

        # Drop area
        drop_area = QFrame()
        drop_area.setObjectName("drop_area")
        drop_area.setMinimumHeight(120)
        drop_area_layout = QVBoxLayout(drop_area)

        # Drop instructions
        drop_icon = QLabel("📄")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_icon.setStyleSheet("font-size: 48px; color: #6c757d; margin-bottom: 10px;")
        drop_area_layout.addWidget(drop_icon)

        drop_text = QLabel("Drag and drop files here or click Upload Files")
        drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_text.setStyleSheet("font-size: 16px; color: #6c757d; margin-bottom: 5px;")
        drop_area_layout.addWidget(drop_text)

        self.format_label = QLabel("Supported formats will be shown here")
        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.format_label.setStyleSheet("font-size: 12px; color: #adb5bd;")
        drop_area_layout.addWidget(self.format_label)

        layout.addWidget(drop_area)

        # File list
        list_label = QLabel("Selected Files:")
        list_label.setObjectName("section_title")
        layout.addWidget(list_label)

        self.file_list = FileListWidget()
        self.file_list.files_dropped.connect(self.add_files)
        self.file_list.itemSelectionChanged.connect(self.update_button_states)
        self.file_list.setMinimumHeight(200)
        layout.addWidget(self.file_list)

        # File count label
        self.count_label = QLabel("No files selected")
        self.count_label.setStyleSheet("font-size: 12px; color: #6c757d; margin-top: 5px;")
        layout.addWidget(self.count_label)

    def set_accepted_extensions(self, extensions: List[str], description: str = ""):
        """Set accepted file extensions"""
        self.accepted_extensions = [ext.lower() for ext in extensions]

        if description:
            format_text = f"Accepted formats: {description}"
        else:
            format_text = f"Accepted formats: {', '.join(extensions)}"

        self.format_label.setText(format_text)

    def upload_files(self):
        """Open file dialog to upload files"""
        if not self.accepted_extensions:
            QMessageBox.warning(self, "Error", "No file types configured for this operation.")
            return

        # Create file filter
        extensions_filter = f"Supported Files ({' '.join(['*' + ext for ext in self.accepted_extensions])})"
        all_files_filter = "All Files (*)"
        file_filter = f"{extensions_filter};;{all_files_filter}"

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "",
            file_filter
        )

        if files:
            self.add_files(files)

    def add_files(self, file_paths: List[str]):
        """Add files to the list"""
        added_count = 0
        invalid_files = []

        for file_path in file_paths:
            if not os.path.isfile(file_path):
                continue

            # Check extension
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in self.accepted_extensions:
                invalid_files.append(os.path.basename(file_path))
                continue

            # Avoid duplicates
            if file_path not in self.files:
                self.files.append(file_path)

                # Add to list widget
                item = QListWidgetItem()
                file_name = os.path.basename(file_path)
                file_size = self.format_file_size(os.path.getsize(file_path))

                # Add file type icon
                _, ext = os.path.splitext(file_path)
                if ext.lower() in ['.pdf']:
                    icon = "📄"
                elif ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']:
                    icon = "🖼️"
                else:
                    icon = "📎"

                item.setText(f"{icon} {len(self.files)}. {file_name} ({file_size})")
                item.setData(Qt.ItemDataRole.UserRole, file_path)

                self.file_list.addItem(item)
                added_count += 1

        # Show warnings for invalid files
        if invalid_files:
            invalid_list = '\n'.join(invalid_files[:10])  # Show max 10
            if len(invalid_files) > 10:
                invalid_list += f"\n... and {len(invalid_files) - 10} more"

            QMessageBox.warning(
                self,
                "Invalid Files",
                f"The following files were not added due to unsupported format:\n\n{invalid_list}"
            )

        self.update_display()

        if added_count > 0:
            self.files_changed.emit()

    def delete_selected(self):
        """Delete selected files from the list"""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return

        # Remove from files list and list widget
        for item in selected_items:
            file_path = item.data(Qt.ItemDataRole.UserRole)
            if file_path in self.files:
                self.files.remove(file_path)

            row = self.file_list.row(item)
            self.file_list.takeItem(row)

        # Update numbering
        self.refresh_list_display()
        self.update_display()
        self.files_changed.emit()

    def clear_all(self):
        """Clear all files"""
        reply = QMessageBox.question(
            self,
            "Confirm Clear",
            "Are you sure you want to remove all files?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.files.clear()
            self.file_list.clear()
            self.update_display()
            self.files_changed.emit()

    def refresh_list_display(self):
        """Refresh the display of all items in the list"""
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)

            if file_path:
                file_name = os.path.basename(file_path)
                file_size = self.format_file_size(os.path.getsize(file_path))

                # Add file type icon
                _, ext = os.path.splitext(file_path)
                if ext.lower() in ['.pdf']:
                    icon = "📄"
                elif ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']:
                    icon = "🖼️"
                else:
                    icon = "📎"

                item.setText(f"{icon} {i + 1}. {file_name} ({file_size})")

    def update_button_states(self):
        """Update button enabled states"""
        has_files = len(self.files) > 0
        has_selection = len(self.file_list.selectedItems()) > 0

        self.delete_btn.setEnabled(has_selection)
        self.clear_btn.setEnabled(has_files)

    def update_display(self):
        """Update file count display and button states"""
        count = len(self.files)
        if count == 0:
            self.count_label.setText("No files selected")
        elif count == 1:
            self.count_label.setText("1 file selected")
        else:
            self.count_label.setText(f"{count} files selected")

        self.update_button_states()

    def get_files(self) -> List[str]:
        """Get the list of selected files"""
        return self.files.copy()

    def get_pdf_files(self) -> List[str]:
        """Get only PDF files from the selection"""
        return [f for f in self.files if f.lower().endswith('.pdf')]

    def get_image_files(self) -> List[str]:
        """Get only image files from the selection"""
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']
        return [f for f in self.files if any(f.lower().endswith(ext) for ext in image_extensions)]

    def has_files(self) -> bool:
        """Check if any files are selected"""
        return len(self.files) > 0

    def get_file_count(self) -> int:
        """Get the number of selected files"""
        return len(self.files)

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        if i == 0:
            return f"{int(size_bytes)} {size_names[i]}"
        else:
            return f"{size_bytes:.1f} {size_names[i]}"