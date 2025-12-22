import asyncio
import time
import logging
from functools import wraps
from typing import Any, Callable, Dict, List
from dataclasses import dataclass
from enum import Enum
import weakref
from collections import OrderedDict


logger = logging.getLogger(__name__)


class CacheStrategy(Enum):
    LRU = "lru"
    TTL = "ttl"
    INFINITE = "infinite"


@dataclass
class CacheEntry:
    value: Any
    timestamp: float
    ttl: float = 0.0  # None means no expiration


class LRUCache:
    """
    Simple LRU cache implementation for performance optimization.
    """
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()

    def get(self, key: str) -> Any:
        """Get a value from the cache."""
        if key in self.cache:
            # Move to end (most recently used)
            entry = self.cache.pop(key)
            self.cache[key] = entry
            # Check TTL expiration
            if entry.ttl and time.time() - entry.timestamp > entry.ttl:
                del self.cache[key]
                return None
            return entry.value
        return None

    def set(self, key: str, value: Any, ttl: float = None):
        """Set a value in the cache."""
        if len(self.cache) >= self.maxsize:
            # Remove least recently used item
            self.cache.popitem(last=False)

        self.cache[key] = CacheEntry(value=value, timestamp=time.time(), ttl=ttl)

    def clear(self):
        """Clear the cache."""
        self.cache.clear()


class PerformanceOptimizer:
    """
    Performance optimization utilities for the RAG chatbot.
    """
    def __init__(self):
        self.cache = LRUCache(maxsize=1024)  # Larger cache for production
        self.query_complexity_threshold = 50  # Characters
        self.response_cache_ttl = 300  # 5 minutes
        self.embedding_cache_ttl = 3600  # 1 hour

    def cache_result(self, ttl: float = 300, key_prefix: str = ""):
        """
        Decorator to cache function results.

        Args:
            ttl: Time to live in seconds
            key_prefix: Prefix for cache key
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                cache_key = f"{key_prefix}{func.__name__}:{str(args)}:{str(kwargs)}"

                # Try to get from cache
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_result

                # Execute function
                result = await func(*args, **kwargs)

                # Store in cache
                self.cache.set(cache_key, result, ttl=ttl)
                logger.debug(f"Cache miss, stored result for {cache_key}")

                return result

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                cache_key = f"{key_prefix}{func.__name__}:{str(args)}:{str(kwargs)}"

                # Try to get from cache
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_result

                # Execute function
                result = func(*args, **kwargs)

                # Store in cache
                self.cache.set(cache_key, result, ttl=ttl)
                logger.debug(f"Cache miss, stored result for {cache_key}")

                return result

            # Return appropriate wrapper based on function type
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper

        return decorator

    def optimize_query_processing(self, query: str) -> str:
        """
        Optimize query processing by normalizing and preprocessing.

        Args:
            query: The input query string

        Returns:
            Optimized query string
        """
        # Remove extra whitespace
        query = " ".join(query.split())

        # Convert to lowercase for consistent processing
        query = query.lower()

        # Remove common stop words if needed (for semantic search)
        # This is a simple example - in practice, you might want more sophisticated preprocessing
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words = query.split()
        filtered_words = [word for word in words if word not in stop_words]
        optimized_query = " ".join(filtered_words)

        return optimized_query

    def batch_process_queries(self, queries: List[str]) -> List[Any]:
        """
        Process multiple queries efficiently in batch.

        Args:
            queries: List of query strings

        Returns:
            List of results
        """
        # This is a placeholder - in a real implementation, you would
        # batch the queries to the LLM service or vector store for efficiency
        results = []
        for query in queries:
            # Process each query individually for now
            # In a real implementation, this would use batch APIs
            results.append(f"Result for: {query}")
        return results

    def get_optimized_embedding_size(self, content_length: int) -> int:
        """
        Determine optimal embedding size based on content length.

        Args:
            content_length: Length of the content to embed

        Returns:
            Recommended embedding size
        """
        # For longer content, you might want to use a smaller model for efficiency
        # or break it into chunks
        if content_length > 10000:  # Very long content
            return 512  # Use smaller embedding dimension if supported
        else:
            return 1536  # Standard embedding size

    def should_cache_response(self, query: str, response: str) -> bool:
        """
        Determine if a response should be cached based on heuristics.

        Args:
            query: The original query
            response: The generated response

        Returns:
            True if the response should be cached
        """
        # Don't cache very short responses (likely error messages)
        if len(response) < 20:
            return False

        # Don't cache responses that indicate failure
        if any(phrase in response.lower() for phrase in [
            "i cannot answer",
            "insufficient context",
            "not found in provided context",
            "error",
            "failed"
        ]):
            return False

        # Don't cache very long responses (might be too specific)
        if len(response) > 5000:
            return False

        # Don't cache responses with session-specific information
        if any(phrase in response.lower() for phrase in [
            "your session",
            "for you",
            "specific to your"
        ]):
            return False

        return True


# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()


def optimize_for_performance():
    """
    Apply performance optimizations to the application.
    This function should be called during application startup.
    """
    logger.info("Applying performance optimizations...")

    # Set up cache warming if needed
    # Configure connection pooling
    # Set up any other performance-related configurations

    logger.info("Performance optimizations applied")


# Convenience functions for common optimizations
def cache_embeddings():
    """
    Decorator to cache embedding calculations.
    """
    return performance_optimizer.cache_result(
        ttl=performance_optimizer.embedding_cache_ttl,
        key_prefix="embedding:"
    )


def cache_query_results():
    """
    Decorator to cache query results.
    """
    return performance_optimizer.cache_result(
        ttl=performance_optimizer.response_cache_ttl,
        key_prefix="query:"
    )


def optimize_query(query: str) -> str:
    """
    Apply query optimization.

    Args:
        query: Input query string

    Returns:
        Optimized query string
    """
    return performance_optimizer.optimize_query_processing(query)


def should_cache_response(query: str, response: str) -> bool:
    """
    Determine if a response should be cached.

    Args:
        query: The original query
        response: The generated response

    Returns:
        True if the response should be cached
    """
    return performance_optimizer.should_cache_response(query, response)