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
Unit tests for the bsl.termux module.
"""

import unittest
from unittest.mock import patch, MagicMock

from bsl.termux import TermuxAPI


class TestTermuxAPI(unittest.TestCase):
    """Test suite for the TermuxAPI Android wrappers and fallbacks."""

    @patch('shutil.which')
    def test_init_without_termux(
        self, mock_which: MagicMock
    ) -> None:
        """Verify initialization handles missing Termux binaries."""
        mock_which.return_value = None
        termux = TermuxAPI()
        # pylint: disable=protected-access
        self.assertIsNone(termux._termux_sensor)
        self.assertIsNone(termux._termux_dialog)
        self.assertIsNone(termux._termux_battery)
        # pylint: enable=protected-access

    @patch('shutil.which')
    def test_init_with_termux(
        self, mock_which: MagicMock
    ) -> None:
        """Verify initialization finds Termux binaries."""
        def side_effect(arg):
            return f'/data/data/com.termux/bin/{arg}'
        mock_which.side_effect = side_effect

        termux = TermuxAPI()
        # pylint: disable=protected-access
        self.assertEqual(
            termux._termux_sensor,
            '/data/data/com.termux/bin/termux-sensor'
        )
        self.assertEqual(
            termux._termux_dialog,
            '/data/data/com.termux/bin/termux-dialog'
        )
        self.assertEqual(
            termux._termux_battery,
            '/data/data/com.termux/bin/termux-battery-status'
        )
        # pylint: enable=protected-access

    @patch('shutil.which')
    def test_battery_status_fallback(self, mock_which: MagicMock) -> None:
        """Verify get_battery_status fallback to None when missing."""
        mock_which.return_value = None
        termux = TermuxAPI()

        with self.assertLogs('bsl.termux', level='DEBUG') as cm:
            result = termux.get_battery_status()

        self.assertIsNone(result)
        self.assertTrue(
            any("termux-battery-status not found" in log for log in cm.output)
        )

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_battery_status_success(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Verify get_battery_status parses output successfully."""
        def side_effect(arg):
            return f'/fake/bin/{arg}'
        mock_which.side_effect = side_effect

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"percentage": 85, "status": "DISCHARGING"}'
        )

        termux = TermuxAPI()
        result = termux.get_battery_status()

        self.assertIsNotNone(result)
        if result is not None:
            self.assertEqual(result.get("percentage"), 85)
            self.assertEqual(result.get("status"), "DISCHARGING")
        mock_run.assert_called_once_with(
            ['/fake/bin/termux-battery-status'],
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
    @patch('shutil.which')
    def test_dialog_fallback(self, mock_which: MagicMock) -> None:
        """Verify show_dialog fallback to None when missing."""
        mock_which.return_value = None
        termux = TermuxAPI()

        with self.assertLogs('bsl.termux', level='DEBUG') as cm:
            result = termux.show_dialog("Test")

        self.assertIsNone(result)
        self.assertTrue(
            any("termux-dialog not found" in log for log in cm.output)
        )

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_dialog_success(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Verify show_dialog formats command and parses output."""
        def side_effect(arg):
            return f'/fake/bin/{arg}'
        mock_which.side_effect = side_effect

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"code": -1, "text": "user input"}'
        )

        termux = TermuxAPI()
        result = termux.show_dialog(
            title="Title",
            hint="Hint",
            multiple_lines=True
        )

        self.assertIsNotNone(result)
        if result is not None:
            self.assertEqual(result.get("text"), "user input")

        expected_cmd = [
            '/fake/bin/termux-dialog', 'text', '-t', 'Title',
            '-i', 'Hint', '-m'
        ]
        mock_run.assert_called_once_with(
            expected_cmd,
            capture_output=True,
            text=True,
            check=False
        )

    @patch('shutil.which')
    def test_sensors_fallback(self, mock_which: MagicMock) -> None:
        """Verify get_sensors fallback to None when missing."""
        mock_which.return_value = None
        termux = TermuxAPI()

        with self.assertLogs('bsl.termux', level='DEBUG') as cm:
            result = termux.get_sensors()

        self.assertIsNone(result)
        self.assertTrue(
            any("termux-sensor not found" in log for log in cm.output)
        )

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_sensors_success(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Verify get_sensors formats command and parses output."""
        def side_effect(arg):
            return f'/fake/bin/{arg}'
        mock_which.side_effect = side_effect

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"ACCELEROMETER": {"values": [0.1, 0.2, 9.8]}}'
        )

        termux = TermuxAPI()
        result = termux.get_sensors(sensor_name="ACCELEROMETER")

        self.assertIsNotNone(result)
        if result is not None:
            self.assertIn("ACCELEROMETER", result)

        mock_run.assert_called_once_with(
            ['/fake/bin/termux-sensor', '-s', 'ACCELEROMETER', '-n', '1'],
            capture_output=True,
            text=True,
            check=False
        )

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_command_failure_logs_warning(
        self, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Verify that a failing command returns None and logs warning."""
        def side_effect(arg):
            return f'/fake/bin/{arg}'
        mock_which.side_effect = side_effect

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Permission denied"
        )

        termux = TermuxAPI()
        with self.assertLogs('bsl.termux', level='WARNING') as cm:
            result = termux.get_battery_status()

        self.assertIsNone(result)

        found_log = any(
            "failed with exit code 1: Permission denied" in log
            for log in cm.output
        )
        self.assertTrue(found_log)


if __name__ == '__main__':
    unittest.main()
