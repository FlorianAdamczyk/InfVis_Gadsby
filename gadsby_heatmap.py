from __future__ import annotations

import argparse
from pathlib import Path

from keyboard_heatmap import (
    GRADIENT_PRESETS,
    QWERTY_LAYOUT,
    analyze_text,
    load_text,
    render_keyboard_heatmap,
)
from keyboard_heatmap.text_counts import export_counts_to_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a keyboard heatmap for a given text.")
    parser.add_argument("--input", required=True, help="Path to the input text file")
    parser.add_argument("--output-dir", default="output", help="Directory for generated assets")
    parser.add_argument("--gradient", default="standard", choices=GRADIENT_PRESETS.keys(), help="Color gradient preset")
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Characters to exclude from the count (default: none)",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Optional maximum number of characters to read from the text"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = load_text(args.input)
    if args.limit:
        text = text[: args.limit]

    analysis = analyze_text(text, QWERTY_LAYOUT, excludes=args.exclude)

    image_path = output_dir / "keyboard_heatmap_qwerty.png"
    csv_path = output_dir / "keyboard_letter_counts.csv"
    unmapped_path = output_dir / "unmapped_characters.txt"

    render_keyboard_heatmap(analysis, output_path=image_path, gradient=args.gradient)
    export_counts_to_csv(csv_path, analysis)

    if analysis.unmapped_counts:
        with unmapped_path.open("w", encoding="utf-8") as fh:
            for char, count in analysis.unmapped_counts.most_common():
                fh.write(f"{char}\t{count}\n")

    print(f"Saved heatmap to {image_path}")
    print(f"Saved CSV stats to {csv_path}")
    if analysis.unmapped_counts:
        print(f"See {unmapped_path} for unmapped characters")


if __name__ == "__main__":
    main()
