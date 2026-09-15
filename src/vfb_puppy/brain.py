from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .connectome import ConnectomeData


@dataclass
class BrainState:
    voltage: np.ndarray
    calcium: np.ndarray
    spikes: np.ndarray


class FlyBrainSimulator:
    def __init__(self, connectome: ConnectomeData, dt_ms: float = 1.0):
        self.connectome = connectome
        self.dt_ms = dt_ms
        n = connectome.neuron_ids.size
        self.state = BrainState(
            voltage=np.full(n, -60.0, dtype=np.float32),
            calcium=np.zeros(n, dtype=np.float32),
            spikes=np.zeros(n, dtype=np.float32),
        )
        self.rest = -62.0
        self.threshold = -50.0
        self.decay = np.float32(np.exp(-dt_ms / 15.0))
        self.calcium_decay = np.float32(np.exp(-dt_ms / 80.0))

    def step(self, sensory_drive: np.ndarray) -> BrainState:
        sensory = sensory_drive.astype(np.float32, copy=False)
        syn_current = np.zeros_like(self.state.voltage)
        np.add.at(
            syn_current,
            self.connectome.post_idx,
            self.state.spikes[self.connectome.pre_idx] * self.connectome.weights,
        )

        dv = ((self.rest - self.state.voltage) * 0.06) + syn_current * 0.15 + sensory
        self.state.voltage = self.state.voltage + dv

        spiked = self.state.voltage >= self.threshold
        self.state.spikes.fill(0.0)
        self.state.spikes[spiked] = 1.0
        self.state.voltage[spiked] = -58.0

        self.state.calcium = self.state.calcium * self.calcium_decay + self.state.spikes * 0.9
        self.state.voltage = self.rest + (self.state.voltage - self.rest) * self.decay
        return self.state

    def neural_heatmap(self, buckets: int = 20) -> np.ndarray:
        calcium = self.state.calcium
        if calcium.size == 0:
            return np.zeros((1, 1), dtype=np.float32)
        cols = int(np.ceil(calcium.size / buckets))
        padded = np.pad(calcium, (0, cols * buckets - calcium.size), constant_values=0)
        return padded.reshape(cols, buckets).T
