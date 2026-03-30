import subprocess
import shutil
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class System_Telemetry:
    """
    Handles system-level telemetry and hardware hooks, designed to be terminal-agnostic
    but robustly supporting Android via Termux.
    """

    def __init__(self) -> None:
        """
        Initializes the telemetry system and checks for available hardware hooks.
        """
        # Dynamically check if the termux-vibrate binary exists on the system path.
        self._termux_vibrate_path: Optional[str] = shutil.which("termux-vibrate")

        if self._termux_vibrate_path:
            logger.debug(f"Found termux-vibrate at: {self._termux_vibrate_path}")
        else:
            logger.debug("termux-vibrate not found. Haptic feedback will be simulated/logged.")

    def haptic_feedback(self, duration_ms: int = 100) -> bool:
        """
        Triggers a haptic feedback (vibration) event.

        If running inside Termux, it invokes `termux-vibrate`.
        If not, it logs the event and returns gracefully, keeping the system terminal-agnostic.

        Args:
            duration_ms (int): The duration of the vibration in milliseconds. Defaults to 100.

        Returns:
            bool: True if the actual hardware vibration command was successfully dispatched,
                  False if it was simulated/logged or if the command failed.
        """
        if self._termux_vibrate_path:
            try:
                # Dispatch the command, non-blocking if possible, but wait to check return code.
                result = subprocess.run(
                    [self._termux_vibrate_path, "-d", str(duration_ms)],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    return True
                else:
                    logger.warning(f"termux-vibrate failed with exit code {result.returncode}: {result.stderr}")
                    return False
            except Exception as e:
                logger.error(f"Error executing termux-vibrate: {e}")
                return False
        else:
            # Terminal-agnostic fallback
            logger.info(f"[SIMULATED HAPTIC] Vibrating for {duration_ms}ms")
            return False
