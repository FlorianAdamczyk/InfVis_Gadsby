from __future__ import annotations

from pathlib import Path
from typing import Mapping, Tuple

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from PIL import Image

from .gradients import get_colormap

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


def _accumulate_heatmap(point_counts: Mapping[Tuple[int, int], float], shape: tuple[int, int], kernel: np.ndarray) -> np.ndarray:
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


def _apply_transforms(data: np.ndarray, gamma: float, use_log_scale: bool) -> np.ndarray:
    transformed = data.copy()
    if use_log_scale:
        transformed = np.sign(transformed) * np.log1p(np.abs(transformed))
    if gamma and gamma > 0 and not np.isclose(gamma, 1.0):
        transformed = np.sign(transformed) * (np.abs(transformed) ** (1.0 / gamma))
    return transformed


def _build_norm(data: np.ndarray, scale_type: str, center: float) -> colors.Normalize:
    data_min = float(np.min(data))
    data_max = float(np.max(data))

    if scale_type == "diverging":
        max_abs = max(abs(data_min - center), abs(data_max - center))
        if max_abs == 0:
            max_abs = 1.0
        vmin = center - max_abs
        vmax = center + max_abs
        return colors.TwoSlopeNorm(vcenter=center, vmin=vmin, vmax=vmax)

    vmin = 0.0 if data_min >= 0 else data_min
    vmax = data_max if data_max > 0 else 1.0
    if np.isclose(vmin, vmax):
        vmax = vmin + 1.0
    return colors.Normalize(vmin=vmin, vmax=vmax)


def render_keyboard_heatmap(
    point_counts: Mapping[Tuple[int, int], float],
    *,
    output_path: Path | str,
    layout_name: str = "QWERTY",
    gradient: str = "cividis",
    background_path: Path | str | None = None,
    blur_sigma: float = 10.0,
    blur_truncate: float = 3.0,
    gamma: float = 1.3,
    opacity: float = 0.9,
    use_log_scale: bool = False,
    scale_type: str = "sequential",
    center: float = 0.0,
    colorbar_label: str | None = None,
) -> None:
    """Render a keyboard heatmap image using Matplotlib colormaps and a labeled colorbar."""

    output = Path(output_path)
    bg_path = Path(background_path) if background_path else _DEFAULT_BACKGROUND
    if not bg_path.exists():
        raise FileNotFoundError(f"Keyboard background not found: {bg_path}")

    background = Image.open(bg_path).convert("RGBA")
    width, height = background.size

    kernel = _build_kernel(blur_sigma, blur_truncate)
    heatmap = _accumulate_heatmap(point_counts, (height, width), kernel)

    if not np.any(heatmap):
        background.save(output)
        return

    transformed = _apply_transforms(heatmap, gamma=gamma, use_log_scale=use_log_scale)
    cmap = get_colormap(gradient)
    norm = _build_norm(transformed, scale_type, center)

    data_label = colorbar_label or (
        "Relative key frequency"
        if scale_type != "diverging"
        else "Relative frequency difference"
    )
    if use_log_scale:
        data_label += " (log)"
    if scale_type == "diverging":
        data_label += f" ({layout_name})"

    dpi = 110
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax.imshow(background)
    im = ax.imshow(transformed, cmap=cmap, norm=norm, alpha=opacity, origin="upper")
    ax.set_title(f"Keyboard Heatmap — {layout_name}")
    ax.axis("off")

    cbar = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.046, pad=0.08)
    cbar.set_label(data_label)

    fig.savefig(output, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
