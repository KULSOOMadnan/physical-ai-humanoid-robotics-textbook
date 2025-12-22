# RAG Chatbot Backend

Backend service for the RAG (Retrieval-Augmented Generation) Chatbot integrated with book intelligence.

## Overview

This backend service provides:
- FastAPI-based API for RAG operations
- Integration with Qdrant vector database for semantic search
- Connection to Neon PostgreSQL for session management
- OpenAI integration for RAG response generation
- Support for two query modes: global book content and selected-text-only

## Setup

1. Install uv package manager:
```bash
pip install uv
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables (copy `.env.example` to `.env` and fill in values)

4. Run the application:
```bash
uv run uvicorn app.main:app --reload
```

## Development

Run tests:
```bash
uv run pytest
```

Format code:
```bash
uv run black .
```

## API Endpoints

### Health Check
- `GET /health` - Check if the service is running

### Query Processing
- `POST /api/v1/query/` - Process a query against the book content and return a response with sources

**Request Body:**
```json
{
  "query": "string (required, 1-2000 characters)",
  "mode": "enum (optional, default: 'global')",
  "selected_text": "string (optional, max 10000 characters)",
  "session_id": "string (optional)"
}
```

**Query Modes:**
- `global`: Search the entire book content
- `selected-text-only`: Only use the provided selected text

**Response:**
```json
{
  "response": "string",
  "sources": [
    {
      "content": "string",
      "source": "string",
      "relevance_score": "number (0.0-1.0)",
      "page_number": "integer (optional)",
      "section_title": "string (optional)",
      "citation": "string (optional)"
    }
  ],
  "session_id": "string",
  "timestamp": "ISO 8601 datetime",
  "mode": "string"
}
```

### Session Management
- `GET /api/v1/session/{session_id}` - Get session details

### Book Upload
- `POST /api/v1/upload/` - Upload a book for processing and indexing

## Authentication
API endpoints may require authentication using Bearer tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Error Handling
The API returns structured error responses:
```json
{
  "status_code": "integer",
  "detail": "string",
  "error_type": "string"
}
```

## Usage Examples

### Basic Query
```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is retrieval augmented generation?",
    "mode": "global"
  }'
```

### Selected Text Query
```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this concept?",
    "mode": "selected-text-only",
    "selected_text": "The concept of retrieval augmented generation combines..."
  }'
```

## Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname

# Qdrant
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your-api-key

# OpenRouter (for OpenAI Agents)
OPENROUTER_API_KEY=your-openrouter-api-key

# Cohere (for embeddings)
COHERE_API_KEY=your-cohere-api-key

# Application
API_KEY=your-api-key-for-authentication
DEBUG=false
```

### Running with Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual services
docker build -t rag-chatbot .
docker run -p 8000:8000 rag-chatbot
```

## Development

### Running Locally
```bash
# Install dependencies with uv
uv sync --dev

# Run the application
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=app
```

### Running Migrations (if using database migrations)
```bash
# Example using alembic (you would need to set this up)
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Performance & Monitoring

The application includes built-in metrics collection using the custom metrics module:
- Query processing duration is tracked automatically
- Error counts are monitored
- Active sessions are tracked
- Memory usage can be monitored (integration required)

To access metrics programmatically, use the `metrics_collector` instance from `app.core.metrics`.

## Security

The application implements:
- JWT-based authentication (optional, configured via API_KEY)
- Secure password hashing with bcrypt
- Input validation using Pydantic
- SQL injection prevention through SQLAlchemy ORM
- Rate limiting (implementation required for production)

## Testing

The application includes comprehensive test coverage:
- Unit tests for individual components
- Integration tests for service interactions
- API endpoint tests
- Attribution accuracy tests

Run all tests with:
```bash
uv run pytest tests/ -v
```

## Architecture

The application follows a service-oriented architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Book Content  │───▶│  Content Index   │───▶│   Qdrant DB     │
│   (PDF/Text)    │    │  (Chunked/       │    │  (Vector Store) │
└─────────────────┘    │   Embedded)      │    └─────────────────┘
                       └──────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   FastAPI API    │───▶│ Neon PostgreSQL │
│                 │    │                  │    │ (Session Data)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ OpenAI Agents    │
                       │ (RAG Pipeline)   │
                       └──────────────────┘
```

Key services include:
- `ContentProcessor`: Handles document parsing, chunking, and indexing
- `QueryProcessor`: Manages query processing flow
- `VectorStoreService`: Handles vector database operations
- `LLMService`: Manages LLM interactions using OpenAI Agents
- `SessionManager`: Manages user sessions
```

## Connecting Your Book from GitHub

The RAG Chatbot supports connecting books directly from GitHub repositories. Here's how to connect your book:

### Method 1: Using the API

Connect your book using the `/book-connect/connect-github` endpoint:

```bash
# Connect a book from a GitHub URL
curl -X POST http://localhost:8000/api/v1/book-connect/connect-github \
  -d "url=https://github.com/your-username/your-repo/blob/main/your-book.md" \
  -d "title=Your Book Title" \
  -d 'metadata={"author": "Your Name", "category": "Technical"}'
```

For raw GitHub content URLs:
```bash
curl -X POST http://localhost:8000/api/v1/book-connect/connect-url \
  -d "url=https://raw.githubusercontent.com/your-username/your-repo/main/your-book.md" \
  -d "title=Your Book Title" \
  -d 'metadata={"author": "Your Name", "category": "Technical"}'
```

### Method 2: Using the Swagger UI

1. Start the application: `uv run uvicorn app.main:app --reload`
2. Navigate to `http://localhost:8000/docs`
3. Find the `/api/v1/book-connect/connect-github` endpoint
4. Fill in your GitHub book URL and title
5. Click "Execute" to connect your book

### Supported GitHub Formats

The system supports various formats when connecting books from GitHub:
- Markdown files (.md)
- Text files (.txt)
- ReStructuredText files (.rst)
- PDF files (though not recommended for GitHub due to binary format)

### Example GitHub URLs

- Repository file: `https://github.com/username/repo/blob/main/book.md`
- Raw content: `https://raw.githubusercontent.com/username/repo/main/book.md`
- GitHub Pages site: `https://kulsoomadnan.github.io/physical-ai-humanoid-robotics-textbook/`

### Connecting Your Specific Book

To connect your Physical AI Humanoid Robotics textbook from GitHub Pages, use the following command:

```bash
curl -X POST http://localhost:8000/api/v1/book-connect/connect-url \
  -d "url=https://kulsoomadnan.github.io/physical-ai-humanoid-robotics-textbook/" \
  -d "title=Physical AI Humanoid Robotics Textbook" \
  -d 'metadata={"author": "Kulsoom Adnan", "category": "AI/Robotics", "description": "A comprehensive guide to humanoid robotics and physical AI"}'
```

After connecting your book, you can query it using the standard query endpoints:

```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main concept of this book?",
    "mode": "global"
  }'
```