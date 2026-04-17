"""
Core primitives module defining the foundational classes and workflows
for the Human Execution Framework.
"""

from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Primitive(ABC):
    """
    Base class for all behavioral primitives in the Human Execution Framework.
    """

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Executes the primary logic of this primitive.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError(
            "Subclasses must implement the execute method.")

    @abstractmethod
    def rollback(self) -> None:
        """
        Rolls back or undoes the execution if possible.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError(
            "Subclasses must implement the rollback method.")


class Task(Primitive):
    """
    A Task represents a higher-level workflow composed of primitives.
    """

    def __init__(self, name: str, description: Optional[str] = None) -> None:
        """
        Initializes a Task.

        Args:
            name (str): The name of the task.
            description (Optional[str]): An optional description of the task.
        """
        self.name: str = name
        self.description: Optional[str] = description
        self.status: str = "PENDING"
        self._context: Dict[str, Any] = {}
        self._primitives: List['Primitive'] = []
        self._completed_primitives: List['Primitive'] = []

    def add_primitive(self, primitive: 'Primitive') -> None:
        """
        Adds a primitive to the task workflow.

        Args:
            primitive (Primitive): The primitive to add.
        """
        self._primitives.append(primitive)

    def get_context(self) -> Dict[str, Any]:
        """
        Returns the current execution context.

        Returns:
            Dict[str, Any]: The task context.
        """
        return self._context

    def update_context(self, key: str, value: Any) -> None:
        """
        Updates the execution context with a key-value pair.

        Args:
            key (str): The context key.
            value (Any): The context value.
        """
        self._context[key] = value

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Executes the task logic by sequentially running all
        primitives.

        Returns:
            List[Any]: A list of results from each primitive.

        Raises:
            Exception: If any primitive fails during execution, triggering a
            rollback.
        """
        self.status = "RUNNING"
        self._completed_primitives.clear()
        results = []
        try:
            for primitive in self._primitives:
                result = primitive.execute(*args, **kwargs)
                results.append(result)
                self._completed_primitives.append(primitive)
            self.status = "COMPLETED"
            return results
        except Exception as error:
            self.status = "FAILED"
            self.rollback()
            raise error

    def rollback(self) -> None:
        """
        Rolls back the task execution by invoking rollback on completed
        primitives in reverse order.
        """
        self.status = "ROLLING_BACK"
        for primitive in reversed(self._completed_primitives):
            try:
                primitive.rollback()
            except Exception:  # pylint: disable=broad-exception-caught
                logger.exception(
                    "Error rolling back primitive %s",
                    primitive.__class__.__name__
                )
        self._completed_primitives.clear()
        self.status = "ROLLED_BACK"
