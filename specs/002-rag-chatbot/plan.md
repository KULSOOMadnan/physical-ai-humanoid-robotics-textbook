# Implementation Plan: Integrated RAG Chatbot for Embedded Book Intelligence

**Feature**: Integrated RAG Chatbot Development
**Created**: 2025-12-15
**Status**: Draft
**Branch**: 001-rag-chat

## Technical Context

**Problem**: Need to build and embed a Retrieval-Augmented Generation (RAG) chatbot within a published book that answers user questions using book content and supports a strict mode where answers are generated only from user-selected text.

**Solution approach**:
- Backend API using FastAPI
- Vector database for content retrieval using Qdrant Cloud
- Relational database for session management using Neon Serverless PostgreSQL
- AI orchestration using OpenAI Agents SDK / ChatKit SDKs

**Unknowns**:
- Specific book content format and structure
- Exact embedding model selection
- Performance requirements for large books

## Constitution Check

Based on project principles, this implementation will:
- Prioritize user privacy and data protection
- Follow clean architecture principles
- Ensure scalable and maintainable code
- Implement proper error handling and observability

## Gates

**Passed**:
- Feature specification exists and is reasonably complete
- Required technologies are available and compatible
- Clear success criteria defined

**Pending**:
- Performance requirements need to be validated
- Security requirements need to be detailed

---

## Phase 0: Research & Discovery

### Research Tasks

1. **OpenAI Agents SDK / ChatKit SDKs Integration**
   - Task: Research best practices for implementing RAG with OpenAI Agents
   - Expected outcome: Understanding of agent orchestration patterns for RAG

2. **Qdrant Cloud Implementation**
   - Task: Research Qdrant Cloud setup for semantic search
   - Expected outcome: Understanding of vector storage and retrieval patterns

3. **FastAPI Backend Architecture**
   - Task: Research FastAPI patterns for RAG applications
   - Expected outcome: Understanding of API design for RAG systems

4. **Content Processing Strategy**
   - Task: Research best practices for processing book content for RAG
   - Expected outcome: Understanding of chunking, indexing, and retrieval strategies

### Research Outcomes

**Decision**: Use OpenAI Assistants API for agent orchestration
**Rationale**: Better suited for RAG applications than basic Chat completions
**Alternatives considered**: LangChain agents, basic OpenAI Chat API

**Decision**: Implement hybrid search (semantic + keyword) in Qdrant
**Rationale**: Provides better retrieval accuracy than semantic-only search
**Alternatives considered**: Pure semantic search, Elasticsearch

**Decision**: Use async FastAPI for better performance under load
**Rationale**: RAG operations are inherently I/O bound with embedding and LLM calls
**Alternatives considered**: Synchronous API, other frameworks

---

## Phase 1: Foundation & Architecture

### High-level Architecture Sketch

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
                                │
                                ▼
                       ┌──────────────────┐
                       │  Generated       │
                       │  Response        │
                       └──────────────────┘
```

### Data Model

**BookContent**:
- id: string (unique identifier)
- title: string (book title)
- content: text (processed book text)
- chunks: array of text (processed content chunks)
- metadata: object (author, publication, etc.)

**QuerySession**:
- id: string (session identifier)
- userId: string (user identifier)
- selectedText: string (text selected by user for mode 2)
- queryMode: enum (global | selected-text-only)
- createdAt: timestamp
- updatedAt: timestamp

**RetrievedChunk**:
- id: string (chunk identifier)
- content: text (retrieved text)
- source: string (book section reference)
- relevanceScore: float (similarity score)
- sessionId: string (foreign key to QuerySession)

### API Contracts

**POST /api/v1/query**
- Request: {query: string, mode: "global" | "selected-text-only", selectedText?: string}
- Response: {response: string, sources: array, timestamp: string}
- Auth: Optional user authentication

**POST /api/v1/upload-book**
- Request: {file: binary, title: string, metadata: object}
- Response: {bookId: string, status: "processing" | "complete"}
- Auth: Required admin access

**GET /api/v1/session/{sessionId}**
- Response: {session: object, history: array}
- Auth: User must own session

### Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py         # Application settings and configuration
│   │   └── database.py         # Database connection setup
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── query.py    # Query processing endpoints
│   │   │   │   ├── upload.py   # Book upload endpoints
│   │   │   │   └── session.py  # Session management endpoints
│   │   │   └── api_router.py   # Main API router
│   │   └── deps.py             # Dependency injection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book_content.py     # Book content data models
│   │   ├── query_session.py    # Query session models
│   │   └── retrieved_chunk.py  # Retrieved chunk models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── query.py            # Query request/response schemas
│   │   ├── book.py             # Book upload schemas
│   │   └── session.py          # Session schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── content_processor.py # Content processing service
│   │   ├── query_processor.py  # Query processing service
│   │   ├── session_manager.py  # Session management service
│   │   ├── vector_store.py     # Vector store operations
│   │   └── llm_service.py      # LLM interaction service
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── text_chunker.py     # Text chunking utilities
│   │   ├── embeddings.py       # Embedding generation utilities
│   │   └── validators.py       # Input validation utilities
│   └── core/
│       ├── __init__.py
│       ├── security.py         # Authentication and security
│       └── exceptions.py       # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_query.py       # Query endpoint tests
│   │   ├── test_upload.py      # Upload endpoint tests
│   │   └── test_session.py     # Session endpoint tests
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── test_content_processor.py
│   │   ├── test_query_processor.py
│   │   └── test_session_manager.py
│   └── test_utils/
│       ├── __init__.py
│       └── test_text_chunker.py
├── pyproject.toml              # Project dependencies and configuration (uv managed)
├── uv.lock                     # Lock file for reproducible builds (uv managed)
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Docker compose configuration
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # Backend service documentation
```

