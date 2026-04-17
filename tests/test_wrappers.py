"""
Test suite for the bsl.wrappers module.
"""
import unittest

from bsl.wrappers import telemetry_wrapper, ContextManagerWrapper


class TestWrappers(unittest.TestCase):
    """Test cases for wrappers."""

    def test_telemetry_wrapper_success(self):
        """Test successful execution with telemetry_wrapper."""
        @telemetry_wrapper
        def dummy_function(x, y):
            return x + y

        result = dummy_function(3, 4)
        self.assertEqual(result, 7)

    def test_telemetry_wrapper_failure(self):
        """Test failing execution with telemetry_wrapper."""
        @telemetry_wrapper
        def failing_function():
            raise ValueError("Test Error")

        with self.assertRaises(ValueError):
            failing_function()

    def test_context_manager_wrapper_success(self):
        """Test successful execution within ContextManagerWrapper."""
        with ContextManagerWrapper("TestContext") as ctx:
            self.assertEqual(ctx.context_name, "TestContext")

    def test_context_manager_wrapper_exception_handled(self):
        """Test exception propagation within ContextManagerWrapper."""
        try:
            with ContextManagerWrapper("ExceptionContext"):
                raise RuntimeError("Context Error")
        except RuntimeError:
            pass

    def test_telemetry_wrapper_dx(self):
        """Test that telemetry_wrapper preserves function metadata for DX."""
        @telemetry_wrapper
        def sample_function() -> str:
            """This is a sample docstring."""
            return "ok"

        self.assertEqual(sample_function.__name__, "sample_function")
        self.assertEqual(
            sample_function.__doc__, "This is a sample docstring.")


if __name__ == '__main__':
    unittest.main()
