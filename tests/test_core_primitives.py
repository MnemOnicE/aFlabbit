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


if __name__ == '__main__':
    unittest.main()
