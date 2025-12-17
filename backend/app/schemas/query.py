from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class QueryMode(str, Enum):
    """Enumeration of query modes."""
    GLOBAL = "global"
    SELECTED_TEXT_ONLY = "selected-text-only"


class QueryRequest(BaseModel):
    """Request schema for query endpoint."""
    query: str = Field(..., min_length=1, max_length=2000, description="The question to ask about the book content")
    mode: QueryMode = Field(QueryMode.GLOBAL, description="The query mode to use")
    selected_text: Optional[str] = Field(None, max_length=10000, description="Text selected by user for selected-text-only mode")
    session_id: Optional[str] = Field(None, description="Session ID to maintain context")


class SourceAttribution(BaseModel):
    """Schema for source attribution in responses."""
    content: str = Field(..., description="The content that was used as source")
    source: str = Field(..., description="Reference to where the content came from (e.g., book section)")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score of this source")
    page_number: Optional[int] = Field(None, description="Page number where the content was found")
    section_title: Optional[str] = Field(None, description="Section title where the content was found")
    citation: Optional[str] = Field(None, description="Formatted citation for the source")


class QueryResponse(BaseModel):
    """Response schema for query endpoint."""
    response: str = Field(..., description="The generated response to the query")
    sources: List[SourceAttribution] = Field(..., description="List of sources used to generate the response")
    session_id: str = Field(..., description="Session ID for maintaining context")
    timestamp: datetime = Field(..., description="Timestamp of the response")
    mode: QueryMode = Field(..., description="The query mode that was used")


class QueryHistoryItem(BaseModel):
    """Schema for a single query history item."""
    query: str
    response: str
    sources: List[SourceAttribution]
    timestamp: datetime
    mode: QueryMode


class SessionResponse(BaseModel):
    """Response schema for session endpoint."""
    session_id: str
    user_id: Optional[str] = None
    selected_text: Optional[str] = None
    query_mode: QueryMode = QueryMode.GLOBAL
    created_at: datetime
    updated_at: datetime
    history: List[QueryHistoryItem] = Field(default_factory=list)