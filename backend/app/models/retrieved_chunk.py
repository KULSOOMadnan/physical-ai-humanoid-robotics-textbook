from sqlalchemy import Column, String, Text, DateTime, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class RetrievedChunk(Base):
    """
    Model representing a chunk of content retrieved during query processing.
    """
    __tablename__ = "retrieved_chunks"

    id = Column(String, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # Retrieved text content
    source = Column(String, nullable=False)  # Reference to book section
    relevance_score = Column(Float, nullable=False)  # Similarity score
    page_number = Column(Integer, nullable=True)  # Page number where content was found
    section_title = Column(String, nullable=True)  # Section title where content was found
    chunk_metadata = Column(JSONB, nullable=True)  # Additional metadata about the chunk
    session_id = Column(String, ForeignKey("query_sessions.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())