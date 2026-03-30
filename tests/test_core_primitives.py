"""
Test suite for the bsl.core_primitives module.
"""
import unittest
from typing import Any

from bsl.core_primitives import Task, Primitive


class MockPrimitive(Primitive):
    """A mock primitive for testing Task execution."""

    def __init__(self, value: int, should_fail: bool = False):
        self.value = value
        self.should_fail = should_fail
        self.executed = False
        self.rolled_back = False

    def execute(self, *args: Any, **kwargs: Any) -> int:
        self.executed = True
        if self.should_fail:
            raise ValueError("Intentional failure")
        return self.value

    def rollback(self) -> None:
        self.rolled_back = True


class TestTask(unittest.TestCase):
    """Test cases for the Task class."""

    def test_task_execution(self):
        """Test successful task execution and state updates."""
        task = Task("TestTask")
        p1 = MockPrimitive(1)
        p2 = MockPrimitive(2)

        task.add_primitive(p1)
        task.add_primitive(p2)

        results = task.execute()

        self.assertEqual(results, [1, 2])
        self.assertEqual(task.status, "COMPLETED")
        self.assertTrue(p1.executed)
        self.assertTrue(p2.executed)
        self.assertFalse(p1.rolled_back)

    def test_task_rollback_on_failure(self):
        """Test task rollback mechanism upon primitive failure."""
        task = Task("FailingTask")
        p1 = MockPrimitive(1)
        p2 = MockPrimitive(2, should_fail=True)
        p3 = MockPrimitive(3)

        task.add_primitive(p1)
        task.add_primitive(p2)
        task.add_primitive(p3)

        with self.assertRaises(ValueError):
            task.execute()

        self.assertEqual(task.status, "ROLLED_BACK")

        # p1 executed successfully and should be rolled back
        self.assertTrue(p1.executed)
        self.assertTrue(p1.rolled_back)

        # p2 executed but failed, no rollback should be called on it since it's
        # not complete
        self.assertTrue(p2.executed)
        self.assertFalse(p2.rolled_back)

        # p3 should never execute
        self.assertFalse(p3.executed)
        self.assertFalse(p3.rolled_back)


if __name__ == '__main__':
    unittest.main()
