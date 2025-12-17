from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime
from app.schemas.query import SessionResponse, QueryMode
from app.services.session_manager import session_manager
from app.config.database import SessionLocal, get_db
from app.core.exceptions import SessionNotFoundError


router = APIRouter()


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, db: SessionLocal = Depends(get_db)):
    """
    Get session details by session ID.
    """
    try:
        session = await session_manager.get_session(db, session_id)

        if not session:
            raise SessionNotFoundError(f"Session with ID {session_id} not found")

        # Return session details
        return SessionResponse(
            session_id=session.id,
            user_id=session.user_id,
            selected_text=session.selected_text,
            query_mode=session.query_mode,
            created_at=session.created_at,
            updated_at=session.updated_at,
            history=[]  # For now, return empty history - would need to implement query history storage
        )
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail=f"Session with ID {session_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {str(e)}")


@router.put("/{session_id}")
async def update_session(
    session_id: str,
    mode: Optional[QueryMode] = None,
    selected_text: Optional[str] = None,
    user_id: Optional[str] = None,
    db: SessionLocal = Depends(get_db)
):
    """
    Update session properties.
    """
    try:
        updated_session = await session_manager.update_session(
            db, session_id, mode, selected_text, user_id
        )

        if not updated_session:
            raise SessionNotFoundError(f"Session with ID {session_id} not found")

        return {
            "session_id": updated_session.id,
            "user_id": updated_session.user_id,
            "selected_text": updated_session.selected_text,
            "query_mode": updated_session.query_mode,
            "updated_at": updated_session.updated_at
        }
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail=f"Session with ID {session_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating session: {str(e)}")


@router.delete("/{session_id}")
async def delete_session(session_id: str, db: SessionLocal = Depends(get_db)):
    """
    Delete a session.
    """
    try:
        success = await session_manager.delete_session(db, session_id)

        if not success:
            raise SessionNotFoundError(f"Session with ID {session_id} not found")

        return {"message": f"Session {session_id} deleted successfully"}
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail=f"Session with ID {session_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")


@router.post("/clear_selected_text/{session_id}")
async def clear_selected_text(session_id: str, db: SessionLocal = Depends(get_db)):
    """
    Clear the selected text for a session.
    """
    try:
        session = await session_manager.clear_selected_text(db, session_id)

        if not session:
            raise SessionNotFoundError(f"Session with ID {session_id} not found")

        return {
            "session_id": session.id,
            "selected_text": session.selected_text,
            "message": "Selected text cleared successfully"
        }
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail=f"Session with ID {session_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing selected text: {str(e)}")