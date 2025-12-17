import time
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import asyncio
from functools import wraps


logger = logging.getLogger(__name__)


class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """Represents a single metric."""
    name: str
    type: MetricType
    value: float
    labels: Dict[str, str]
    timestamp: datetime


class MetricsCollector:
    """
    Collects and manages application metrics for performance monitoring.
    """
    def __init__(self):
        self._metrics: Dict[str, Metric] = {}
        self._timers: Dict[str, float] = {}
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, list] = {}

    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None, value: float = 1.0):
        """Increment a counter metric."""
        key = f"{name}_{labels or ''}"
        self._counters[key] = self._counters.get(key, 0) + value
        logger.debug(f"Incremented counter {name} to {self._counters[key]}")

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric to a specific value."""
        key = f"{name}_{labels or ''}"
        self._gauges[key] = value
        logger.debug(f"Set gauge {name} to {value}")

    def record_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a value in a histogram."""
        key = f"{name}_{labels or ''}"
        if key not in self._histograms:
            self._histograms[key] = []
        self._histograms[key].append(value)
        logger.debug(f"Recorded histogram value {name} = {value}")

    def start_timer(self, name: str):
        """Start a timer for measuring duration."""
        self._timers[name] = time.time()
        logger.debug(f"Started timer {name}")

    def stop_timer(self, name: str, labels: Optional[Dict[str, str]] = None) -> float:
        """Stop a timer and record the duration."""
        if name not in self._timers:
            logger.warning(f"Timer {name} was not started")
            return 0.0

        duration = time.time() - self._timers[name]
        self.record_histogram(f"{name}_duration_seconds", duration, labels)
        logger.debug(f"Stopped timer {name}, duration: {duration:.3f}s")

        # Clean up the timer
        del self._timers[name]

        return duration

    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        return {
            "counters": self._counters,
            "gauges": self._gauges,
            "histograms": self._histograms,
            "timers": self._timers
        }

    def get_query_performance_metrics(self) -> Dict[str, Any]:
        """Get specific metrics related to query performance."""
        query_duration_key = "query_processing_duration_seconds"
        if query_duration_key in self._histograms:
            durations = self._histograms[query_duration_key]
            if durations:
                return {
                    "count": len(durations),
                    "avg_duration": sum(durations) / len(durations),
                    "min_duration": min(durations),
                    "max_duration": max(durations),
                    "p95_duration": sorted(durations)[int(0.95 * len(durations))] if len(durations) > 0 else 0
                }

        return {
            "count": 0,
            "avg_duration": 0,
            "min_duration": 0,
            "max_duration": 0,
            "p95_duration": 0
        }


# Global metrics collector instance
metrics_collector = MetricsCollector()


def time_it(name: str, labels: Optional[Dict[str, str]] = None):
    """
    Decorator to time function execution and record metrics.
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            metrics_collector.start_timer(name)
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                metrics_collector.stop_timer(name, labels)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            metrics_collector.start_timer(name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                metrics_collector.stop_timer(name, labels)

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def count_calls(name: str, labels: Optional[Dict[str, str]] = None):
    """
    Decorator to count function calls.
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            metrics_collector.increment_counter(name, labels)
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            metrics_collector.increment_counter(name, labels)
            return func(*args, **kwargs)

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def track_memory_usage(name: str = "memory_usage_bytes", labels: Optional[Dict[str, str]] = None):
    """
    Track memory usage (placeholder - in a real implementation,
    this would integrate with a memory profiling library).
    """
    import psutil
    import os

    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    metrics_collector.set_gauge(name, memory_info.rss, labels)
    logger.debug(f"Memory usage tracked: {memory_info.rss} bytes")


# Convenience functions for common metrics
def record_query_duration(duration: float, query_type: str = "global"):
    """Record the duration of a query operation."""
    labels = {"query_type": query_type}
    metrics_collector.record_histogram("query_processing_duration_seconds", duration, labels)


def increment_query_count(query_type: str = "global"):
    """Increment the count of queries processed."""
    labels = {"query_type": query_type}
    metrics_collector.increment_counter("queries_total", labels)


def increment_error_count(error_type: str = "unknown"):
    """Increment the count of errors."""
    labels = {"error_type": error_type}
    metrics_collector.increment_counter("errors_total", labels)


def set_active_sessions_count(count: int):
    """Set the number of active sessions."""
    metrics_collector.set_gauge("active_sessions", count)