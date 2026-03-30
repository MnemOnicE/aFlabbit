"""
Test suite for BSL Telemetry
"""

import unittest
from bsl.telemetry import System_Telemetry

class TestTelemetry(unittest.TestCase):
    def setUp(self):
        self.telemetry = System_Telemetry()

    def test_method_not_implemented(self):
        """Test that scaffolding correctly raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.telemetry.haptic_feedback("100,50,100")


if __name__ == '__main__':
    unittest.main()
