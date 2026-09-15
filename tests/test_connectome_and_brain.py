from pathlib import Path
import tempfile
import unittest

import numpy as np

from src.vfb_puppy.connectome import load_connectome, TARGET_NEURONS
from src.vfb_puppy.brain import FlyBrainSimulator


class ConnectomeTests(unittest.TestCase):
    def test_fallback_reference_connectome_is_full_size(self):
        data = load_connectome(data_dir=Path("/tmp/nonexistent-connectome"), complexity="full")
        self.assertGreaterEqual(data.neuron_ids.size, TARGET_NEURONS)
        self.assertGreaterEqual(data.pre_idx.size, 548_000)

    def test_csv_loading_works(self):
        with tempfile.TemporaryDirectory() as d:
            csv_path = Path(d) / "malecns_connectome.csv"
            csv_path.write_text(
                "pre_neuron,post_neuron,weight,pre_neuropil,post_neuropil\n"
                "1,2,0.7,3,4\n"
                "2,3,0.5,4,5\n",
                encoding="utf-8",
            )
            data = load_connectome(data_dir=d, complexity="full")
            self.assertEqual(data.neuron_ids.size, 3)
            self.assertEqual(data.pre_idx.size, 2)


class BrainStepTests(unittest.TestCase):
    def test_brain_step_updates_activity(self):
        data = load_connectome(data_dir=Path("/tmp/nonexistent-connectome"), complexity="core")
        sim = FlyBrainSimulator(data)
        sensory = np.full(data.neuron_ids.shape[0], 0.3, dtype=np.float32)
        state = sim.step(sensory)
        self.assertEqual(state.voltage.shape[0], data.neuron_ids.shape[0])
        self.assertEqual(state.calcium.shape[0], data.neuron_ids.shape[0])
        self.assertGreaterEqual(float(np.mean(state.calcium)), 0.0)


if __name__ == "__main__":
    unittest.main()
