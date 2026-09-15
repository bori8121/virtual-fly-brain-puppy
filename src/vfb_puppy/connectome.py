from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import numpy as np

TARGET_NEURONS = 3001
TARGET_SYNAPSES = 548_000


@dataclass
class ConnectomeData:
    neuron_ids: np.ndarray
    neuropil_ids: np.ndarray
    pre_idx: np.ndarray
    post_idx: np.ndarray
    weights: np.ndarray


def _generate_reference_connectome(neurons: int = TARGET_NEURONS, synapses: int = TARGET_SYNAPSES) -> ConnectomeData:
    rng = np.random.default_rng(8121)
    neuron_ids = np.arange(neurons, dtype=np.int32)
    neuropil_ids = rng.integers(0, 16, size=neurons, dtype=np.int16)
    pre_idx = rng.integers(0, neurons, size=synapses, dtype=np.int32)
    post_idx = rng.integers(0, neurons, size=synapses, dtype=np.int32)
    weights = rng.uniform(0.05, 1.0, size=synapses).astype(np.float32)
    return ConnectomeData(neuron_ids, neuropil_ids, pre_idx, post_idx, weights)


def _load_csv_connectome(path: Path) -> ConnectomeData:
    neuron_set: set[int] = set()
    pre: list[int] = []
    post: list[int] = []
    weights: list[float] = []
    neuropil_by_neuron: dict[int, int] = {}

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"pre_neuron", "post_neuron", "weight", "pre_neuropil", "post_neuropil"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"{path} must include columns: {sorted(required)}")

        for row in reader:
            p = int(row["pre_neuron"])
            q = int(row["post_neuron"])
            w = float(row["weight"])
            pp = int(row["pre_neuropil"])
            qp = int(row["post_neuropil"])
            neuron_set.update((p, q))
            neuropil_by_neuron[p] = pp
            neuropil_by_neuron[q] = qp
            pre.append(p)
            post.append(q)
            weights.append(w)

    sorted_ids = np.array(sorted(neuron_set), dtype=np.int32)
    id_to_idx = {nid: i for i, nid in enumerate(sorted_ids.tolist())}

    pre_idx = np.array([id_to_idx[n] for n in pre], dtype=np.int32)
    post_idx = np.array([id_to_idx[n] for n in post], dtype=np.int32)
    neuropil_ids = np.array([neuropil_by_neuron.get(int(nid), 0) for nid in sorted_ids], dtype=np.int16)

    return ConnectomeData(
        neuron_ids=sorted_ids,
        neuropil_ids=neuropil_ids,
        pre_idx=pre_idx,
        post_idx=post_idx,
        weights=np.array(weights, dtype=np.float32),
    )


def load_connectome(data_dir: str | Path | None = None, complexity: str = "full") -> ConnectomeData:
    """Load FlyEM/malecns style connectome if present, otherwise fallback to a full-size reference graph."""
    if data_dir is None:
        data_dir = Path(__file__).resolve().parents[2] / "data"
    else:
        data_dir = Path(data_dir)

    candidate = data_dir / "malecns_connectome.csv"
    if candidate.exists():
        data = _load_csv_connectome(candidate)
    else:
        data = _generate_reference_connectome()

    if complexity == "core":
        keep = min(1000, data.neuron_ids.shape[0])
    elif complexity == "medium":
        keep = min(2000, data.neuron_ids.shape[0])
    else:
        keep = data.neuron_ids.shape[0]

    mask = (data.pre_idx < keep) & (data.post_idx < keep)
    return ConnectomeData(
        neuron_ids=data.neuron_ids[:keep],
        neuropil_ids=data.neuropil_ids[:keep],
        pre_idx=data.pre_idx[mask],
        post_idx=data.post_idx[mask],
        weights=data.weights[mask],
    )
