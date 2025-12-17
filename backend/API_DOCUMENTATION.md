# RAG Chatbot API Documentation

## Overview
This API provides a Retrieval-Augmented Generation (RAG) chatbot that allows users to query book content and receive accurate answers based on the provided context.

## Base URL
`/api/v1/`

## Authentication
API endpoints may require authentication using Bearer tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Endpoints

### Health Check
```
GET /health
```
Check if the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

### Query Processing
```
POST /query/
```
Process a query against the book content and return a response with sources.

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

**Error Responses:**
- `400`: Bad request (invalid input)
- `404`: Context insufficient to answer the query
- `500`: Internal server error

### Session Management
```
GET /session/{session_id}
```
Get session details.

**Response:**
```json
{
  "session_id": "string",
  "user_id": "string (optional)",
  "selected_text": "string (optional)",
  "query_mode": "string",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime",
  "history": [
    {
      "query": "string",
      "response": "string",
      "sources": "[SourceAttribution]",
      "timestamp": "ISO 8601 datetime",
      "mode": "string"
    }
  ]
}
```

### Book Upload
```
POST /upload/
```
Upload a book for processing and indexing.

**Request Body:**
```json
{
  "file": "binary file",
  "title": "string",
  "metadata": "object"
}
```

**Response:**
```json
{
  "bookId": "string",
  "status": "string ('processing' | 'complete')"
}
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

## Rate Limiting
The API may implement rate limiting to prevent abuse. Exceeding rate limits will result in a `429 Too Many Requests` response.

## Response Times
Most queries should respond within 5 seconds. Complex queries or large documents may take longer.