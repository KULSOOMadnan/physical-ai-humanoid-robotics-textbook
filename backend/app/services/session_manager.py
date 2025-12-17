import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.query_session import QuerySession, QueryMode
from app.core.exceptions import SessionNotFoundError


logger = logging.getLogger(__name__)


class SessionManager:
    """
    Service for managing user query sessions.
    """

    async def get_or_create_session(
        self,
        db: Session,
        session_id: Optional[str],
        mode: QueryMode = QueryMode.GLOBAL,
        selected_text: Optional[str] = None
    ) -> QuerySession:
        """
        Get an existing session or create a new one.

        Args:
            db: Database session
            session_id: Session identifier (if None, creates a new session)
            mode: Query mode for the session
            selected_text: Selected text for selected-text-only mode

        Returns:
            QuerySession object
        """
        try:
            if session_id:
                # Try to get existing session
                session = db.query(QuerySession).filter(QuerySession.id == session_id).first()
                if session:
                    # Update session properties if provided
                    if mode:
                        session.query_mode = mode
                    if selected_text is not None:
                        session.selected_text = selected_text
                    db.commit()
                    db.refresh(session)
                    return session

            # Create new session
            import uuid
            new_session_id = session_id or str(uuid.uuid4())

            new_session = QuerySession(
                id=new_session_id,
                selected_text=selected_text,
                query_mode=mode
            )

            db.add(new_session)
            db.commit()
            db.refresh(new_session)

            logger.info(f"Created new session: {new_session_id}")

            return new_session

        except SQLAlchemyError as e:
            logger.error(f"Database error in session management: {str(e)}")
            raise SessionNotFoundError(f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Error in get_or_create_session: {str(e)}")
            raise SessionNotFoundError(f"Error managing session: {str(e)}")

    async def get_session(self, db: Session, session_id: str) -> Optional[QuerySession]:
        """
        Get a session by ID.

        Args:
            db: Database session
            session_id: Session identifier

        Returns:
            QuerySession object if found, None otherwise
        """
        try:
            session = db.query(QuerySession).filter(QuerySession.id == session_id).first()
            return session
        except SQLAlchemyError as e:
            logger.error(f"Database error getting session: {str(e)}")
            raise SessionNotFoundError(f"Database error: {str(e)}")

    async def update_session(
        self,
        db: Session,
        session_id: str,
        mode: Optional[QueryMode] = None,
        selected_text: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Optional[QuerySession]:
        """
        Update session properties.

        Args:
            db: Database session
            session_id: Session identifier
            mode: New query mode
            selected_text: New selected text
            user_id: New user ID

        Returns:
            Updated QuerySession object if found, None otherwise
        """
        try:
            session = db.query(QuerySession).filter(QuerySession.id == session_id).first()

            if not session:
                return None

            # Update fields if provided
            if mode is not None:
                session.query_mode = mode
            if selected_text is not None:
                session.selected_text = selected_text
            if user_id is not None:
                session.user_id = user_id

            db.commit()
            db.refresh(session)

            logger.info(f"Updated session: {session_id}")

            return session
        except SQLAlchemyError as e:
            logger.error(f"Database error updating session: {str(e)}")
            raise SessionNotFoundError(f"Database error: {str(e)}")

    async def delete_session(self, db: Session, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            db: Database session
            session_id: Session identifier

        Returns:
            True if successful, False if session not found
        """
        try:
            session = db.query(QuerySession).filter(QuerySession.id == session_id).first()

            if not session:
                return False

            db.delete(session)
            db.commit()

            logger.info(f"Deleted session: {session_id}")

            return True
        except SQLAlchemyError as e:
            logger.error(f"Database error deleting session: {str(e)}")
            raise SessionNotFoundError(f"Database error: {str(e)}")

    async def clear_selected_text(self, db: Session, session_id: str) -> Optional[QuerySession]:
        """
        Clear the selected text for a session.

        Args:
            db: Database session
            session_id: Session identifier

        Returns:
            Updated QuerySession object if found, None otherwise
        """
        try:
            session = db.query(QuerySession).filter(QuerySession.id == session_id).first()

            if not session:
                return None

            session.selected_text = None
            db.commit()
            db.refresh(session)

            logger.info(f"Cleared selected text for session: {session_id}")

            return session
        except SQLAlchemyError as e:
            logger.error(f"Database error clearing selected text: {str(e)}")
            raise SessionNotFoundError(f"Database error: {str(e)}")


# Default session manager instance
session_manager = SessionManager()