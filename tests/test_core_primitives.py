"""
Test suite for BSL Core Primitives
"""

import unittest
from bsl.core_primitives import (
    Class0_Exception_Handling,
    Class1_Bootstrapping,
    Class2_Concurrency_IO,
    Class3_Execution,
    Class4_Garbage_Collection
)

class TestCorePrimitives(unittest.TestCase):
    """Test suite ensuring that all core primitives raise NotImplementedError."""

    def setUp(self):
        self.exception_handler = Class0_Exception_Handling()
        self.bootstrapper = Class1_Bootstrapping()
        self.concurrency = Class2_Concurrency_IO()
        self.execution = Class3_Execution()
        self.garbage_collector = Class4_Garbage_Collection()

    def test_method_not_implemented(self):
        """Test that scaffolding correctly raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.exception_handler.try_catch_finally(lambda: None, lambda: None, lambda: None)
Unit tests for the bsl.core_primitives module.
"""

import unittest
from typing import Any

from bsl.core_primitives import Primitive, Task


class DummyTask(Task):
    """A concrete implementation of Task to allow instantiation in tests."""
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return "Executed"

    def rollback(self) -> None:
        pass


class TestCorePrimitives(unittest.TestCase):
    """Test suite for Primitive and Task base classes."""

    def test_primitive_abc(self) -> None:
        """Verify that Primitive cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            # pylint: disable=abstract-class-instantiated
            Primitive()  # type: ignore

    def test_task_initialization(self) -> None:
        """Verify Task initializes with correct attributes."""
        task = DummyTask(name="Test Task", description="A test description")
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.description, "A test description")
        self.assertEqual(task.status, "PENDING")
        self.assertEqual(task.get_context(), {})

    def test_task_context_updates(self) -> None:
        """Verify context updating and retrieval works."""
        task = DummyTask(name="Context Task")
        task.update_context("key1", "value1")
        self.assertEqual(task.get_context(), {"key1": "value1"})
        task.update_context("key2", 42)
        self.assertEqual(task.get_context(), {"key1": "value1", "key2": 42})

    def test_task_unimplemented_methods(self) -> None:
        """Verify base Task raises NotImplementedError for execute and rollback."""
        task = Task(name="Unimplemented Task")
        with self.assertRaises(NotImplementedError):
            task.execute()
        with self.assertRaises(NotImplementedError):
            task.rollback()


if __name__ == '__main__':
    unittest.main()
