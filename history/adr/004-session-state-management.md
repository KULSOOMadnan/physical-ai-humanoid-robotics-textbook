# ADR-4: Session State Management

## Status
Accepted

## Date
2025-12-16

## Context
The RAG chatbot needs to maintain session state to track user interactions, selected text for the selected-text-only mode, and query history. We need to choose an approach that balances persistence, scalability, and performance requirements.

## Decision
We will use database-stored sessions with TTL (Time To Live) for session state management.

## Alternatives Considered
- In-memory cache: Store sessions in memory (Redis, etc.)
- Client-side storage: Store session data in client cookies or local storage

## Consequences
### Positive
- Persistence across application restarts and server failures
- Scalability to multiple server instances without sticky sessions
- Ability to query and analyze session data for analytics
- Better security as sensitive session data remains server-side
- TTL ensures automatic cleanup of old sessions

### Negative
- Higher latency compared to in-memory storage
- Additional database load and potential bottlenecks
- More complex implementation than client-side storage
- Requires database transaction management for consistency

## References
- plan.md: Decision 4: Session State Management
- plan.md: Data model section describing QuerySession
- spec.md: Requirements for session tracking and history