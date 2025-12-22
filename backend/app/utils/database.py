"""
Database utilities to reduce code duplication.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.config.database import SessionLocal
from sqlalchemy.orm import Session


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[Session, None]:
    """
    Context manager for database sessions to ensure proper cleanup.

    Usage:
        async with get_db_session() as db:
            # Use db session here
            result = db.query(...)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def execute_in_db_session(func, *args, **kwargs):
    """
    Execute a function within a database session context.

    Args:
        func: The function to execute with a db session
        *args, **kwargs: Arguments to pass to the function

    Returns:
        Result of the function execution
    """
    async with get_db_session() as db:
        return await func(db, *args, **kwargs)