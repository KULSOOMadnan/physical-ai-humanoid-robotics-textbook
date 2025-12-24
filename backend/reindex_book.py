#!/usr/bin/env python3
"""
Script to clear existing Qdrant documents and re-index book content from the website
"""
import asyncio
import sys
import os

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.book_content_processor import book_content_processor
from app.services.vector_store import vector_store_service
from app.config.qdrant import qdrant_config
from app.config.settings import get_settings

async def clear_and_reindex_book():
    """Clear existing documents and re-index book content from the website"""
    print("Starting to clear existing documents and re-index book content...")

    # Initialize Qdrant collection with 1024 dimensions for Cohere embeddings
    print("Initializing Qdrant collection with 1024 dimensions...")
    await qdrant_config.initialize_collection(vector_size=1024)

    # Clear existing book content from vector store
    print("Clearing existing book content from vector store...")
    # We'll delete by book_id pattern, but since we don't know the exact book_id,
    # we'll just reinitialize the collection which will clear everything
    await qdrant_config.initialize_collection(vector_size=1024)

    # URL of your book
    book_url = "https://kulsoomadnan.github.io/physical-ai-humanoid-robotics-textbook/"
    book_title = "Physical AI & Humanoid Robotics Textbook"

    print(f"Processing book content from: {book_url}")

    # Process the book content from the URL
    metadata = {
        "source_type": "website",
        "url": book_url,
        "author": "Kulsoom Adnan",
        "category": "AI/Robotics"
    }

    try:
        book_id = await book_content_processor.process_book_content(
            book_title=book_title,
            content_source=book_url,
            source_type="url",
            metadata=metadata
        )

        print(f"Successfully processed and indexed book: {book_title}")
        print(f"Book ID: {book_id}")
        print(f"Content source: {book_url}")

        # Verify that content was indexed
        from app.services.vector_store import vector_store_service
        # Perform a test search to verify content is available
        test_results = vector_store_service.client.count(
            collection_name=qdrant_config.collection_name
        )
        print(f"Total documents in vector store after indexing: {test_results.count}")

    except Exception as e:
        print(f"Error processing book content: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    print("Book content has been successfully re-indexed!")
    return True

if __name__ == "__main__":
    asyncio.run(clear_and_reindex_book())