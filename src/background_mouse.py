import ctypes
import time
import win32con
import win32gui


CLICK_DELAY = 0.05
DOUBLE_CLICK_DELAY = 0.1


class BackgroundMouse:
    """Perform background mouse operations on a specific window."""

    def __init__(self, title: str = None, class_name: str = None) -> None:
        """Initialize and cache the window handle (hwnd) at creation."""
        self.title = title
        self.class_name = class_name

        # Find and cache the window handle
        self._hwnd = self._find_window(title, class_name)

        # Get the DPI scale factor for the window
        dpi = ctypes.windll.user32.GetDpiForWindow(self._hwnd)
        self._scale = dpi / 96  # 96 DPI = 100%

    def click(self, position: tuple) -> None:
        """Perform a background click at the given client coordinates (x, y)."""
        self._refresh_hwnd()
        x, y = int(position[0] / self._scale), int(position[1] / self._scale)
        lParam = (y << 16) | x
        win32gui.PostMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(CLICK_DELAY)
        win32gui.PostMessage(self._hwnd, win32con.WM_LBUTTONUP, 0, lParam)

    def double_click(self, position: tuple) -> None:
        """Perform a double-click at the given client coordinates (x, y)."""
        self.click(position)
        time.sleep(DOUBLE_CLICK_DELAY)
        self.click(position)

    def move_to(self, position: tuple) -> None:
        """Move the mouse to the specified coordinates."""
        self._refresh_hwnd()
        x, y = int(position[0] / self._scale), int(position[1] / self._scale)
        lParam = (y << 16) | x
        win32gui.PostMessage(self._hwnd, win32con.WM_MOUSEMOVE, 0, lParam)

    def smooth_move_to(self, start_position: tuple, end_position: tuple,
            steps: int = 30, delay: float = 0.01) -> None:
        """Smoothly move the mouse from start_position to end_position in small steps."""
        start_x, start_y = start_position
        end_x, end_y = end_position

        # Calculate the step size for each movement along the two positions
        step_x = (end_x - start_x) / steps
        step_y = (end_y - start_y) / steps

        # Move the mouse in steps from start to end position
        for i in range(1, steps + 1):
            new_x = int(start_x + step_x * i)
            new_y = int(start_y + step_y * i)
            self.move_to((new_x, new_y))
            time.sleep(delay)

    def _refresh_hwnd(self) -> None:
        """Refresh the cached hwnd if the current hwnd is invalid."""
        if not self._hwnd or not win32gui.IsWindow(self._hwnd):
            self._hwnd = self._find_window(self.title, self.class_name)

    @staticmethod
    def _find_window(title: str = None, class_name: str = None) -> int:
        """Find hwnd based on the window title or class name."""
        hwnd = win32gui.FindWindow(class_name, title)
        if hwnd == 0:
            raise ValueError("Window not found")
        return hwnd
