from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image

from .analysis import KeyboardAnalysis
from .gradients import get_colormap

_DEFAULT_BACKGROUND = Path(__file__).resolve().parents[1] / "patrick-wied.at" / "img" / "QWERTY.png"


def _build_kernel(radius_in: int, radius_out: int) -> np.ndarray:
    if radius_in < 0 or radius_out <= radius_in:
        raise ValueError("radius_out must be greater than radius_in and both must be positive")

    coords = np.arange(-radius_out, radius_out + 1, dtype=float)
    grid_x, grid_y = np.meshgrid(coords, coords)
    distance = np.sqrt(grid_x ** 2 + grid_y ** 2)
    kernel = np.zeros_like(distance, dtype=float)
    inner_mask = distance <= radius_in
    kernel[inner_mask] = 1.0

    transition_mask = (distance > radius_in) & (distance <= radius_out)
    kernel[transition_mask] = 1.0 - (distance[transition_mask] - radius_in) / (radius_out - radius_in)
    return kernel


def _accumulate_heatmap(point_counts: dict[Tuple[int, int], int], shape: tuple[int, int], kernel: np.ndarray) -> np.ndarray:
    heatmap = np.zeros(shape, dtype=float)
    radius = kernel.shape[0] // 2

    for (x, y), count in point_counts.items():
        if count <= 0:
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


def render_keyboard_heatmap(
    analysis: KeyboardAnalysis,
    *,
    output_path: Path | str,
    gradient: str = "cividis",
    background_path: Path | str | None = None,
    radius_in: int = 18,
    radius_out: int = 48,
    opacity: float = 1.0,
) -> None:
    """Render a keyboard heatmap image using Matplotlib colormaps."""

    output_path = Path(output_path)
    bg_path = Path(background_path) if background_path else _DEFAULT_BACKGROUND
    if not bg_path.exists():
        raise FileNotFoundError(f"Keyboard background not found: {bg_path}")

    background = Image.open(bg_path).convert("RGBA")
    width, height = background.size

    kernel = _build_kernel(radius_in, radius_out)
    heatmap = _accumulate_heatmap(dict(analysis.point_counts), (height, width), kernel)

    max_density = float(heatmap.max())
    if max_density <= 0:
        background.save(output_path)
        return

    norm_heat = heatmap / max_density
    cmap = get_colormap(gradient)
    rgba = cmap(norm_heat)

    rgb = (rgba[..., :3] * 255).astype(np.uint8)
    alpha = (norm_heat * 255 * opacity).clip(0, 255).astype(np.uint8)
    overlay = np.dstack([rgb, alpha])
    overlay_image = Image.fromarray(overlay, mode="RGBA")

    result = Image.alpha_composite(background, overlay_image)
    result.save(output_path)
