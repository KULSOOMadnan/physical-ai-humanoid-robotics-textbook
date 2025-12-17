import logging
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import tempfile
import os
from urllib.parse import urlparse
from app.models.book_content import BookContent
from app.services.vector_store import vector_store_service
from app.utils.text_chunker import TextChunker
from app.models.retrieved_chunk import RetrievedChunk
from app.config.database import SessionLocal
from sqlalchemy.orm import Session
from app.config.qdrant import qdrant_config
import hashlib


logger = logging.getLogger(__name__)


class BookContentProcessor:
    """
    Service for processing book content and indexing it in the vector store.
    Supports various formats including PDF, text files, GitHub URLs, and other web sources.
    """

    def __init__(self):
        self.text_chunker = TextChunker()

    async def process_book_content(
        self,
        book_title: str,
        content_source: str,
        source_type: str = "file",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process book content from various sources and index it in the vector store.

        Args:
            book_title: Title of the book
            content_source: Path to file or URL to content
            source_type: Type of source ("file", "url", "text")
            metadata: Additional metadata about the book

        Returns:
            Book ID for the processed content
        """
        try:
            # Determine content based on source type
            content = await self._extract_content(content_source, source_type)

            # Generate a unique book ID based on title and content hash
            content_hash = hashlib.md5(content.encode()).hexdigest()
            book_id = f"{book_title.replace(' ', '_')}_{content_hash[:8]}"

            # Chunk the content
            chunks = self.text_chunker.chunk_text(content, book_title)

            # Index each chunk in the vector store
            documents = []
            for i, chunk in enumerate(chunks):
                doc_id = f"{book_id}_chunk_{i}"
                doc_metadata = {
                    "source": f"book:{book_id}#chunk:{i}",
                    "book_id": book_id,
                    "chunk_id": i,
                    "title": book_title,
                    "original_content_source": content_source
                }
                # Add any additional metadata
                if metadata:
                    doc_metadata.update(metadata)

                documents.append({
                    "id": doc_id,
                    "content": chunk,
                    "metadata": doc_metadata
                })

            # Batch add all documents to vector store
            await vector_store_service.batch_add_documents(documents)

            # Store book metadata in the database
            await self._store_book_metadata(book_id, book_title, content, metadata)

            logger.info(f"Successfully processed and indexed book: {book_title} ({book_id}) with {len(chunks)} chunks")
            return book_id

        except Exception as e:
            logger.error(f"Error processing book content: {str(e)}")
            raise

    async def _extract_content(self, source: str, source_type: str) -> str:
        """
        Extract text content from various sources.

        Args:
            source: Path to file, URL, or raw text
            source_type: Type of source ("file", "url", "text")

        Returns:
            Extracted text content
        """
        if source_type == "file":
            return await self._extract_from_file(source)
        elif source_type == "url":
            return await self._extract_from_url(source)
        elif source_type == "text":
            return source
        else:
            raise ValueError(f"Unsupported source type: {source_type}")

    async def _extract_from_file(self, file_path: str) -> str:
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
            return await self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.txt', '.md', '.rst']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Try to read as text file
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

    async def _extract_from_pdf(self, pdf_path: Path) -> str:
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

    async def _extract_from_url(self, url: str) -> str:
        """
        Extract text content from a URL, with special handling for GitHub URLs.

        Args:
            url: URL to extract content from

        Returns:
            Extracted text content
        """
        try:
            parsed_url = urlparse(url)

            # Special handling for GitHub URLs
            if 'github.com' in parsed_url.netloc:
                content = await self._extract_from_github_url(url)
            elif 'raw.githubusercontent.com' in parsed_url.netloc:
                # Direct link to raw content
                response = requests.get(url)
                response.raise_for_status()
                content = response.text
            else:
                # Standard URL handling
                response = requests.get(url)
                response.raise_for_status()

                content_type = response.headers.get('content-type', '').lower()
                if 'application/pdf' in content_type:
                    # Download PDF to temporary file and process
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(response.content)
                        tmp_path = tmp_file.name
                    try:
                        content = await self._extract_from_pdf(Path(tmp_path))
                    finally:
                        os.unlink(tmp_path)
                else:
                    # For HTML content, extract text properly
                    if 'text/html' in content_type:
                        content = await self._extract_from_webpage_content(response.text)
                    else:
                        content = response.text

            return content
        except Exception as e:
            logger.error(f"Error extracting content from URL {url}: {str(e)}")
            raise

    async def _extract_from_github_url(self, github_url: str) -> str:
        """
        Extract content from a GitHub URL (repository/file link).

        Args:
            github_url: GitHub URL to extract content from

        Returns:
            Extracted text content
        """
        # Convert github.com URL to raw.githubusercontent.com URL
        # Example: https://github.com/user/repo/blob/main/file.md
        # Becomes: https://raw.githubusercontent.com/user/repo/main/file.md
        raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        response = requests.get(raw_url)
        response.raise_for_status()

        return response.text

    async def _extract_from_webpage_content(self, html_content: str) -> str:
        """
        Extract text content from HTML content.

        Args:
            html_content: Raw HTML content

        Returns:
            Extracted text content
        """
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    async def _store_book_metadata(
        self,
        book_id: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Store book metadata in the database.

        Args:
            book_id: Unique identifier for the book
            title: Book title
            content: Full book content
            metadata: Additional metadata
        """
        db = SessionLocal()
        try:
            # Check if book already exists
            existing_book = db.query(BookContent).filter(BookContent.id == book_id).first()

            if existing_book:
                # Update existing book
                existing_book.title = title
                existing_book.content = content
                existing_book.book_metadata = metadata or {}
                existing_book.chunks = []  # This will be handled by vector store
            else:
                # Create new book entry
                book_entry = BookContent(
                    id=book_id,
                    title=title,
                    content=content,
                    book_metadata=metadata or {},
                    chunks=[]  # This will be handled by vector store
                )
                db.add(book_entry)

            db.commit()
            logger.info(f"Book metadata stored for {book_id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error storing book metadata: {str(e)}")
            raise
        finally:
            db.close()

    async def process_book_from_file(self, file_path: str, title: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Convenience method to process a book from a file.

        Args:
            file_path: Path to the book file
            title: Title of the book
            metadata: Additional metadata about the book

        Returns:
            Book ID for the processed content
        """
        return await self.process_book_content(
            book_title=title,
            content_source=file_path,
            source_type="file",
            metadata=metadata
        )

    async def process_book_from_text(self, title: str, text_content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Convenience method to process a book from raw text.

        Args:
            title: Title of the book
            text_content: Raw text content of the book
            metadata: Additional metadata about the book

        Returns:
            Book ID for the processed content
        """
        return await self.process_book_content(
            book_title=title,
            content_source=text_content,
            source_type="text",
            metadata=metadata
        )

    async def list_available_books(self) -> List[Dict[str, Any]]:
        """
        List all available books in the system.

        Returns:
            List of book information
        """
        db = SessionLocal()
        try:
            books = db.query(BookContent).all()
            return [
                {
                    "id": book.id,
                    "title": book.title,
                    "book_metadata": book.book_metadata,
                    "created_at": book.created_at,
                    "updated_at": book.updated_at
                }
                for book in books
            ]
        finally:
            db.close()

    async def delete_book(self, book_id: str) -> bool:
        """
        Delete a book and its indexed content.

        Args:
            book_id: ID of the book to delete

        Returns:
            True if successful, False otherwise
        """
        # First delete from vector store
        await vector_store_service.delete_book_content(book_id)

        # Then delete from database
        db = SessionLocal()
        try:
            book = db.query(BookContent).filter(BookContent.id == book_id).first()
            if book:
                db.delete(book)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting book {book_id}: {str(e)}")
            return False
        finally:
            db.close()


# Global book content processor instance
book_content_processor = BookContentProcessor()