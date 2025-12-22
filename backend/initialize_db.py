"""
Database initialization script for the RAG Chatbot
"""
from sqlalchemy import create_engine, text
from app.config.settings import settings
from app.models.book_content import BookContent
from app.models.query_session import QuerySession
from app.models.retrieved_chunk import RetrievedChunk
from app.config.database import engine

def init_db():
    """Initialize the database tables in correct order"""
    try:
        # Create tables in the correct order to respect foreign key constraints
        # 1. First create QuerySession table (referenced by RetrievedChunk)
        QuerySession.__table__.create(bind=engine, checkfirst=True)
        print("[OK] QuerySession table created")

        # 2. Then create BookContent table (no dependencies)
        BookContent.__table__.create(bind=engine, checkfirst=True)
        print("[OK] BookContent table created")

        # 3. Finally create RetrievedChunk table (references QuerySession)
        RetrievedChunk.__table__.create(bind=engine, checkfirst=True)
        print("[OK] RetrievedChunk table created")

        print("\nDatabase initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_db()