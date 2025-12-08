import threading
from numpy import ndarray
from windows_capture import Frame, InternalCaptureControl, WindowsCapture

class WindowCapture:
    """
    A wrapper for WindowsCapture to capture a single frame from a specified window.

    Attributes
    ----------
    _capture : WindowsCapture
        The internal WindowsCapture instance.
    _last_frame : ndarray
        The most recently captured frame buffer.
    _frame_ready_event : threading.Event
        Event indicating that a frame has arrived.
    """

    def __init__(self, window_name: str):
        """
        Initialize the WindowCapture for a specific window.

        Parameters
        ----------
        window_name : str
            The title of the window to capture.
        """
        self._capture = WindowsCapture(window_name=window_name)
        self._capture.frame_handler = self._on_frame_arrived
        self._capture.closed_handler = lambda: None
        self._last_frame = None
        self._frame_ready_event = threading.Event()

    def _on_frame_arrived(self, frame: Frame, capture_control: InternalCaptureControl):
        """
        Callback invoked when a new frame is received.
        Updates the last frame and stops capture.
        """
        self._last_frame = frame.frame_buffer
        self._frame_ready_event.set()
        capture_control.stop()

    def snapshot(self, timeout: float = 2) -> ndarray:
        """
        Capture a single frame from the window.

        Raises
        ------
        TimeoutError
            If no frame is received within the timeout period.
        """
        self._capture.start()

        if self._frame_ready_event.wait(timeout):
            self._frame_ready_event.clear()
            return self._last_frame
        else:
            raise TimeoutError("No frame received within timeout")
