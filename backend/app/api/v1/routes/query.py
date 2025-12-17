from fastapi import APIRouter, Depends
from typing import Optional
import uuid
from datetime import datetime
from app.schemas.query import QueryRequest, QueryResponse, QueryMode
from app.services.query_processor import query_processor
from app.services.session_manager import session_manager
from app.services.llm_service import llm_service
from app.config.database import SessionLocal
from app.core.exceptions import RAGException, ContextInsufficientError


router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query against the book content and return a response with sources.
    """
    # Generate a session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())

    try:
        # Get database session
        db = SessionLocal()
        try:
            # Update session if it exists, or create a new one
            session = await session_manager.get_or_create_session(
                db,
                session_id,
                request.mode,
                request.selected_text
            )
        finally:
            db.close()

        # Process the query using the query processor
        response_text, sources = await query_processor.process_query(
            query=request.query,
            session_id=session_id,
            mode=request.mode,
            selected_text=request.selected_text
        )

        # Create and return the response
        response = QueryResponse(
            response=response_text,
            sources=sources,
            session_id=session_id,
            timestamp=datetime.now(),
            mode=request.mode
        )

        return response

    except ContextInsufficientError as e:
        # Handle case where there's insufficient context to answer
        return QueryResponse(
            response="I cannot answer this question based on the provided context.",
            sources=[],
            session_id=session_id,
            timestamp=datetime.now(),
            mode=request.mode
        )
    except RAGException as e:
        # Handle other RAG-specific exceptions
        raise e
    except Exception as e:
        # Handle any other exceptions
        raise RAGException(f"Error processing query: {str(e)}")