### Section and Deliverable Structure

1. **Content Processing Module** (`backend/app/services/content_processor.py`)
   - Document parsing and chunking
   - Embedding generation
   - Vector storage in Qdrant

2. **Query Processing Module** (`backend/app/services/query_processor.py`)
   - Mode selection handling
   - Context retrieval
   - Response generation

3. **Session Management Module** (`backend/app/services/session_manager.py`)
   - User session tracking
   - Query history
   - Selected text storage

4. **API Layer** (`backend/app/api/v1/routes/`)
   - FastAPI endpoints
   - Request validation
   - Response formatting

---

## Phase 2: Analysis & Design

### Research-Concurrent Approach

The research will happen concurrently with implementation:
- Week 1: Basic RAG pipeline with minimal viable API
- Week 2: Mode switching and selected-text-only functionality
- Week 3: Performance optimization and testing
- Week 4: Deployment and validation

### Key Technical Decisions

**Decision 1: RAG Architecture Pattern**
- **Chosen**: Retrieval-augmented generation with agent orchestration
- **Alternatives**: Simple prompt injection, fine-tuning, external knowledge base
- **Tradeoffs**: Higher latency but better accuracy vs. lower latency but less accuracy

**Decision 2: Content Chunking Strategy**
- **Chosen**: Sentence-aware chunking with overlap
- **Alternatives**: Fixed-size token chunks, paragraph-based chunks
- **Tradeoffs**: Better semantic coherence vs. more uniform chunk sizes

**Decision 3: Vector Search Configuration**
- **Chosen**: Cosine similarity with hybrid search
- **Alternatives**: Euclidean distance, Max Inner Product
- **Tradeoffs**: Better semantic matching vs. computational efficiency

**Decision 4: Session State Management**
- **Chosen**: Database-stored sessions with TTL
- **Alternatives**: In-memory cache, client-side storage
- **Tradeoffs**: Persistence and scalability vs. performance

### Quality Validation and Acceptance Checks

1. **Retrieval Accuracy Validation**
   - Test: Compare retrieved chunks against known relevant sections
   - Target: 90% precision at k=3 (top 3 retrieved chunks contain relevant info)

2. **Hallucination Prevention Checks**
   - Test: Verify responses only contain information from retrieved context
   - Target: 0% hallucination rate on test queries

3. **Selected-text-only Mode Validation**
   - Test: Ensure responses only use user-selected text
   - Target: 100% compliance with scope restriction

4. **Refusal-to-answer Validation**
   - Test: Verify system refuses to answer when context unavailable
   - Target: 100% correct refusal behavior

5. **Performance Validation**
   - Test: Response time under various query loads
   - Target: <5 seconds for 95% of queries

---

## Phase 3: Synthesis & Implementation

### Implementation Plan

**Foundation Layer**:
- Set up FastAPI application structure
- Configure Qdrant Cloud connection
- Set up Neon PostgreSQL connection
- Implement basic document processing pipeline

**Core Functionality**:
- Implement content indexing and retrieval
- Build OpenAI agent orchestration
- Add mode switching (global vs selected-text)
- Implement source attribution

**Validation Layer**:
- Add hallucination detection
- Implement context scope validation
- Add performance monitoring
- Create test suite

**Deployment**:
- Containerize application
- Set up CI/CD pipeline
- Configure cloud deployment
- Add observability and logging

### Testing and Validation Strategy

**Unit Tests**:
- Content chunking algorithms
- Vector similarity calculations
- Agent response generation
- Session management logic

**Integration Tests**:
- End-to-end RAG pipeline
- Mode switching functionality
- Database operations
- API endpoint validation

**Acceptance Tests**:
- User story validation
- Success criteria verification
- Edge case handling
- Performance benchmarks

**Load Tests**:
- Concurrent user handling
- Large document processing
- Vector search performance
- API response times under load

### Technical Constraints Implementation

1. **Retrieval Before Generation**:
   - Enforce in agent orchestration flow
   - Validate retrieved context exists before LLM call

2. **Selected-text Mode Bypass**:
   - Implement separate query path for selected-text mode
   - Skip vector search and use only provided text

3. **Grounded Responses**:
   - Implement context verification in response generation
   - Add source attribution to all responses

4. **API-driven Backend**:
   - Design RESTful API endpoints
   - Implement stateless request handling