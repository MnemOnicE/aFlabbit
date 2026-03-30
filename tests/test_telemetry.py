"""
Unit tests for the bsl.telemetry module.
"""

import unittest
from unittest.mock import patch, MagicMock

from bsl.telemetry import SystemTelemetry


class TestTelemetry(unittest.TestCase):
    """Test suite for the SystemTelemetry hardware hooks and fallbacks."""

    @patch('shutil.which')
    def test_init_without_termux(
        self, mock_which: MagicMock
    ) -> None:
        """Verify initialization handles missing termux-vibrate."""
        mock_which.return_value = None
        telemetry = SystemTelemetry()
        self.assertIsNone(telemetry.get_vibrate_path())

    @patch('shutil.which')
    def test_init_with_termux(
        self, mock_which: MagicMock
    ) -> None:
        """Verify initialization finds termux-vibrate."""
        mock_which.return_value = '/data/data/com.termux/bin/vibrate'
        telemetry = SystemTelemetry()
        self.assertEqual(
            telemetry.get_vibrate_path(),
            '/data/data/com.termux/bin/vibrate'
        )

    @patch('shutil.which')
    def test_haptic_fallback(
        self, mock_which: MagicMock
    ) -> None:
        """Verify haptic fallback to False when missing."""
        mock_which.return_value = None
        telemetry = SystemTelemetry()

        # We can also capture logs to ensure the fallback branch is hit
        with self.assertLogs('bsl.telemetry', level='INFO') as cm:
            result = telemetry.haptic_feedback(duration_ms=150)

        self.assertFalse(result)
        self.assertTrue(
            any("SIMULATED HAPTIC" in log for log in cm.output)
        )

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_haptic_success(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Verify haptic feedback returns True when termux-vibrate works."""
        mock_which.return_value = '/fake/bin/termux-vibrate'
        mock_run.return_value = MagicMock(returncode=0)

        telemetry = SystemTelemetry()
        result = telemetry.haptic_feedback(duration_ms=200)

        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ['/fake/bin/termux-vibrate', '-d', '200'],
            capture_output=True,
            text=True,
            check=False
        )

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_haptic_failure(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Verify haptic feedback returns False when vibrate fails."""
        mock_which.return_value = '/fake/bin/termux-vibrate'
        mock_run.return_value = MagicMock(
            returncode=1, stderr="Failed to vibrate"
        )

        telemetry = SystemTelemetry()

        with self.assertLogs('bsl.telemetry', level='WARNING') as cm:
            result = telemetry.haptic_feedback()

        self.assertFalse(result)
        self.assertTrue(
            any("termux-vibrate failed" in log for log in cm.output))


if __name__ == '__main__':
    unittest.main()
