import logging
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
import fitz  # PyMuPDF
from app.utils.text_chunker import TextChunker
from app.utils.embeddings import EmbeddingGenerator
from app.config.qdrant import get_qdrant_client, get_collection_name
from app.models.book_content import BookContent
from app.config.database import SessionLocal
from app.core.exceptions import ContentProcessingError


logger = logging.getLogger(__name__)


class ContentProcessor:
    """
    Service for processing book content: parsing, chunking, and indexing.
    """

    def __init__(self):
        self.text_chunker = TextChunker()
        self.embedding_generator = EmbeddingGenerator()
        self.qdrant_client = get_qdrant_client()
        self.collection_name = get_collection_name()

    async def process_book_content(self,
                                 content: str,
                                 title: str,
                                 book_id: str,
                                 metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process book content by chunking and indexing in Qdrant.

        Args:
            content: Raw book content
            title: Book title
            book_id: Unique identifier for the book
            metadata: Additional metadata about the book

        Returns:
            Dictionary with processing results
        """
        try:
            # Chunk the content
            chunks = self.text_chunker.chunk_text(content)
            logger.info(f"Content chunked into {len(chunks)} pieces")

            # Generate embeddings for chunks
            embeddings = await self.embedding_generator.generate_embeddings(chunks)
            logger.info(f"Generated embeddings for {len(embeddings)} chunks")

            # Prepare points for Qdrant
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = {
                    "id": f"{book_id}_chunk_{i}",
                    "vector": embedding,
                    "payload": {
                        "book_id": book_id,
                        "chunk_id": i,
                        "content": chunk,
                        "title": title,
                        "source": f"book:{book_id}#chunk:{i}"
                    }
                }
                points.append(point)

            # Upload to Qdrant
            self.qdrant_client.upload_points(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Uploaded {len(points)} points to Qdrant collection '{self.collection_name}'")

            # Create database record for the book content
            db = SessionLocal()
            try:
                book_record = BookContent(
                    id=book_id,
                    title=title,
                    content=content,
                    chunks=chunks,
                    metadata=metadata or {}
                )
                db.add(book_record)
                db.commit()
                db.refresh(book_record)
            finally:
                db.close()

            return {
                "book_id": book_id,
                "title": title,
                "chunk_count": len(chunks),
                "total_tokens": sum(len(chunk.split()) for chunk in chunks),
                "status": "processed"
            }

        except Exception as e:
            logger.error(f"Error processing book content: {str(e)}")
            raise ContentProcessingError(f"Failed to process book content: {str(e)}")

    async def process_pdf_file(self,
                             file_path: str,
                             title: str,
                             book_id: str,
                             metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a PDF file by extracting text and indexing content.

        Args:
            file_path: Path to the PDF file
            title: Book title
            book_id: Unique identifier for the book
            metadata: Additional metadata about the book

        Returns:
            Dictionary with processing results
        """
        try:
            # Extract text from PDF
            doc = fitz.open(file_path)
            content = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                content += page.get_text()

            doc.close()

            logger.info(f"Extracted {len(content)} characters from PDF")

            # Process the extracted content
            return await self.process_book_content(content, title, book_id, metadata)

        except Exception as e:
            logger.error(f"Error processing PDF file: {str(e)}")
            raise ContentProcessingError(f"Failed to process PDF file: {str(e)}")

    async def process_text_file(self,
                              file_path: str,
                              title: str,
                              book_id: str,
                              metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a text file by reading content and indexing.

        Args:
            file_path: Path to the text file
            title: Book title
            book_id: Unique identifier for the book
            metadata: Additional metadata about the book

        Returns:
            Dictionary with processing results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            logger.info(f"Read {len(content)} characters from text file")

            # Process the content
            return await self.process_book_content(content, title, book_id, metadata)

        except Exception as e:
            logger.error(f"Error processing text file: {str(e)}")
            raise ContentProcessingError(f"Failed to process text file: {str(e)}")


# Default content processor instance
content_processor = ContentProcessor()