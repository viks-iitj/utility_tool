"""
Utility Pro - Core Processing Logic
Author: Vivek Srivastava  
Description: Backend processing for PDF and image operations with improved error handling
"""

import os
import platform
import subprocess
import tempfile
import logging
from typing import List, Tuple, Optional, Dict, Any

try:
    from PIL import Image, ImageFilter, ImageEnhance
except ImportError:
    print("Warning: PIL/Pillow not installed. Image processing will be limited.")
    Image = None

try:
    import PyPDF2
except ImportError:
    print("Warning: PyPDF2 not installed. PDF processing will be limited.")
    PyPDF2 = None

try:
    from pdf2docx import Converter
except ImportError:
    print("Warning: pdf2docx not installed. PDF to Word conversion unavailable.")
    Converter = None

try:
    from docx import Document
except ImportError:
    print("Warning: python-docx not installed. Word document creation unavailable.")
    Document = None

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Warning: PyMuPDF not installed. Some PDF features will be limited.")
    fitz = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles all PDF-related operations with improved error handling"""

    @staticmethod
    def merge_pdfs(input_files: List[str], output_path: str) -> bool:
        """Merge multiple PDF files into one"""
        if not PyPDF2:
            logger.error("PyPDF2 not available")
            return False

        merger = None
        try:
            # Validate input files
            for file in input_files:
                if not os.path.exists(file):
                    logger.error(f"Input file does not exist: {file}")
                    return False
                if not file.lower().endswith('.pdf'):
                    logger.error(f"Invalid file format: {file}")
                    return False

            merger = PyPDF2.PdfMerger()
            for file in input_files:
                try:
                    merger.append(file)
                except Exception as e:
                    logger.error(f"Error appending file {file}: {e}")
                    return False

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'wb') as output_file:
                merger.write(output_file)

            return True

        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            return False
        finally:
            if merger:
                merger.close()

    @staticmethod
    def custom_merge_pdfs(merge_instructions: List[Dict[str, Any]], output_path: str) -> bool:
        """Custom merge PDFs with specific page ranges"""
        if not PyPDF2:
            logger.error("PyPDF2 not available")
            return False

        merger = None
        try:
            merger = PyPDF2.PdfMerger()

            for instruction in merge_instructions:
                file_path = instruction.get('file')
                page_range = instruction.get('pages', 'all')

                if not os.path.exists(file_path):
                    logger.error(f"Input file does not exist: {file_path}")
                    return False

                try:
                    if page_range == 'all':
                        merger.append(file_path)
                    else:
                        # Parse page range
                        pages = PDFProcessor._parse_page_range(page_range, PDFProcessor._get_pdf_page_count(file_path))
                        if pages:
                            for page in pages:
                                merger.append(file_path, pages=(page-1, page))  # PyPDF2 uses 0-based indexing
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
                    return False

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'wb') as output_file:
                merger.write(output_file)

            return True

        except Exception as e:
            logger.error(f"Error in custom merge: {e}")
            return False
        finally:
            if merger:
                merger.close()

    @staticmethod
    def split_pdf(input_file: str, output_dir: str) -> bool:
        """Split PDF into individual pages"""
        if not PyPDF2:
            logger.error("PyPDF2 not available")
            return False

        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file does not exist: {input_file}")
                return False

            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            with open(input_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)

                base_name = os.path.splitext(os.path.basename(input_file))[0]

                for page_num in range(total_pages):
                    writer = PyPDF2.PdfWriter()
                    writer.add_page(reader.pages[page_num])

                    output_filename = f"{base_name}_page_{page_num + 1:03d}.pdf"
                    output_path = os.path.join(output_dir, output_filename)

                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)

            return True

        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            return False

    @staticmethod
    def shuffle_pages(input_file: str, output_path: str, page_sequence: List[int]) -> bool:
        """Shuffle PDF pages according to specified sequence"""
        if not PyPDF2:
            logger.error("PyPDF2 not available")
            return False

        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file does not exist: {input_file}")
                return False

            with open(input_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)

                # Validate page sequence
                for page_num in page_sequence:
                    if page_num < 1 or page_num > total_pages:
                        logger.error(f"Invalid page number: {page_num}. PDF has {total_pages} pages.")
                        return False

                writer = PyPDF2.PdfWriter()

                # Add pages in the specified sequence
                for page_num in page_sequence:
                    writer.add_page(reader.pages[page_num - 1])  # Convert to 0-based indexing

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

            return True

        except Exception as e:
            logger.error(f"Error shuffling pages: {e}")
            return False

    @staticmethod
    def convert_to_word(input_files: List[str], output_path: str) -> bool:
        """Convert PDF files to Word document"""
        if not Converter:
            logger.error("pdf2docx not available")
            return False

        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # For multiple files, create a combined Word document
            if len(input_files) == 1:
                cv = Converter(input_files[0])
                cv.convert(output_path, start=0, end=None)
                cv.close()
            else:
                # Merge multiple PDFs first, then convert
                temp_pdf = tempfile.mktemp(suffix='.pdf')
                if PDFProcessor.merge_pdfs(input_files, temp_pdf):
                    cv = Converter(temp_pdf)
                    cv.convert(output_path, start=0, end=None)
                    cv.close()
                    os.unlink(temp_pdf)  # Clean up temp file
                else:
                    return False

            return True

        except Exception as e:
            logger.error(f"Error converting to Word: {e}")
            return False

    @staticmethod
    def convert_to_pages(input_files: List[str], output_path: str) -> bool:
        """Convert PDF files to Apple Pages format (via RTF)"""
        try:
            # Convert to RTF first (Pages can import RTF)
            rtf_path = output_path.replace('.pages', '.rtf')

            # For macOS, we can use textutil for basic conversion
            if platform.system() == 'Darwin':
                if len(input_files) == 1:
                    subprocess.run(['textutil', '-convert', 'rtf', input_files[0], '-output', rtf_path],
                                 check=True)
                else:
                    # Merge PDFs first
                    temp_pdf = tempfile.mktemp(suffix='.pdf')
                    if PDFProcessor.merge_pdfs(input_files, temp_pdf):
                        subprocess.run(['textutil', '-convert', 'rtf', temp_pdf, '-output', rtf_path],
                                     check=True)
                        os.unlink(temp_pdf)
                    else:
                        return False

                return True
            else:
                logger.error("Pages conversion only supported on macOS")
                return False

        except Exception as e:
            logger.error(f"Error converting to Pages: {e}")
            return False

    @staticmethod
    def pdf_to_images(input_files: List[str], output_dir: str, format: str = 'PNG', quality_preset: str = 'Web') -> bool:
        """Convert PDF pages to images"""
        if not fitz:
            logger.error("PyMuPDF not available")
            return False

        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Set quality based on preset
            quality_map = {
                'Web': (72, 72),      # 72 DPI
                'Print': (150, 150),  # 150 DPI
                'High': (300, 300)    # 300 DPI
            }
            dpi_x, dpi_y = quality_map.get(quality_preset, (72, 72))

            for input_file in input_files:
                if not os.path.exists(input_file):
                    logger.error(f"Input file does not exist: {input_file}")
                    return False

                doc = fitz.open(input_file)
                base_name = os.path.splitext(os.path.basename(input_file))[0]

                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)

                    # Create transformation matrix for desired DPI
                    mat = fitz.Matrix(dpi_x/72, dpi_y/72)
                    pix = page.get_pixmap(matrix=mat)

                    output_filename = f"{base_name}_page_{page_num + 1:03d}.{format.lower()}"
                    output_path = os.path.join(output_dir, output_filename)

                    pix.save(output_path)

                doc.close()

            return True

        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            return False

    @staticmethod
    def _parse_page_range(page_range: str, total_pages: int) -> List[int]:
        """Parse page range string (e.g., '1-3,5,7-9') into list of page numbers"""
        pages = []

        try:
            parts = page_range.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    pages.extend(range(start, min(end + 1, total_pages + 1)))
                else:
                    page_num = int(part)
                    if 1 <= page_num <= total_pages:
                        pages.append(page_num)
        except ValueError as e:
            logger.error(f"Invalid page range format: {page_range}")
            return []

        # Remove duplicates and sort
        return sorted(list(set(pages)))

    @staticmethod
    def _get_pdf_page_count(file_path: str) -> int:
        """Get the number of pages in a PDF file"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return len(reader.pages)
        except Exception as e:
            logger.error(f"Error getting page count for {file_path}: {e}")
            return 0


