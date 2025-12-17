from fastapi import APIRouter, HTTPException, Form
from typing import Optional
import json
from pydantic import BaseModel
from app.services.book_content_processor import book_content_processor
from app.core.exceptions import ContentProcessingError


router = APIRouter()


class ConnectBookResponse(BaseModel):
    book_id: str
    title: str
    source_url: str
    chunk_count: int
    status: str


class BookMetadata(BaseModel):
    author: Optional[str] = None
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


@router.post("/connect-github", response_model=ConnectBookResponse)
async def connect_github_book(
    url: str = Form(...),
    title: str = Form(...),
    metadata: str = Form("{}")  # JSON string of metadata
):
    """
    Connect a book from a GitHub URL for processing and indexing.
    Supports GitHub repository files and raw GitHub content URLs.
    """
    try:
        # Parse metadata JSON
        try:
            metadata_dict = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid metadata JSON format"
            )

        # Process the book from the GitHub URL
        book_id = await book_content_processor.process_book_content(
            book_title=title,
            content_source=url,
            source_type="url",
            metadata=metadata_dict
        )

        # For now, return a simple response - in a real implementation,
        # we'd have more detailed information from the processing
        return ConnectBookResponse(
            book_id=book_id,
            title=title,
            source_url=url,
            chunk_count=0,  # Would be provided by the processor in full implementation
            status="connected"
        )

    except ContentProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect GitHub book: {str(e)}")


@router.post("/connect-url", response_model=ConnectBookResponse)
async def connect_url_book(
    url: str = Form(...),
    title: str = Form(...),
    metadata: str = Form("{}")  # JSON string of metadata
):
    """
    Connect a book from any URL for processing and indexing.
    Supports various content types including text, markdown, and PDFs.
    """
    try:
        # Parse metadata JSON
        try:
            metadata_dict = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid metadata JSON format"
            )

        # Process the book from the URL
        book_id = await book_content_processor.process_book_content(
            book_title=title,
            content_source=url,
            source_type="url",
            metadata=metadata_dict
        )

        return ConnectBookResponse(
            book_id=book_id,
            title=title,
            source_url=url,
            chunk_count=0,  # Would be provided by the processor in full implementation
            status="connected"
        )

    except ContentProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect book from URL: {str(e)}")


@router.get("/status/{book_id}")
async def get_book_status(book_id: str):
    """
    Get the processing status of a connected book.
    """
    try:
        # This would check the status in a real implementation
        # For now, we'll just return that the book exists
        from app.config.database import SessionLocal
        from app.models.book_content import BookContent

        db = SessionLocal()
        try:
            book = db.query(BookContent).filter(BookContent.id == book_id).first()

            if not book:
                raise HTTPException(status_code=404, detail="Book not found")

            return {
                "book_id": book_id,
                "title": book.title,
                "status": "processed",
                "indexed_chunks": len(book.chunks) if book.chunks else 0,
                "indexed_in_vector_store": True  # Would check actual vector store in real implementation
            }
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get book status: {str(e)}")