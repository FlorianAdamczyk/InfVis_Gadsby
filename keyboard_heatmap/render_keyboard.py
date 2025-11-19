"""Rendering utilities for coloring QWERTY keys based on usage."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize

from .gradients import build_colormap
from .layout_qwerty import CANVAS_HEIGHT, CANVAS_WIDTH, KEYBOXES, iter_key_rects
from .text_counts import AnalysisResult


DEFAULT_FIGURE_WIDTH = 12
DEFAULT_DPI = 200


def render_keyboard_heatmap(
    analysis: AnalysisResult,
    *,
    output_path: str | Path,
    gradient: str = "standard",
    show_colorbar: bool = True,
    annotate_frequencies: bool = True,
    background_color: str = "#1b1b1f",
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmap = build_colormap(gradient)
    rect_values: Dict[Tuple[float, float], int] = {}
    rect_labels: Dict[Tuple[float, float], str] = {}

    for label, rect in KEYBOXES.items():
        center = rect.center
        rect_labels.setdefault(center, rect.label)
        rect_values.setdefault(center, 0)
        rect_values[center] += analysis.key_counts.get(label, 0)

    max_value = max(rect_values.values(), default=1)
    norm = Normalize(vmin=0, vmax=max_value)

    fig_height = DEFAULT_FIGURE_WIDTH * (CANVAS_HEIGHT / CANVAS_WIDTH)
    fig, ax = plt.subplots(figsize=(DEFAULT_FIGURE_WIDTH, fig_height), dpi=DEFAULT_DPI)
    ax.set_facecolor(background_color)
    ax.set_xlim(0, CANVAS_WIDTH)
    ax.set_ylim(CANVAS_HEIGHT, 0)
    ax.axis("off")

    for rect in iter_key_rects():
        center = rect.center
        value = rect_values.get(center, 0)
        color = cmap(norm(value)) if max_value > 0 else cmap(0)
        patch = Rectangle(
            (rect.x, rect.y),
            rect.width,
            rect.height,
            facecolor=color,
            edgecolor="#2b2b2b",
            linewidth=1.5,
            joinstyle="round",
        )
        ax.add_patch(patch)

        label = rect_labels.get(center, rect.label)
        ax.text(
            rect.x + rect.width / 2,
            rect.y + rect.height / 2,
            label,
            ha="center",
            va="center",
            fontsize=10,
            color="white",
            weight="bold",
        )
        if annotate_frequencies and value > 0 and analysis.total_characters > 0:
            rel = value / analysis.total_characters
            ax.text(
                rect.x + rect.width / 2,
                rect.y + rect.height - 8,
                f"{rel:.1%}",
                ha="center",
                va="top",
                fontsize=6,
                color="#f0f0f0",
            )

    if show_colorbar:
        sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, shrink=0.4, pad=0.02)
        cbar.set_label("Anschläge pro Taste")

    fig.suptitle("Keyboard Heatmap – QWERTY", color="white")
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path
