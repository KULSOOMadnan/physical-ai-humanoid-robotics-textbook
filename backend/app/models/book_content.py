from sqlalchemy import Column, String, Text, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import List, Dict, Any, Optional

Base = declarative_base()


class BookContent(Base):
    """
    Model representing processed book content for RAG system.
    """
    __tablename__ = "book_content"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)  # Full book content
    chunks = Column(ARRAY(String), nullable=True)  # Processed content chunks
    book_metadata = Column(JSONB, nullable=True)  # Book metadata (author, publication, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())