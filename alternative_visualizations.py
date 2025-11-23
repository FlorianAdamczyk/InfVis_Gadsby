from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from keyboard_heatmap import QWERTY_LAYOUT, analyze_text, load_text

LETTERS: Tuple[str, ...] = tuple(chr(code) for code in range(ord("A"), ord("Z") + 1))
LANGUAGE_COLORS = ("#1b9e77", "#d95f02")
BOOK_ALIASES = {
    "gadsby_ ernest vincent wright_1939.txt": "Gadsby",
    "01_harry potter - the philosopher's stone.txt": "HPeng",
    "01_harry potter und der stein der weisen.txt": "HPde",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create alternative visualizations for letter distributions of two texts."
    )
    parser.add_argument("--input", required=True, help="Primary text file (e.g., English).")
    parser.add_argument("--compare-input", required=True, help="Secondary text file (e.g., German).")
    parser.add_argument(
        "--input-label",
        default="Text A",
        help="Label for the primary text (used in figure titles and legends).",
    )
    parser.add_argument(
        "--compare-label",
        default="Text B",
        help="Label for the secondary text.",
    )
    parser.add_argument(
        "--output-dir",
        default="output_alt_viz",
        help="Directory where visualization PNG files will be written.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of characters to load from each text (helpful for testing).",
    )
    return parser.parse_args()


def load_analysis(path: Path, limit: int | None) -> Tuple[str, Dict[str, int], int]:
    text = load_text(path)
    if limit is not None:
        text = text[:limit]
    analysis = analyze_text(text, QWERTY_LAYOUT)
    counts = {letter: analysis.key_counts.get(letter, 0) for letter in LETTERS}
    total = sum(counts.values()) or 1
    return text, counts, total


def compute_freq(counts: Dict[str, int], total: int) -> Dict[str, float]:
    return {letter: counts.get(letter, 0) / total for letter in LETTERS}


def slugify(label: str) -> str:
    safe = label.strip().lower().replace(" ", "-")
    return "".join(ch for ch in safe if ch.isalnum() or ch == "-")


def detect_book_label(path: Path) -> str:
    key = path.name.lower()
    if key in BOOK_ALIASES:
        return BOOK_ALIASES[key]
    return slugify(path.stem)


def plot_single_bar(freq: Dict[str, float], label: str, output_path: Path) -> None:
    sorted_items = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    letters, values = zip(*sorted_items)

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.barh(letters, np.array(values) * 100, color="#367bb7")
    ax.invert_yaxis()
    ax.set_xlabel("Anteil am Text (%)")
    ax.set_title(f"{label}: Häufigkeiten der Buchstaben")

    for bar, value in zip(bars, values):
        ax.text(
            0.2,
            bar.get_y() + bar.get_height() / 2,
            f"{value * 100:.1f}%",
            va="center",
            ha="left",
            color="white",
            fontsize=8,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def top_letters(freq_a: Dict[str, float], freq_b: Dict[str, float], top_n: int = 15) -> List[str]:
    combined = {letter: freq_a.get(letter, 0) + freq_b.get(letter, 0) for letter in LETTERS}
    ranked = sorted(combined.items(), key=lambda kv: kv[1], reverse=True)
    return [letter for letter, _ in ranked[:top_n]]


def plot_grouped_bars(
    freq_a: Dict[str, float],
    freq_b: Dict[str, float],
    label_a: str,
    label_b: str,
    output_path: Path,
    top_n: int = 15,
) -> None:
    letters = top_letters(freq_a, freq_b, top_n)
    idx = np.arange(len(letters))
    width = 0.38

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        idx - width / 2,
        [freq_a[l] * 100 for l in letters],
        width,
        label=label_a,
        color=LANGUAGE_COLORS[0],
    )
    ax.bar(
        idx + width / 2,
        [freq_b[l] * 100 for l in letters],
        width,
        label=label_b,
        color=LANGUAGE_COLORS[1],
    )

    ax.set_xticks(idx)
    ax.set_xticklabels(letters)
    ax.set_ylabel("Anteil am Text (%)")
    ax.set_title("Top-Buchstaben im Vergleich")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_diverging_difference(
    freq_a: Dict[str, float], freq_b: Dict[str, float], label_a: str, label_b: str, output_path: Path
) -> None:
    data = [(letter, freq_a.get(letter, 0) - freq_b.get(letter, 0)) for letter in LETTERS]
    sorted_data = sorted(data, key=lambda kv: kv[1])
    letters, diffs = zip(*sorted_data)
    perc_diffs = np.array(diffs) * 100

    colors = [LANGUAGE_COLORS[1] if diff < 0 else LANGUAGE_COLORS[0] for diff in perc_diffs]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(letters, perc_diffs, color=colors)
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set_xlabel("Differenz in Prozentpunkten")
    ax.set_title(f"{label_a} minus {label_b}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_cumulative_share(
    freq_a: Dict[str, float], freq_b: Dict[str, float], label_a: str, label_b: str, output_path: Path
) -> None:
    sorted_a = sorted(freq_a.values(), reverse=True)
    sorted_b = sorted(freq_b.values(), reverse=True)
    cumulative_a = np.cumsum(sorted_a) * 100
    cumulative_b = np.cumsum(sorted_b) * 100
    ranks = np.arange(1, len(sorted_a) + 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ranks, cumulative_a, marker="o", label=label_a, color=LANGUAGE_COLORS[0])
    ax.plot(ranks, cumulative_b, marker="s", label=label_b, color=LANGUAGE_COLORS[1])
    ax.set_xlabel("Anzahl unterschiedlicher Buchstaben (nach Häufigkeit)")
    ax.set_ylabel("Abgedeckter Textanteil (%)")
    ax.set_xticks(ranks)
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.3)
    ax.legend()
    ax.set_title("Kumulative Abdeckung der häufigsten Buchstaben")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    path_a = Path(args.input)
    path_b = Path(args.compare_input)

    _, counts_a, total_a = load_analysis(path_a, args.limit)
    _, counts_b, total_b = load_analysis(path_b, args.limit)

    freq_a = compute_freq(counts_a, total_a)
    freq_b = compute_freq(counts_b, total_b)

    label_a = detect_book_label(path_a)
    label_b = detect_book_label(path_b)
    combo_label = f"{label_a}{label_b}"
    base_name = f"alt_{combo_label}"

    plot_single_bar(freq_a, args.input_label, output_dir / f"{base_name}_{label_a}_bar.png")
    plot_grouped_bars(
        freq_a,
        freq_b,
        args.input_label,
        args.compare_label,
        output_dir / f"{base_name}_grouped.png",
    )
    plot_diverging_difference(
        freq_a,
        freq_b,
        args.input_label,
        args.compare_label,
        output_dir / f"{base_name}_diff.png",
    )
    plot_cumulative_share(
        freq_a,
        freq_b,
        args.input_label,
        args.compare_label,
        output_dir / f"{base_name}_cumulative.png",
    )

    print(f"Saved visualizations to {output_dir}")


if __name__ == "__main__":
    main()
