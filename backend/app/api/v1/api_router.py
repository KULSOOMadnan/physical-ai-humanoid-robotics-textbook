from fastapi import APIRouter
from app.api.v1.routes import query, upload, session, book_connect


# Main API router for version 1
api_router = APIRouter()

# Include API routes
api_router.include_router(
    query.router,
    prefix="/query",
    tags=["query"]
)

api_router.include_router(
    upload.router,
    prefix="/upload",
    tags=["upload"]
)

api_router.include_router(
    session.router,
    prefix="/session",
    tags=["session"]
)

api_router.include_router(
    book_connect.router,
    prefix="/book-connect",
    tags=["book-connect"]
)