import threading
import numpy as np
from windows_capture import Frame, InternalCaptureControl, WindowsCapture

import config


WAIT_FRAME_TIMEOUT = 2


class WindowCapture:
    """A wrapper for WindowsCapture to capture a single frame from a specified window."""

    def __init__(self, window_name: str) -> None:
        """Initialize the WindowCapture for a specific window."""
        self._capture = WindowsCapture(cursor_capture=False, window_name=window_name)
        self._capture.frame_handler = self._on_frame_arrived
        self._capture.closed_handler = lambda: None
        self._running = False
        self._frame_ready_event = threading.Event()
        self.latest_frame: np.ndarray | None = None

    def _on_frame_arrived(self, frame: Frame, capture_control: InternalCaptureControl) -> None:
        """
        Callback invoked when a new frame is received.
        Updates the latest frame and stops capture if not running.
        """
        self.latest_frame = frame.frame_buffer

        if config.settings.capture_mode == config.CaptureMode.SINGLE:
            self._frame_ready_event.set()
            capture_control.stop()
        elif not self._running:
            capture_control.stop()

    def start(self) -> None:
        """Start capturing frames."""
        if config.settings.capture_mode == config.CaptureMode.CONTINUOUS and not self._running:
            self._running = True
            self._capture.start_free_threaded()

    def stop(self) -> None:
        """Stop capturing frames."""
        self._running = False

    def get_frame(self) -> (np.ndarray | None):
        """Retrieve the most recently captured frame."""
        if config.settings.capture_mode == config.CaptureMode.SINGLE:
            return self._capture_single_frame()
        return self.latest_frame

    def _capture_single_frame(self) -> (np.ndarray | None):
        self._capture.start_free_threaded()
        if self._frame_ready_event.wait(WAIT_FRAME_TIMEOUT):
            return self.latest_frame
        raise TimeoutError("No frame received within timeout")
