# ADR-5: Backend Technology Stack

## Status
Accepted

## Date
2025-12-16

## Context
We need to select the core technologies for the RAG chatbot backend. The chosen stack must support async operations for I/O bound RAG processes, integrate well with our chosen services (Qdrant, OpenAI, Neon PostgreSQL), and provide a solid foundation for the API layer.

## Decision
We will use:
- FastAPI as the web framework for building the API
- OpenAI Assistants API for agent orchestration
- Qdrant Cloud for vector storage and retrieval
- Async operations throughout to handle I/O bound tasks efficiently

## Alternatives Considered
- For web framework: Synchronous frameworks like Flask, other async frameworks
- For agent orchestration: LangChain agents, basic OpenAI Chat API
- For vector storage: Elasticsearch, other vector databases

## Consequences
### Positive
- FastAPI provides excellent async support and automatic API documentation
- OpenAI Assistants API is better suited for RAG applications than basic Chat completions
- Async operations improve performance under load with embedding and LLM calls
- FastAPI has excellent Pydantic integration for request/response validation
- Strong ecosystem and community support

### Negative
- Learning curve for team members unfamiliar with FastAPI
- OpenAI Assistants API has different pricing model than basic API calls
- Async programming can be more complex to debug
- FastAPI async features require careful handling of database connections

## References
- plan.md: Research outcomes section with technology decisions
- plan.md: High-level architecture sketch
- plan.md: API contracts section
- spec.md: Technical requirements for the backend