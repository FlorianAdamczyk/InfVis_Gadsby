from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, Tuple

Coordinate = Tuple[int, int]
LayoutMapping = Dict[str, Tuple[Coordinate, ...]]

_LAYOUT_SOURCE = Path(__file__).resolve().parents[1] / "patrick-wied.at" / "keyboard-layouts.js"
_PAIR_PATTERN = re.compile(r'"(?P<key>[^"]+)"\s*:\s*\[(?P<values>[^\]]*)\]', re.MULTILINE)


def _extract_layout_block(name: str) -> str:
    text = _LAYOUT_SOURCE.read_text(encoding="utf-8")
    marker = f"{name}:"
    start = text.find(marker)
    if start == -1:
        raise ValueError(f"Layout {name!r} not found in { _LAYOUT_SOURCE }")
    brace_start = text.find("{", start)
    if brace_start == -1:
        raise ValueError(f"Layout {name!r} is malformed")

    depth = 0
    for idx in range(brace_start, len(text)):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[brace_start + 1 : idx]
    raise ValueError(f"Unbalanced braces while parsing layout {name!r}")


def _parse_layout(name: str) -> LayoutMapping:
    block = _extract_layout_block(name)
    layout: LayoutMapping = {}
    for match in _PAIR_PATTERN.finditer(block):
        key = match.group("key")
        values = [int(token.strip()) for token in match.group("values").split(",") if token.strip()]
        coords = tuple(zip(values[0::2], values[1::2]))
        layout[key] = coords
    return layout


def get_layout(name: str) -> LayoutMapping:
    """Public helper to fetch any layout block from the Patrick Wied asset."""

    return _parse_layout(name)


try:
    QWERTY_LAYOUT = _parse_layout("QWERTY")
except FileNotFoundError:  # pragma: no cover - repo layout issue
    QWERTY_LAYOUT = {}
except ValueError as exc:  # pragma: no cover - repo layout issue
    raise RuntimeError("Failed to parse QWERTY layout") from exc
