"""
Shared content extraction utilities to avoid code duplication.
"""
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


async def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text content
    """
    try:
        doc = fitz.open(pdf_path)
        text_parts = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            # Add page number information to the text
            text_with_page = f"[PAGE_{page_num + 1}] {text}"
            text_parts.append(text_with_page)

        doc.close()
        return "\n".join(text_parts)
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        raise


async def extract_text_from_file(file_path: str) -> str:
    """
    Extract text content from a file.

    Args:
        file_path: Path to the file

    Returns:
        Extracted text content
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Handle different file types
    if file_path.suffix.lower() == '.pdf':
        return await extract_text_from_pdf(str(file_path))
    elif file_path.suffix.lower() in ['.txt', '.md', '.rst']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Try to read as text file
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()