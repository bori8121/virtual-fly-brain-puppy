from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class MotorCommand:
    forward: float
    turn: float
    head_tilt: float


class BehaviorMapper:
    """Maps emergent motor neuron activity to puppy controls."""

    def __init__(self, neuron_count: int):
        third = neuron_count // 3
        self.forward_idx = slice(0, third)
        self.turn_idx = slice(third, third * 2)
        self.head_idx = slice(third * 2, neuron_count)

    def to_motor_command(self, spikes: np.ndarray, calcium: np.ndarray) -> MotorCommand:
        forward = float(np.mean(spikes[self.forward_idx]) * 2.0 - 0.2)
        left = float(np.mean(calcium[self.turn_idx]))
        right = float(np.mean(spikes[self.turn_idx]))
        turn = (left - right) * 1.5
        head_tilt = float(np.mean(calcium[self.head_idx]) - 0.3)
        return MotorCommand(forward=forward, turn=turn, head_tilt=head_tilt)
