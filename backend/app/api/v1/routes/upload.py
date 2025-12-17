from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
import uuid
import json
from app.services.content_processor import content_processor
from app.core.exceptions import ContentProcessingError


router = APIRouter()


class UploadResponse(BaseModel):
    book_id: str
    title: str
    chunk_count: int
    total_tokens: int
    status: str


class BookMetadata(BaseModel):
    author: Optional[str] = None
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


@router.post("/", response_model=UploadResponse)
async def upload_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    metadata: str = Form("{}")  # JSON string of metadata
):
    """
    Upload a book file for processing and indexing.

    Supports PDF and text files.
    """
    try:
        # Validate file type
        if not file.content_type or not any(
            ext in file.content_type for ext in ["application/pdf", "text/plain", "text/csv"]
        ):
            if not any(
                ext in file.filename.lower() for ext in [".pdf", ".txt", ".md"]
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file type. Only PDF and text files are supported."
                )

        # Parse metadata JSON
        try:
            metadata_dict = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid metadata JSON format"
            )

        # Generate unique book ID
        book_id = str(uuid.uuid4())

        # Save file temporarily and process
        file_extension = file.filename.split(".")[-1].lower()
        file_path = f"/tmp/{book_id}.{file_extension}"

        # Write uploaded file to temporary location
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process based on file type
        if file_extension == "pdf":
            result = await content_processor.process_pdf_file(
                file_path=file_path,
                title=title,
                book_id=book_id,
                metadata=metadata_dict
            )
        elif file_extension in ["txt", "md"]:
            result = await content_processor.process_text_file(
                file_path=file_path,
                title=title,
                book_id=book_id,
                metadata=metadata_dict
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file extension: {file_extension}"
            )

        # Clean up temporary file
        import os
        os.remove(file_path)

        return UploadResponse(
            book_id=result["book_id"],
            title=result["title"],
            chunk_count=result["chunk_count"],
            total_tokens=result["total_tokens"],
            status=result["status"]
        )

    except ContentProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")