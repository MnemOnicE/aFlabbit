"""
Termux hardware hooks and sensor integrations.
Provides secure wrappers around Termux API binaries.
"""

import subprocess
import shutil
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def _run_termux_cmd(cmd: str, *args: str) -> Optional[str]:
    """
    Safely execute a termux command if it exists.

    Args:
        cmd (str): The termux binary name (e.g., termux-sensor).
        args (str): Additional arguments for the command.

    Returns:
        Optional[str]: The standard output of the command if successful,
                       or None if the command is missing or fails.
    """
    cmd_path = shutil.which(cmd)
    if not cmd_path:
        logger.debug("%s not found. Simulating or ignoring.", cmd)
        return None

    try:
        # We explicitly avoid shell=True to prevent command injection.
        # Arguments are passed securely as a list.
        result = subprocess.run(
            [cmd_path, *args],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
        logger.warning(
            "%s failed with exit code %s: %s",
            cmd,
            result.returncode,
            result.stderr.strip()
        )
        return None
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error executing %s: %s", cmd, str(e))
        return None


class TermuxAPI:
    """
    Interface for Termux-specific API interactions.
    Fails gracefully on non-Termux systems.
    """

    @staticmethod
    def get_sensor(sensor_name: str) -> Optional[str]:
        """
        Retrieves data for a specific sensor.

        Args:
            sensor_name (str): The name of the sensor (e.g., 'accel').

        Returns:
            Optional[str]: Sensor data as a JSON string, or None.
        """
        if not isinstance(sensor_name, str) or not sensor_name.strip():
            raise ValueError("sensor_name must be a non-empty string.")
        return _run_termux_cmd("termux-sensor", "-s", sensor_name, "-n", "1")

    @staticmethod
    def show_dialog(title: str, content: str) -> Optional[str]:
        """
        Shows a dialog to the user and captures the result.

        Args:
            title (str): The title of the dialog.
            content (str): The content/message of the dialog.

        Returns:
            Optional[str]: Dialog interaction result as a JSON string, or None.
        """
        if not isinstance(title, str) or not isinstance(content, str):
            raise TypeError("title and content must be strings.")

        return _run_termux_cmd(
            "termux-dialog", "confirm", "-t", title, "-i", content
        )

    @staticmethod
    def get_battery_status() -> Optional[str]:
        """
        Retrieves the device battery status.

        Returns:
            Optional[str]: Battery status data as a JSON string, or None.
        """
        return _run_termux_cmd("termux-battery-status")
