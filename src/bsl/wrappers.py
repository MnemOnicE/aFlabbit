"""
Wrappers module containing decorators and context managers
for execution interception and telemetry.
"""

from typing import Any, Callable, TypeVar, cast, Optional, Type
from types import TracebackType
import time
import logging
import functools

logger = logging.getLogger(__name__)

# A generic type variable to represent any callable
F = TypeVar('F', bound=Callable[..., Any])


def telemetry_wrapper(func: F) -> F:
    """
    A decorator that wraps a function or method to automatically inject
    telemetry hooks before and after execution.

    Args:
        func (F): The function to wrap.

    Returns:
        F: The wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Wrapper implementation for telemetry tracking.
        """
        start_time = time.perf_counter()
        logger.info("Executing %s...", func.__name__)
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            logger.info(
                "Execution of %s completed successfully in %.4f seconds.",
                func.__name__,
                duration
            )
            return result
        except Exception as error:
            duration = time.perf_counter() - start_time
            logger.error(
                "Execution of %s failed after %.4f seconds: %s",
                func.__name__,
                duration,
                str(error)
            )
            raise
    return cast(F, wrapper)


class ContextManagerWrapper:
    """
    A foundational context manager wrapper for ensuring safe execution.
    """

    def __init__(self, context_name: str) -> None:
        """
        Initializes the context manager wrapper.

        Args:
            context_name (str): The logical name of the context environment.
        """
        self.context_name: str = context_name

    def __enter__(self) -> 'ContextManagerWrapper':
        """
        Enters the context safely.
        """
        logger.info("Entering execution context: %s", self.context_name)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        """
        Exits the context and ensures resources are logged and managed.

        Args:
            exc_type: The type of the exception if raised.
            exc_value: The exception value if raised.
            traceback: The exception traceback if raised.
        """
        if exc_type is not None:
            logger.error(
                "Context '%s' exited with an exception: %s: %s",
                self.context_name,
                exc_type.__name__,
                exc_value
            )
        else:
            logger.info(
                "Successfully exited execution context: %s",
                self.context_name)
