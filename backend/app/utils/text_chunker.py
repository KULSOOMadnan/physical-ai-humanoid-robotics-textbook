import re
from typing import List, Tuple
from typing import Optional


class TextChunker:
    """
    Utility class for chunking text using sentence-aware chunking with overlap.
    This approach preserves semantic coherence by keeping sentences intact.
    """

    def __init__(self, max_chunk_size: int = 512, overlap_size: int = 50):
        """
        Initialize the text chunker with configuration.

        Args:
            max_chunk_size: Maximum size of each chunk in tokens/characters
            overlap_size: Number of tokens/characters to overlap between chunks
        """
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks using sentence-aware chunking with overlap.

        Args:
            text: The input text to chunk

        Returns:
            List of text chunks
        """
        # Split text into sentences
        sentences = self._split_into_sentences(text)

        if not sentences:
            return [text] if text else []

        chunks = []
        current_chunk = ""
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)

            # If adding this sentence would exceed the chunk size
            if current_length + sentence_length > self.max_chunk_size and current_chunk:
                # Save the current chunk
                chunks.append(current_chunk.strip())

                # Start a new chunk with overlap if possible
                if self.overlap_size > 0:
                    # Find overlap text from the end of the current chunk
                    overlap_start = max(0, len(current_chunk) - self.overlap_size)
                    current_chunk = current_chunk[overlap_start:]
                    current_length = len(current_chunk)
                else:
                    current_chunk = ""
                    current_length = 0

            # Add the sentence to the current chunk
            if current_length + sentence_length <= self.max_chunk_size or not current_chunk:
                current_chunk += " " + sentence if current_chunk else sentence
                current_length += sentence_length + (1 if current_chunk != sentence else 0)
            else:
                # If the sentence is too long by itself, split it by length
                chunks.extend(self._split_long_sentence(sentence))

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using regex pattern.

        Args:
            text: Input text to split

        Returns:
            List of sentences
        """
        # Pattern to match sentence endings (., !, ?, etc.) followed by whitespace or end of string
        sentence_pattern = r'[.!?]+\s+|[\n\r]+|(?<!\w\.\w.)(?<![A-Z][a-z].)\s*[.!?]\s+|(?<=[a-z])\.(?=\s+[A-Z])'

        sentences = re.split(sentence_pattern, text)

        # Filter out empty sentences and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    def _split_long_sentence(self, sentence: str) -> List[str]:
        """
        Split a sentence that is too long for a single chunk.

        Args:
            sentence: A sentence that exceeds the chunk size

        Returns:
            List of sentence fragments
        """
        if len(sentence) <= self.max_chunk_size:
            return [sentence]

        # Split the long sentence into smaller chunks
        chunks = []
        start = 0

        while start < len(sentence):
            end = start + self.max_chunk_size
            if end >= len(sentence):
                chunks.append(sentence[start:])
                break

            # Try to break at a space to avoid cutting words
            if sentence[end] != ' ':
                # Find the last space before the end
                space_pos = sentence.rfind(' ', start, end)
                if space_pos != -1 and space_pos > start:
                    chunks.append(sentence[start:space_pos])
                    start = space_pos + 1
                else:
                    # If no space found, just cut at max_chunk_size
                    chunks.append(sentence[start:end])
                    start = end
            else:
                chunks.append(sentence[start:end])
                start = end + 1

        return chunks


# Default text chunker instance
default_chunker = TextChunker()


def chunk_text(text: str, max_chunk_size: int = 512, overlap_size: int = 50) -> List[str]:
    """
    Convenience function to chunk text with default settings.

    Args:
        text: The input text to chunk
        max_chunk_size: Maximum size of each chunk
        overlap_size: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    chunker = TextChunker(max_chunk_size=max_chunk_size, overlap_size=overlap_size)
    return chunker.chunk_text(text)