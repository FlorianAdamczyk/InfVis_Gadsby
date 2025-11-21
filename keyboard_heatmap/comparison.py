from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple

from .analysis import KeyboardAnalysis

Coordinate = Tuple[int, int]


def _relative_frequencies(analysis: KeyboardAnalysis) -> Dict[str, float]:
    total = analysis.total_characters or 1
    return {key: analysis.key_counts.get(key, 0) / total for key in analysis.layout.keys()}


def compute_relative_difference_points(
    base: KeyboardAnalysis,
    other: KeyboardAnalysis,
) -> Dict[Coordinate, float]:
    """Return per-coordinate relative frequency differences (base - other)."""

    if base.layout is not other.layout:
        # We rely on identical layout dicts so coordinates match exactly.
        raise ValueError("Both analyses must reference the same layout instance for comparison")

    base_freq = _relative_frequencies(base)
    other_freq = _relative_frequencies(other)
    point_values: Dict[Coordinate, float] = {}

    for key, coords in base.layout.items():
        diff = base_freq.get(key, 0.0) - other_freq.get(key, 0.0)
        for coord in coords:
            point_values[(int(coord[0]), int(coord[1]))] = diff

    return point_values
