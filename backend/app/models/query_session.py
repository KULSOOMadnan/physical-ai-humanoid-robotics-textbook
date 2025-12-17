from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import Optional
import enum

Base = declarative_base()


class QueryMode(str, enum.Enum):
    """Enumeration of query modes supported by the system."""
    GLOBAL = "global"
    SELECTED_TEXT_ONLY = "selected-text-only"


class QuerySession(Base):
    """
    Model representing a user's query session with selected text and mode preferences.
    """
    __tablename__ = "query_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True, index=True)  # Optional user identifier
    selected_text = Column(Text, nullable=True)  # Text selected by user for mode 2
    query_mode = Column(SQLEnum(QueryMode), nullable=False, default=QueryMode.GLOBAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())