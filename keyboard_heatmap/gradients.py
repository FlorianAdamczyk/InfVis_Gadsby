"""Gradient presets inspired by Patrick Wied's heatmap.js demo."""
from __future__ import annotations

from typing import Dict, Tuple

from matplotlib import colormaps
from matplotlib.colors import Colormap, LinearSegmentedColormap

ColorStop = Tuple[float, str]

GRADIENT_PRESETS: Dict[str, Tuple[Tuple[float, str], ...]] = {
    "standard": (
        (0.00, "#0000ff"),
        (0.45, "#0000ff"),
        (0.55, "#00ffff"),
        (0.65, "#00ff00"),
        (0.95, "#ffff00"),
        (1.00, "#ff0000"),
    ),
    "nightly": (
        (0.00, "#ffffff"),
        (0.45, "#ffffff"),
        (0.70, "#000000"),
        (0.90, "#02fff6"),
        (1.00, "#032242"),
    ),
    "fanzy": (
        (0.00, "#d888d3"),
        (0.45, "#d888d3"),
        (0.55, "#00ffff"),
        (0.65, "#e93be9"),
        (0.95, "#ff00f0"),
        (1.00, "#ffff00"),
    ),
}


def resolve_colormap(name: str) -> Colormap:
    """Return either a Matplotlib built-in colormap or one of the legacy presets."""
    if name in colormaps:
        return colormaps[name]
    stops = GRADIENT_PRESETS.get(name)
    if stops:
        return LinearSegmentedColormap.from_list(name, stops)
    available = {"matplotlib": list(colormaps), "presets": list(GRADIENT_PRESETS)}
    raise KeyError(f"Unknown colormap '{name}'. Available presets: {', '.join(GRADIENT_PRESETS)}.")

