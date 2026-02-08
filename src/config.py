from dataclasses import dataclass
from enum import Enum


class CaptureMode(Enum):
    SINGLE = "Single Capture"
    CONTINUOUS = "Continuous Capture"


class TriState(Enum):
    """Tri-state toggle: enabled / disabled / unset."""
    ENABLED = "enabled"
    DISABLED = "disabled"
    UNSET = "unset"


@dataclass
class Settings:
    """Core configuration parameters for strategy execution and UI."""
    # Private attributes
    _capture_mode: CaptureMode = CaptureMode.SINGLE
    _advance: TriState = TriState.UNSET
    _night_battle: TriState = TriState.UNSET

    # Capture mode property
    @property
    def capture_mode(self) -> CaptureMode:
        """Get current capture mode."""
        return self._capture_mode

    @capture_mode.setter
    def capture_mode(self, value: CaptureMode):
        """Set capture mode, must be a CaptureMode enum."""
        if not isinstance(value, CaptureMode):
            raise ValueError("capture_mode must be a CaptureMode")
        self._capture_mode = value

    def toggle_capture_mode(self):
        """Toggle between SINGLE and CONTINUOUS capture modes."""
        self.capture_mode = (
            CaptureMode.CONTINUOUS
            if self.capture_mode == CaptureMode.SINGLE
            else CaptureMode.SINGLE
        )

    # Advance property
    @property
    def advance(self) -> TriState:
        """Get current advance state."""
        return self._advance

    @advance.setter
    def advance(self, value: TriState):
        """Set advance state, must be a TriState enum."""
        if not isinstance(value, TriState):
            raise ValueError("advance must be a TriState")
        self._advance = value

    # Night battle property
    @property
    def night_battle(self) -> TriState:
        """Get current night battle state."""
        return self._night_battle

    @night_battle.setter
    def night_battle(self, value: TriState):
        """Set night battle state, must be a TriState enum."""
        if not isinstance(value, TriState):
            raise ValueError("night_battle must be a TriState")
        self._night_battle = value


# Global settings instance
settings = Settings()
