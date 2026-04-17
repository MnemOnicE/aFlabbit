"""
Termux hardware hooks and sensor integrations.
Provides secure wrappers around Termux API binaries.
Termux integration module for Android-specific sensors and APIs.
Designed to run on Android via Termux with graceful fallbacks.
"""

import subprocess
import shutil
import logging
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TermuxAPI:
    """
    Provides wrappers for advanced Termux APIs such as sensors, dialogs,
    and battery status.
    """

    def __init__(self) -> None:
        """
        Initializes the TermuxAPI system and checks for the presence of
        the required Termux binaries.
        """
        self._termux_sensor: Optional[str] = shutil.which("termux-sensor")
        self._termux_dialog: Optional[str] = shutil.which("termux-dialog")
        self._termux_battery: Optional[str] = shutil.which(
            "termux-battery-status"
        )

    def get_battery_status(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the battery status of the device.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing battery status,
                                      or None if the command is unavailable
                                      or fails.
        """
        if not self._termux_battery:
            logger.debug("termux-battery-status not found. Returning None.")
            return None

        try:
            result = subprocess.run(
                [self._termux_battery],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            logger.warning(
                "termux-battery-status failed with exit code %s: %s",
                result.returncode,
                result.stderr
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error executing termux-battery-status: %s", e)
        return None

    def show_dialog(
        self,
        title: str,
        hint: str = "",
        multiple_lines: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Displays a text input dialog to the user.

        Args:
            title (str): The title of the dialog.
            hint (str): An optional hint for the input field.
            multiple_lines (bool): Allow multiple lines of input.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the user's input,
                                      or None if the command is unavailable
                                      or fails.
        """
        if not self._termux_dialog:
            logger.debug("termux-dialog not found. Returning None.")
            return None

        cmd = [self._termux_dialog, "text", "-t", title]
        if hint:
            cmd.extend(["-i", hint])
        if multiple_lines:
            cmd.append("-m")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            logger.warning(
                "termux-dialog failed with exit code %s: %s",
                result.returncode,
                result.stderr
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error executing termux-dialog: %s", e)
        return None

    def get_sensors(
        self,
        sensor_name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves sensor data from the device.

        Args:
            sensor_name (Optional[str]): A specific sensor name to query.
                                         If None, fetches all sensors.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the sensor data,
                                      or None if the command is unavailable
                                      or fails.
        """
        if not self._termux_sensor:
            logger.debug("termux-sensor not found. Returning None.")
            return None

        cmd = [self._termux_sensor]
        if sensor_name:
            cmd.extend(["-s", sensor_name, "-n", "1"])
        else:
            cmd.extend(["-a", "-n", "1"])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            logger.warning(
                "termux-sensor failed with exit code %s: %s",
                result.returncode,
                result.stderr
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error executing termux-sensor: %s", e)
        return None
