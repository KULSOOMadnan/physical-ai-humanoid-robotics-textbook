# ADR-2: Content Chunking Strategy

## Status
Accepted

## Date
2025-12-16

## Context
We need to process book content for RAG retrieval. The way we chunk the content affects retrieval accuracy and semantic coherence. Different chunking strategies have tradeoffs between preserving meaning and maintaining consistent processing.

## Decision
We will use sentence-aware chunking with overlap as our content chunking strategy.

## Alternatives Considered
- Fixed-size token chunks: Split content into fixed token-length segments
- Paragraph-based chunks: Use paragraphs as natural chunk boundaries

## Consequences
### Positive
- Better semantic coherence as sentences maintain their meaning
- Preserves natural language boundaries which improves retrieval relevance
- Overlap helps ensure context isn't lost at chunk boundaries
- Works well with book content that has natural sentence structure

### Negative
- Less uniform chunk sizes compared to fixed-token approaches
- May result in some chunks being very small or very large
- Overlap increases storage requirements and potential redundancy
- More complex implementation than simple fixed-size chunking

## References
- plan.md: Decision 2: Content Chunking Strategy
- spec.md: Requirements for content processing and retrieval