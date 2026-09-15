from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class PuppyPose:
    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0
    head_tilt: float = 0.0


class PuppyEnvironment:
    def __init__(self):
        self.food = np.array([[2.0, 1.8], [-2.5, -1.2], [1.2, -2.7]], dtype=np.float32)
        self.obstacles = np.array([[1.5, 0.2], [-1.0, -2.1], [0.3, 2.4]], dtype=np.float32)
        self.light = np.array([3.0, 3.0], dtype=np.float32)

    def sensory_vector(self, pose: PuppyPose, neuron_count: int) -> np.ndarray:
        vec = np.zeros(neuron_count, dtype=np.float32)
        p = np.array([pose.x, pose.y], dtype=np.float32)
        food_dist = np.linalg.norm(self.food - p, axis=1)
        obs_dist = np.linalg.norm(self.obstacles - p, axis=1)
        light_dist = np.linalg.norm(self.light - p)

        vec[: neuron_count // 4] = 1.2 / (0.4 + np.min(food_dist))
        vec[neuron_count // 4 : neuron_count // 2] = -1.2 / (0.4 + np.min(obs_dist))
        vec[neuron_count // 2 : neuron_count * 3 // 4] = 1.0 / (0.4 + light_dist)
        vec[neuron_count * 3 // 4 :] = np.sin(pose.heading) * 0.3
        return vec

    def apply_motor(self, pose: PuppyPose, forward: float, turn: float, head_tilt: float, dt: float = 0.05) -> PuppyPose:
        pose.heading += turn * dt
        pose.x += np.cos(pose.heading) * forward * dt
        pose.y += np.sin(pose.heading) * forward * dt
        pose.head_tilt = np.clip(head_tilt, -0.8, 0.8)
        return pose
