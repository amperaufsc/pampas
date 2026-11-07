'''Control modules for the AMP motion system.'''

from dataclasses import dataclass

@dataclass
class DebugInfo:
    """Debug information for the control system."""

    setpoint: float
    sensor: float
    control: float
    control_overshoot: float
    error: float
