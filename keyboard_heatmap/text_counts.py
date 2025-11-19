"""Text ingestion and counting utilities for the keyboard heatmap."""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

LayoutType = Mapping[str, Sequence[Tuple[int, int]]]


def load_text(path: str | Path, encoding: str = "utf-8") -> str:
    path = Path(path)
    return path.read_text(encoding=encoding)


def normalize_char(ch: str) -> str:
    if not ch:
        return ch
    if ch.isalpha():
        return ch.upper()
    return ch


@dataclass
class AnalysisResult:
    char_counts: Counter
    key_counts: Counter
    total_characters: int
    unmapped_counts: Counter

    def most_common(self, n: int = 10) -> List[Tuple[str, int]]:
        return self.char_counts.most_common(n)

    @property
    def max_key_count(self) -> int:
        return max(self.key_counts.values(), default=0)

    def as_csv_rows(self) -> List[Tuple[str, int, float]]:
        rows: List[Tuple[str, int, float]] = []
        if self.total_characters == 0:
            return rows
        for char, count in sorted(self.char_counts.items()):
            rel = count / self.total_characters
            rows.append((char, count, rel))
        return rows


DEFAULT_EXCLUDES: Sequence[str] = []


def analyze_text(
    text: str,
    layout: LayoutType,
    *,
    excludes: Optional[Iterable[str]] = None,
) -> AnalysisResult:
    excludes_set = set(excludes or DEFAULT_EXCLUDES)
    char_counts: Counter = Counter()
    key_counts: Counter = Counter()
    unmapped_counts: Counter = Counter()

    for raw_char in text:
        normalized = normalize_char(raw_char)
        if normalized in excludes_set:
            continue
        if normalized in layout:
            char_counts[normalized] += 1
            key_counts[normalized] += 1
        elif normalized.strip():
            unmapped_counts[normalized] += 1

    return AnalysisResult(
        char_counts=char_counts,
        key_counts=key_counts,
        total_characters=sum(char_counts.values()),
        unmapped_counts=unmapped_counts,
    )


def export_counts_to_csv(path: str | Path, analysis: AnalysisResult) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fp:
        fp.write("character,absolute_count,relative_frequency\n")
        for char, count, rel in analysis.as_csv_rows():
            fp.write(f"{char},{count},{rel:.6f}\n")

