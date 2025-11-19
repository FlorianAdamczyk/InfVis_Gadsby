from __future__ import annotations

import csv
from pathlib import Path

from .analysis import KeyboardAnalysis


def export_counts_to_csv(path: Path | str, analysis: KeyboardAnalysis) -> None:
    """Persist per-key statistics for further analysis."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = analysis.total_characters or 1

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["key", "count", "normalized_count", "x", "y", "mapped_points"])
        for key in sorted(analysis.key_counts.keys()):
            count = analysis.key_counts[key]
            coords = analysis.layout.get(key, ())
            x, y = coords[0] if coords else ("", "")
            writer.writerow([
                key,
                count,
                round(count / total, 6),
                x,
                y,
                len(coords),
            ])
