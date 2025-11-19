from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Counter as CounterType, Iterable, Mapping, Sequence, Tuple

from collections import Counter

Coordinate = Tuple[int, int]
LayoutMapping = Mapping[str, Sequence[Coordinate]]

DEFAULT_EXCLUDES = {" "}


@dataclass(slots=True)
class KeyboardAnalysis:
    """Aggregated keyboard statistics for heatmap rendering."""

    layout_name: str
    layout: LayoutMapping
    total_characters: int
    key_counts: CounterType[str]
    point_counts: CounterType[Coordinate]
    unmapped_counts: CounterType[str]

    @property
    def max_point_density(self) -> int:
        return max(self.point_counts.values(), default=0)


def load_text(path: str | Path) -> str:
    """Read a text file into memory using UTF-8."""

    file_path = Path(path)
    return file_path.read_text(encoding="utf-8")


def _normalize_character(char: str) -> str:
    if char.isalpha():
        return char.upper()
    return char


def analyze_text(
    text: str,
    layout: LayoutMapping,
    *,
    excludes: Iterable[str] | None = None,
    layout_name: str = "QWERTY",
) -> KeyboardAnalysis:
    """Map characters of *text* to keyboard coordinates and aggregate counts."""

    exclude_set = set(DEFAULT_EXCLUDES)
    if excludes:
        exclude_set.update(excludes)

    key_counts: CounterType[str] = Counter()
    point_counts: CounterType[Coordinate] = Counter()
    unmapped: CounterType[str] = Counter()
    total = 0

    for raw_char in text:
        char = _normalize_character(raw_char)
        if char in exclude_set:
            continue

        coords = layout.get(char)
        if not coords:
            unmapped[char] += 1
            continue

        total += 1
        key_counts[char] += 1
        for x, y in coords:
            point_counts[(int(x), int(y))] += 1

    return KeyboardAnalysis(
        layout_name=layout_name,
        layout=layout,
        total_characters=total,
        key_counts=key_counts,
        point_counts=point_counts,
        unmapped_counts=unmapped,
    )
