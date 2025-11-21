"""High-level helpers for generating keyboard heatmaps."""
from .analysis import KeyboardAnalysis, analyze_text, load_text
from .layouts import QWERTY_LAYOUT
from .render import render_keyboard_heatmap
from .comparison import compute_relative_difference_points

__all__ = [
    "KeyboardAnalysis",
    "QWERTY_LAYOUT",
    "analyze_text",
    "load_text",
    "render_keyboard_heatmap",
    "compute_relative_difference_points",
]
