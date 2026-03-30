"""
Telemetry module handling system-level hardware hooks.
Designed to run well on Android via Termux with fallbacks.
"""

import subprocess
import shutil
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class SystemTelemetry:
    """
    Handles system-level telemetry and hardware hooks, designed
    to be terminal-agnostic
    supporting Termux.
    """

    def __init__(self) -> None:
        """
        Initializes the telemetry system and checks for available
        hardware hooks.
        """
        # Dynamically check if the termux-vibrate binary exists on the system
        # path.
        self._termux_vibrate_path: Optional[str] = shutil.which(
            "termux-vibrate")

        if self._termux_vibrate_path:
            logger.debug(
                "Found termux-vibrate at: %s",
                self._termux_vibrate_path)
        else:
            logger.debug(
                "termux-vibrate not found. Haptic feedback will be simulated.")

    def get_vibrate_path(self) -> Optional[str]:
        """
        Returns the path to termux-vibrate, or None if not found.
        """
        return self._termux_vibrate_path

    def haptic_feedback(self, duration_ms: int = 100) -> bool:
        """
        Triggers a haptic feedback (vibration) event.

        If running inside Termux, it invokes `termux-vibrate`.
        If not, it logs the event and returns gracefully.

        Args:
            duration_ms (int): The duration of the vibration in milliseconds.

        Returns:
            bool: True if vibration command was successfully dispatched,
                  False if simulated or if the command failed.
        """
        if self._termux_vibrate_path:
            try:
                # Dispatch the command, non-blocking if possible, wait to check
                # return code.
                result = subprocess.run(
                    [self._termux_vibrate_path, "-d", str(duration_ms)],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return True
                logger.warning(
                    "termux-vibrate failed with exit code %s: %s",
                    result.returncode,
                    result.stderr
                )
                return False
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("Error executing termux-vibrate: %s", e)
                return False

        # Terminal-agnostic fallback
        logger.info("[SIMULATED HAPTIC] Vibrating for %sms", duration_ms)
        return False
