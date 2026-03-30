"""
Test suite for BSL Wrappers
"""

import unittest
from bsl.wrappers import Routine_Wrappers

class TestWrappers(unittest.TestCase):
    """Test suite ensuring that all wrappers raise NotImplementedError."""

    def setUp(self):
        self.wrappers = Routine_Wrappers()

    def test_method_not_implemented(self):
        """Test that scaffolding correctly raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.wrappers.reoccurring_routine("* * * * *", lambda: None)


if __name__ == '__main__':
    unittest.main()
