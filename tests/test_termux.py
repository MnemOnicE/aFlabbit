"""
Test suite for the bsl.termux module.
"""
import unittest
from unittest.mock import patch, MagicMock

from bsl.termux import TermuxAPI, _run_termux_cmd


class TestTermuxAPI(unittest.TestCase):
    """Test cases for the TermuxAPI class and _run_termux_cmd helper."""

    @patch('bsl.termux.shutil.which')
    def test_run_termux_cmd_missing(self, mock_which):
        """Test _run_termux_cmd when binary is missing."""
        mock_which.return_value = None
        result = _run_termux_cmd("termux-sensor")
        self.assertIsNone(result)

    @patch('bsl.termux.subprocess.run')
    @patch('bsl.termux.shutil.which')
    def test_run_termux_cmd_success(self, mock_which, mock_run):
        """Test _run_termux_cmd on successful execution."""
        mock_which.return_value = "/usr/bin/termux-sensor"
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = '{"sensor": "data"}\n'
        mock_run.return_value = mock_process

        result = _run_termux_cmd("termux-sensor", "-s", "accel")
        self.assertEqual(result, '{"sensor": "data"}')
        mock_run.assert_called_once_with(
            ["/usr/bin/termux-sensor", "-s", "accel"],
            capture_output=True,
            text=True,
            check=False
        )

    @patch('bsl.termux.subprocess.run')
    @patch('bsl.termux.shutil.which')
    def test_run_termux_cmd_failure(self, mock_which, mock_run):
        """Test _run_termux_cmd on failed execution."""
        mock_which.return_value = "/bin/termux-sensor"
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "error message\n"
        mock_run.return_value = mock_process

        result = _run_termux_cmd("termux-sensor")
        self.assertIsNone(result)

    def test_get_sensor_validation(self):
        """Test input validation for get_sensor."""
        with self.assertRaises(ValueError):
            TermuxAPI.get_sensor("")
        with self.assertRaises(ValueError):
            TermuxAPI.get_sensor("   ")
        with self.assertRaises(ValueError):
            TermuxAPI.get_sensor(123)  # type: ignore

    def test_show_dialog_validation(self):
        """Test input validation for show_dialog."""
        with self.assertRaises(TypeError):
            TermuxAPI.show_dialog(123, "content")  # type: ignore
        with self.assertRaises(TypeError):
            TermuxAPI.show_dialog("title", ["content"])  # type: ignore


if __name__ == '__main__':
    unittest.main()
