# ADR-1: RAG Architecture Pattern

## Status
Accepted

## Date
2025-12-16

## Context
We need to implement a Retrieval-Augmented Generation (RAG) system for a chatbot that answers user questions using book content. The system must support both global book content queries and selected-text-only mode. We need to choose an architecture pattern that balances accuracy, latency, and maintainability.

## Decision
We will use Retrieval-augmented generation with agent orchestration as the core architecture pattern.

## Alternatives Considered
- Simple prompt injection: Inject book content directly into LLM prompts
- Fine-tuning: Train a model specifically on the book content
- External knowledge base: Use a separate system to manage knowledge retrieval

## Consequences
### Positive
- Better accuracy than simple prompt injection as the system can retrieve relevant context
- More cost-effective than fine-tuning which requires significant training resources
- Flexible architecture that can support both global and selected-text-only modes
- Allows for verification that responses are grounded in retrieved context

### Negative
- Higher latency compared to simple prompt injection due to retrieval step
- More complex architecture requiring coordination between components
- Requires careful management of context length and token usage

## References
- plan.md: Decision 1: RAG Architecture Pattern
- spec.md: Requirements for global and selected-text-only query modes