from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm, Normalize, PowerNorm, TwoSlopeNorm
from PIL import Image

from .analysis import KeyboardAnalysis
from .gradients import get_colormap

Coordinate = Tuple[int, int]
_DEFAULT_BACKGROUND = Path(__file__).resolve().parents[1] / "patrick-wied.at" / "img" / "QWERTY.png"


def _build_kernel(sigma: float, truncate: float) -> np.ndarray:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if truncate < 1.0:
        raise ValueError("truncate must be at least 1.0")

    radius = int(max(1, round(truncate * sigma)))
    coords = np.arange(-radius, radius + 1, dtype=float)
    grid_x, grid_y = np.meshgrid(coords, coords)
    distance_sq = grid_x ** 2 + grid_y ** 2
    kernel = np.exp(-distance_sq / (2 * sigma ** 2))
    kernel /= kernel.max() or 1.0
    return kernel


def _accumulate_heatmap(point_counts: Dict[Coordinate, float], shape: tuple[int, int], kernel: np.ndarray) -> np.ndarray:
    heatmap = np.zeros(shape, dtype=float)
    radius = kernel.shape[0] // 2

    for (x, y), count in point_counts.items():
        if count == 0:
            continue

        xi = int(round(x))
        yi = int(round(y))
        left = max(0, xi - radius)
        right = min(shape[1], xi + radius + 1)
        top = max(0, yi - radius)
        bottom = min(shape[0], yi + radius + 1)

        if left >= right or top >= bottom:
            continue

        kernel_left = left - (xi - radius)
        kernel_right = kernel_left + (right - left)
        kernel_top = top - (yi - radius)
        kernel_bottom = kernel_top + (bottom - top)

        heatmap[top:bottom, left:right] += kernel[kernel_top:kernel_bottom, kernel_left:kernel_right] * count

    return heatmap


def _build_norm(data: np.ndarray, scale: str, gamma: float, comparison: bool) -> Normalize:
    if comparison:
        abs_max = float(np.max(np.abs(data)))
        if abs_max <= 0:
            abs_max = 1.0
        return TwoSlopeNorm(vcenter=0.0, vmin=-abs_max, vmax=abs_max)

    vmax = float(np.max(data))
    if vmax <= 0:
        vmax = 1.0

    if scale == "log":
        positive = data[data > 0]
        vmin = float(np.min(positive)) if positive.size else 1e-6
        return LogNorm(vmin=vmin, vmax=vmax)

    if gamma and gamma != 1.0:
        gamma_value = 1.0 / gamma if gamma > 0 else 1.0
        return PowerNorm(gamma=gamma_value, vmin=0.0, vmax=vmax)

    return Normalize(vmin=0.0, vmax=vmax)


def _default_label(gradient: str, comparison: bool) -> str:
    if comparison:
        return f"{gradient} (relative freq diff)"
    return gradient


def render_keyboard_heatmap(
    analysis: KeyboardAnalysis,
    *,
    output_path: Path | str,
    gradient: str = "cividis",
    background_path: Path | str | None = None,
    blur_sigma: float = 16.0,
    blur_truncate: float = 45.0,
    gamma: float = 1.6,
    opacity: float = 1.0,
    scale: str = "linear",
    comparison_points: Dict[Coordinate, float] | None = None,
    legend: bool = True,
    legend_label: str | None = None,
    title: str | None = None,
) -> None:
    """Render a keyboard heatmap image with optional comparison & legend.

    The optional title is placed above the keyboard layout in the saved image.
    """

    if comparison_points is not None and scale == "log":
        raise ValueError("Log scaling is only supported for single-text heatmaps")

    output_path = Path(output_path)
    bg_path = Path(background_path) if background_path else _DEFAULT_BACKGROUND
    if not bg_path.exists():
        raise FileNotFoundError(f"Keyboard background not found: {bg_path}")

    background = Image.open(bg_path).convert("RGBA")
    width, height = background.size

    kernel = _build_kernel(blur_sigma, blur_truncate)
    source_points = comparison_points if comparison_points is not None else dict(analysis.point_counts)
    heatmap = _accumulate_heatmap(source_points, (height, width), kernel)

    if not np.any(np.abs(heatmap) > 0):
        background.save(output_path)
        return

    comparison_mode = comparison_points is not None
    norm = _build_norm(heatmap, scale, gamma, comparison_mode)
    cmap = get_colormap(gradient)

    display_data = heatmap.copy()
    if scale == "log" and not comparison_mode:
        display_data = np.where(display_data > 0, display_data, np.nan)

    alpha_source = np.abs(heatmap) if comparison_mode else np.clip(heatmap, 0, None)
    alpha_max = float(np.nanmax(alpha_source))
    if alpha_max > 0:
        alpha_map = np.clip(alpha_source / alpha_max, 0, 1) * opacity
    else:
        alpha_map = np.zeros_like(alpha_source)

    title_padding = 0.3 if title else 0.0
    fig_height = height / 100.0 + (0.6 if legend else 0.0) + title_padding
    fig, ax = plt.subplots(figsize=(width / 100.0, fig_height), dpi=100)
    ax.imshow(background)
    im = ax.imshow(display_data, cmap=cmap, norm=norm, alpha=alpha_map, interpolation="bilinear")
    ax.axis("off")
    if title:
        ax.set_title(title, pad=10, fontsize=14, weight="bold")

    if legend:
        cbar = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.05, pad=0.05)
        cbar.set_label(legend_label or _default_label(gradient, comparison_mode))
        # remove numeric tick labels under the colorbar per user request
        try:
            cbar.ax.set_xticks([])
        except Exception:
            # fallback for vertical orientation
            cbar.ax.set_yticks([])

    fig.savefig(output_path, dpi=100, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
