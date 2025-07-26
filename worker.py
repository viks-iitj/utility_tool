"""
Utility Pro - Worker Threads
Author: Vivek Srivastava
Description: Multithreading logic for background operations
"""

from PyQt6.QtCore import QThread, pyqtSignal, QObject
from typing import List, Dict, Any, Optional, Callable
import traceback

from core import PDFProcessor, ImageProcessor


class WorkerSignals(QObject):
    """Signals for worker threads"""
    finished = pyqtSignal(bool, str)  # success, message
    progress = pyqtSignal(int)  # progress percentage
    error = pyqtSignal(str)  # error message


class PDFWorker(QThread):
    """Worker thread for PDF operations"""

    def __init__(self, operation: str, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._is_cancelled = False

    def run(self):
        """Execute the PDF operation"""
        try:
            success = False
            message = ""

            if self._is_cancelled:
                return

            self.signals.progress.emit(10)

            if self.operation == "merge":
                success = PDFProcessor.merge_pdfs(
                    self.kwargs['input_files'],
                    self.kwargs['output_path']
                )
                message = "PDFs merged successfully" if success else "Failed to merge PDFs"

            elif self.operation == "custom_merge":
                success = PDFProcessor.custom_merge_pdfs(
                    self.kwargs['merge_instructions'],
                    self.kwargs['output_path']
                )
                message = "Custom merge completed" if success else "Failed to perform custom merge"

            elif self.operation == "split":
                success = True
                total_files = len(self.kwargs['input_files'])
                for i, file in enumerate(self.kwargs['input_files']):
                    if self._is_cancelled:
                        return

                    file_success = PDFProcessor.split_pdf(file, self.kwargs['output_dir'])
                    if not file_success:
                        success = False
                        break

                    progress = int((i + 1) / total_files * 80) + 10
                    self.signals.progress.emit(progress)

                message = "PDFs split successfully" if success else "Failed to split PDFs"

            elif self.operation == "shuffle":
                success = PDFProcessor.shuffle_pages(
                    self.kwargs['input_file'],
                    self.kwargs['output_path'],
                    self.kwargs['page_sequence']
                )
                message = "Pages shuffled successfully" if success else "Failed to shuffle pages"

            elif self.operation == "convert_to_word":
                success = PDFProcessor.convert_to_word(
                    self.kwargs['input_files'],
                    self.kwargs['output_path']
                )
                message = "Converted to Word successfully" if success else "Failed to convert to Word"

            elif self.operation == "convert_to_pages":
                success = PDFProcessor.convert_to_pages(
                    self.kwargs['input_files'],
                    self.kwargs['output_path']
                )
                message = "Converted to Pages successfully" if success else "Failed to convert to Pages"

            elif self.operation == "pdf_to_images":
                success = PDFProcessor.pdf_to_images(
                    self.kwargs['input_files'],
                    self.kwargs['output_dir'],
                    self.kwargs.get('format', 'PNG'),
                    self.kwargs.get('quality_preset', 'Web')
                )
                message = "PDF converted to images" if success else "Failed to convert PDF to images"

            if not self._is_cancelled:
                self.signals.progress.emit(100)
                self.signals.finished.emit(success, message)

        except Exception as e:
            error_msg = f"Error in PDF operation: {str(e)}"
            print(f"{error_msg}\n{traceback.format_exc()}")
            if not self._is_cancelled:
                self.signals.error.emit(error_msg)

    def cancel(self):
        """Cancel the operation"""
        self._is_cancelled = True


class ImageWorker(QThread):
    """Worker thread for image operations"""

    def __init__(self, operation: str, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._is_cancelled = False

    def run(self):
        """Execute the image operation"""
        try:
            success = False
            message = ""

            if self._is_cancelled:
                return

            self.signals.progress.emit(10)

            if self.operation == "images_to_pdf":
                success = ImageProcessor.images_to_pdf(
                    self.kwargs['input_files'],
                    self.kwargs['output_path']
                )
                message = "Images converted to PDF" if success else "Failed to convert images to PDF"

            elif self.operation == "resize":
                success = True
                total_files = len(self.kwargs['input_files'])

                for i, input_file in enumerate(self.kwargs['input_files']):
                    if self._is_cancelled:
                        return

                    output_file = self.kwargs['output_files'][i]
                    file_success = ImageProcessor.resize_image(
                        input_file,
                        output_file,
                        self.kwargs['width'],
                        self.kwargs['height'],
                        self.kwargs.get('maintain_aspect', True)
                    )

                    if not file_success:
                        success = False
                        break

                    progress = int((i + 1) / total_files * 80) + 10
                    self.signals.progress.emit(progress)

                message = "Images resized successfully" if success else "Failed to resize images"

            elif self.operation == "convert_format":
                success = True
                total_files = len(self.kwargs['input_files'])

                for i, input_file in enumerate(self.kwargs['input_files']):
                    if self._is_cancelled:
                        return

                    output_file = self.kwargs['output_files'][i]
                    file_success = ImageProcessor.convert_format(
                        input_file,
                        output_file,
                        self.kwargs['target_format']
                    )

                    if not file_success:
                        success = False
                        break

                    progress = int((i + 1) / total_files * 80) + 10
                    self.signals.progress.emit(progress)

                message = "Images converted successfully" if success else "Failed to convert images"

            elif self.operation == "rotate":
                success = True
                total_files = len(self.kwargs['input_files'])

                for i, input_file in enumerate(self.kwargs['input_files']):
                    if self._is_cancelled:
                        return

                    output_file = self.kwargs['output_files'][i]
                    file_success = ImageProcessor.rotate_image(
                        input_file,
                        output_file,
                        self.kwargs['angle']
                    )

                    if not file_success:
                        success = False
                        break

                    progress = int((i + 1) / total_files * 80) + 10
                    self.signals.progress.emit(progress)

                message = "Images rotated successfully" if success else "Failed to rotate images"

            elif self.operation == "apply_filter":
                success = True
                total_files = len(self.kwargs['input_files'])

                for i, input_file in enumerate(self.kwargs['input_files']):
                    if self._is_cancelled:
                        return

                    output_file = self.kwargs['output_files'][i]
                    file_success = ImageProcessor.apply_filter(
                        input_file,
                        output_file,
                        self.kwargs['filter_type']
                    )

                    if not file_success:
                        success = False
                        break

                    progress = int((i + 1) / total_files * 80) + 10
                    self.signals.progress.emit(progress)

                message = "Filter applied successfully" if success else "Failed to apply filter"

            if not self._is_cancelled:
                self.signals.progress.emit(100)
                self.signals.finished.emit(success, message)

        except Exception as e:
            error_msg = f"Error in image operation: {str(e)}"
            print(f"{error_msg}\n{traceback.format_exc()}")
            if not self._is_cancelled:
                self.signals.error.emit(error_msg)

    def cancel(self):
        """Cancel the operation"""
        self._is_cancelled = True


class TaskManager(QObject):
    """Manages background tasks and workers"""

    task_started = pyqtSignal(str)  # operation name
    task_finished = pyqtSignal(bool, str)  # success, message
    task_progress = pyqtSignal(int)  # progress percentage
    task_error = pyqtSignal(str)  # error message

    def __init__(self):
        super().__init__()
        self.current_worker: Optional[QThread] = None
        self.is_running = False

    def start_pdf_task(self, operation: str, **kwargs) -> bool:
        """Start a PDF processing task"""
        if self.is_running:
            return False

        self.current_worker = PDFWorker(operation, **kwargs)
        self._connect_worker_signals()
        self.current_worker.start()
        self.is_running = True
        self.task_started.emit(operation)
        return True

    def start_image_task(self, operation: str, **kwargs) -> bool:
        """Start an image processing task"""
        if self.is_running:
            return False

        self.current_worker = ImageWorker(operation, **kwargs)
        self._connect_worker_signals()
        self.current_worker.start()
        self.is_running = True
        self.task_started.emit(operation)
        return True

    def cancel_current_task(self):
        """Cancel the currently running task"""
        if self.current_worker and self.is_running:
            if hasattr(self.current_worker, 'cancel'):
                self.current_worker.cancel()
            self.current_worker.quit()
            self.current_worker.wait()
            self.is_running = False

    def _connect_worker_signals(self):
        """Connect worker signals to task manager signals"""
        if self.current_worker and hasattr(self.current_worker, 'signals'):
            self.current_worker.signals.finished.connect(self._on_task_finished)
            self.current_worker.signals.progress.connect(self.task_progress.emit)
            self.current_worker.signals.error.connect(self.task_error.emit)

    def _on_task_finished(self, success: bool, message: str):
        """Handle task completion"""
        self.is_running = False
        self.task_finished.emit(success, message)

        if self.current_worker:
            self.current_worker.quit()
            self.current_worker.wait()
            self.current_worker = None