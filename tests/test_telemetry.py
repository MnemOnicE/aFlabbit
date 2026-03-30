import unittest
import logging
from unittest.mock import patch, MagicMock

from bsl.telemetry import System_Telemetry


class TestTelemetry(unittest.TestCase):

    @patch('shutil.which')
    def test_init_without_termux(self, mock_which: MagicMock) -> None:
        """Verify initialization handles missing termux-vibrate gracefully."""
        mock_which.return_value = None
        telemetry = System_Telemetry()
        self.assertIsNone(telemetry._termux_vibrate_path)

    @patch('shutil.which')
    def test_init_with_termux(self, mock_which: MagicMock) -> None:
        """Verify initialization finds termux-vibrate."""
        mock_which.return_value = '/data/data/com.termux/files/usr/bin/termux-vibrate'
        telemetry = System_Telemetry()
        self.assertEqual(telemetry._termux_vibrate_path, '/data/data/com.termux/files/usr/bin/termux-vibrate')

    @patch('shutil.which')
    def test_haptic_fallback(self, mock_which: MagicMock) -> None:
        """Verify haptic feedback returns False (simulated) when termux-vibrate is missing."""
        mock_which.return_value = None
        telemetry = System_Telemetry()

        # We can also capture logs to ensure the fallback branch is hit
        with self.assertLogs('bsl.telemetry', level='INFO') as cm:
            result = telemetry.haptic_feedback(duration_ms=150)

        self.assertFalse(result)
        self.assertTrue(any("SIMULATED HAPTIC" in log for log in cm.output))

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_haptic_success(self, mock_subprocess_run: MagicMock, mock_which: MagicMock) -> None:
        """Verify haptic feedback returns True when termux-vibrate succeeds."""
        mock_which.return_value = '/fake/bin/termux-vibrate'
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        telemetry = System_Telemetry()
        result = telemetry.haptic_feedback(duration_ms=200)

        self.assertTrue(result)
        mock_subprocess_run.assert_called_once_with(
            ['/fake/bin/termux-vibrate', '-d', '200'],
            capture_output=True,
            text=True,
            check=False
        )

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_haptic_failure(self, mock_subprocess_run: MagicMock, mock_which: MagicMock) -> None:
        """Verify haptic feedback returns False when termux-vibrate subprocess fails (non-zero exit)."""
        mock_which.return_value = '/fake/bin/termux-vibrate'
        mock_subprocess_run.return_value = MagicMock(returncode=1, stderr="Failed to vibrate")

        telemetry = System_Telemetry()

        with self.assertLogs('bsl.telemetry', level='WARNING') as cm:
            result = telemetry.haptic_feedback()

        self.assertFalse(result)
        self.assertTrue(any("termux-vibrate failed" in log for log in cm.output))

if __name__ == '__main__':
    unittest.main()
