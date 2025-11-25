from __future__ import annotations

from functools import lru_cache
import matplotlib as mpl
from matplotlib.colors import Colormap, LinearSegmentedColormap

_CUSTOM_GRADIENT_DEFS = {
    "standard": [
        (0.0, "#0000FF"),
        (0.45, "#0000FF"),
        (0.55, "#00FFFF"),
        (0.65, "#00FF00"),
        (0.95, "#FFFF00"),
        (1.0, "#FF0000"),
    ],
    "nightly": [
        (0.0, "#FFFFFF"),
        (0.45, "#FFFFFF"),
        (0.70, "#000000"),
        (0.90, "#02FFF6"),
        (1.0, "#032242"),
    ],
    "fanzy": [
        (0.0, "#D888D3"),
        (0.45, "#D888D3"),
        (0.55, "#00FFFF"),
        (0.65, "#E93BE9"),
        (0.95, "#FF00F0"),
        (1.0, "#FFFF00"),
    ],
}


@lru_cache(maxsize=None)
def _build_custom_colormap(name: str) -> LinearSegmentedColormap:
    stops = _CUSTOM_GRADIENT_DEFS[name]
    return LinearSegmentedColormap.from_list(name, stops)


_REVERSE_SUFFIXES = ("-inverse", "_inverse", "-reverse", "_reverse")


def _normalize_colormap_name(name: str) -> tuple[str, bool]:
    key = name.strip().lower()
    reverse = False
    for suffix in _REVERSE_SUFFIXES:
        if key.endswith(suffix):
            reverse = True
            key = key[: -len(suffix)]
            break
    key = key.strip("-_")
    return key, reverse


def available_presets() -> list[str]:
    return sorted(_CUSTOM_GRADIENT_DEFS.keys())


def get_colormap(name: str) -> Colormap:
    key, reverse = _normalize_colormap_name(name)
    if not key:
        raise ValueError(
            f"Unknown colormap '{name}'. Use a Matplotlib colormap or one of: {', '.join(available_presets())}"
        )
    if key in _CUSTOM_GRADIENT_DEFS:
        cmap = _build_custom_colormap(key)
    elif key in mpl.colormaps:
        cmap = mpl.colormaps[key]
    else:
        raise ValueError(
            f"Unknown colormap '{name}'. Use a Matplotlib colormap or one of: {', '.join(available_presets())}"
        )
    if reverse:
        cmap = cmap.reversed()
    return cmap