class ImageProcessor:
    """Handles all image-related operations with improved error handling"""

    SUPPORTED_FORMATS = ['PNG', 'JPEG', 'JPG', 'TIFF', 'TIF', 'BMP', 'WEBP', 'GIF']

    @staticmethod
    def images_to_pdf(image_files: List[str], output_path: str) -> bool:
        """Convert images to PDF"""
        if not Image:
            logger.error("PIL/Pillow not available")
            return False

        try:
            # Validate input files
            for image_file in image_files:
                if not os.path.exists(image_file):
                    logger.error(f"Input file does not exist: {image_file}")
                    return False

            images = []
            for image_file in image_files:
                try:
                    img = Image.open(image_file)
                    if img.mode not in ['RGB', 'RGBA']:
                        img = img.convert('RGB')
                    elif img.mode == 'RGBA':
                        # Create white background for transparent images
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    images.append(img)
                except Exception as e:
                    logger.error(f"Error processing image {image_file}: {e}")
                    return False

            if images:
                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                images[0].save(output_path, save_all=True, append_images=images[1:])
                return True

            return False

        except Exception as e:
            logger.error(f"Error converting images to PDF: {e}")
            return False

    @staticmethod
    def resize_image(input_file: str, output_file: str, width: int, height: int, maintain_aspect: bool = True) -> bool:
        """Resize an image"""
        if not Image:
            logger.error("PIL/Pillow not available")
            return False

        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file does not exist: {input_file}")
                return False

            with Image.open(input_file) as img:
                if maintain_aspect:
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                else:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                # Save with appropriate format
                img.save(output_file)

            return True

        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            return False

    @staticmethod
    def convert_format(input_file: str, output_file: str, target_format: str) -> bool:
        """Convert image to different format"""
        if not Image:
            logger.error("PIL/Pillow not available")
            return False

        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file does not exist: {input_file}")
                return False

            with Image.open(input_file) as img:
                # Handle transparency for formats that don't support it
                if target_format.upper() in ['JPEG', 'JPG'] and img.mode in ['RGBA', 'LA']:
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif target_format.upper() == 'PNG' and img.mode not in ['RGBA', 'RGB', 'L']:
                    img = img.convert('RGBA')

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                # Save with target format
                img.save(output_file, format=target_format.upper())

            return True

        except Exception as e:
            logger.error(f"Error converting image format: {e}")
            return False

    @staticmethod
    def rotate_image(input_file: str, output_file: str, angle: float) -> bool:
        """Rotate an image by specified angle"""
        if not Image:
            logger.error("PIL/Pillow not available")
            return False

        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file does not exist: {input_file}")
                return False

            with Image.open(input_file) as img:
                # Rotate image (counter-clockwise)
                rotated = img.rotate(angle, expand=True)

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                # Save rotated image
                rotated.save(output_file)

            return True

        except Exception as e:
            logger.error(f"Error rotating image: {e}")
            return False

    @staticmethod
    def apply_filter(input_file: str, output_file: str, filter_type: str) -> bool:
        """Apply filter to an image"""
        if not Image:
            logger.error("PIL/Pillow not available")
            return False

        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file does not exist: {input_file}")
                return False

            with Image.open(input_file) as img:
                # Apply filter based on type
                if filter_type == 'blur':
                    filtered = img.filter(ImageFilter.BLUR)
                elif filter_type == 'sharpen':
                    filtered = img.filter(ImageFilter.SHARPEN)
                elif filter_type == 'smooth':
                    filtered = img.filter(ImageFilter.SMOOTH)
                elif filter_type == 'detail':
                    filtered = img.filter(ImageFilter.DETAIL)
                elif filter_type == 'edge_enhance':
                    filtered = img.filter(ImageFilter.EDGE_ENHANCE)
                elif filter_type == 'emboss':
                    filtered = img.filter(ImageFilter.EMBOSS)
                elif filter_type == 'contour':
                    filtered = img.filter(ImageFilter.CONTOUR)
                elif filter_type == 'grayscale':
                    filtered = img.convert('L')
                elif filter_type == 'sepia':
                    # Create sepia effect
                    grayscale = img.convert('L')
                    sepia = Image.new('RGB', img.size)
                    sepia_pixels = []
                    for pixel in grayscale.getdata():
                        # Apply sepia tone
                        r = min(255, int(pixel * 1.35))
                        g = min(255, int(pixel * 1.2))
                        b = min(255, int(pixel * 0.8))
                        sepia_pixels.append((r, g, b))
                    sepia.putdata(sepia_pixels)
                    filtered = sepia
                elif filter_type == 'brightness_up':
                    enhancer = ImageEnhance.Brightness(img)
                    filtered = enhancer.enhance(1.3)
                elif filter_type == 'brightness_down':
                    enhancer = ImageEnhance.Brightness(img)
                    filtered = enhancer.enhance(0.7)
                elif filter_type == 'contrast_up':
                    enhancer = ImageEnhance.Contrast(img)
                    filtered = enhancer.enhance(1.3)
                elif filter_type == 'contrast_down':
                    enhancer = ImageEnhance.Contrast(img)
                    filtered = enhancer.enhance(0.7)
                else:
                    logger.error(f"Unknown filter type: {filter_type}")
                    return False

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                # Save filtered image
                filtered.save(output_file)

            return True

        except Exception as e:
            logger.error(f"Error applying filter: {e}")
            return False

    @staticmethod
    def is_supported_format(file_path: str) -> bool:
        """Check if file format is supported"""
        ext = os.path.splitext(file_path)[1].upper().lstrip('.')
        return ext in ImageProcessor.SUPPORTED_FORMATS