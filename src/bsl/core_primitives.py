"""
Core primitives module defining the foundational classes and workflows
for the Human Execution Framework.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


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
        raise NotImplementedError("Subclasses must implement the execute method.")

    @abstractmethod
    def rollback(self) -> None:
        """
        Rolls back or undoes the execution if possible.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement the rollback method.")


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
        Executes the task logic.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement the execute method.")

    def rollback(self) -> None:
        """
        Rolls back the task execution.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement the rollback method.")
