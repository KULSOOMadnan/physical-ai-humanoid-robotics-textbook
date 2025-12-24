import time
import logging
from functools import wraps
from typing import Callable, Any
from asyncio import get_event_loop, iscoroutinefunction


logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """
    Utility class for monitoring and logging performance metrics.
    """

    def __init__(self):
        self.metrics = {}

    def measure_time(self, name: str = None):
        """
        Decorator to measure execution time of a function.

        Args:
            name: Optional name for the metric (defaults to function name)
        """
        def decorator(func: Callable) -> Callable:
            if iscoroutinefunction(func):
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    start_time = time.time()
                    try:
                        result = await func(*args, **kwargs)
                        return result
                    finally:
                        end_time = time.time()
                        execution_time = end_time - start_time
                        metric_name = name or f"{func.__module__}.{func.__name__}"
                        self._log_metric(metric_name, execution_time)
            else:
                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        return result
                    finally:
                        end_time = time.time()
                        execution_time = end_time - start_time
                        metric_name = name or f"{func.__module__}.{func.__name__}"
                        self._log_metric(metric_name, execution_time)

            return async_wrapper if iscoroutinefunction(func) else sync_wrapper

        return decorator

    def _log_metric(self, name: str, execution_time: float):
        """
        Log the performance metric.

        Args:
            name: Name of the metric
            execution_time: Execution time in seconds
        """
        # Store in metrics dict for potential aggregation
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(execution_time)

        # Log if it exceeds threshold (e.g., 1 second)
        if execution_time > 1.0:
            logger.warning(f"Performance alert: {name} took {execution_time:.2f}s")
        else:
            logger.info(f"Performance: {name} took {execution_time:.2f}s")

    def get_average_time(self, name: str) -> float:
        """
        Get the average execution time for a specific metric.

        Args:
            name: Name of the metric

        Returns:
            Average execution time in seconds
        """
        if name in self.metrics and self.metrics[name]:
            return sum(self.metrics[name]) / len(self.metrics[name])
        return 0.0

    def reset_metrics(self):
        """Reset all collected metrics."""
        self.metrics.clear()


# Global performance monitor instance
perf_monitor = PerformanceMonitor()


def add_performance_monitoring(app):
    """
    Add performance monitoring to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    @app.middleware("http")
    async def performance_monitoring_middleware(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()

        execution_time = end_time - start_time
        perf_monitor._log_metric(f"request_{request.method}_{request.url.path}", execution_time)

        # Add performance header to response (only in debug mode)
        from app.config.settings import get_settings
        if get_settings().DEBUG:
            response.headers["X-Response-Time"] = f"{execution_time:.3f}s"

        return response