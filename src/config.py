from dataclasses import dataclass
from enum import Enum


class CaptureMode(Enum):
    SINGLE = "Single Capture"
    CONTINUOUS = "Continuous Capture"


@dataclass
class Settings:
    """Core configuration parameters for strategy execution and UI."""
    capture_mode: CaptureMode = CaptureMode.SINGLE

    def toggle_capture_mode(self):
        self.capture_mode = (
            CaptureMode.CONTINUOUS
            if self.capture_mode == CaptureMode.SINGLE
            else CaptureMode.SINGLE
        )


settings = Settings()
