from __future__ import annotations

import argparse
from pathlib import Path

from keyboard_heatmap import (
    QWERTY_LAYOUT,
    analyze_text,
    compute_relative_difference_points,
    load_text,
    render_keyboard_heatmap,
)
from keyboard_heatmap.text_counts import export_counts_to_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a keyboard heatmap for a given text.")
    parser.add_argument("--input", required=True, help="Path to the input text file")
    parser.add_argument("--output-dir", default="output", help="Directory for generated assets")
    parser.add_argument(
        "--cmap",
        default="cividis",
        help=(
            "Matplotlib colormap name (e.g. cividis, plasma, viridis) or one of the presets: "
            "standard, nightly, fanzy"
        ),
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=None,
        help="Characters to exclude in addition to the defaults (space is excluded by default)",
    )
    parser.add_argument(
        "--scale",
        choices=("linear", "log"),
        default="linear",
        help="Intensity scaling for the heatmap (log dampens extreme outliers)",
    )
    parser.add_argument(
        "--compare-input",
        default=None,
        help="Optional second text file. If provided, renders a relative frequency comparison heatmap.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of characters to read from the text",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = load_text(args.input)
    if args.limit:
        text = text[: args.limit]
    input_chars = len(text)

    analysis = analyze_text(text, QWERTY_LAYOUT, excludes=args.exclude)

    comparison_path = Path(args.compare_input) if args.compare_input else None
    comparison_analysis = None
    comparison_points = None

    if comparison_path:
        comparison_text = load_text(comparison_path)
        if args.limit:
            comparison_text = comparison_text[: args.limit]
        comparison_analysis = analyze_text(comparison_text, QWERTY_LAYOUT, excludes=args.exclude)
        comparison_points = compute_relative_difference_points(analysis, comparison_analysis)

    image_name = "keyboard_heatmap_qwerty_compare.png" if comparison_points else "keyboard_heatmap_qwerty.png"
    image_path = output_dir / image_name
    csv_path = output_dir / "keyboard_letter_counts.csv"
    unmapped_path = output_dir / "unmapped_characters.txt"

    render_keyboard_heatmap(
        analysis,
        output_path=image_path,
        gradient=args.cmap,
        scale=args.scale,
        comparison_points=comparison_points,
        legend=True,
    )
    export_counts_to_csv(csv_path, analysis)

    if comparison_analysis:
        comparison_csv = output_dir / "keyboard_letter_counts_compare.csv"
        export_counts_to_csv(comparison_csv, comparison_analysis)
        cmp_unmapped = output_dir / "unmapped_characters_compare.txt"
        if comparison_analysis.unmapped_counts:
            with cmp_unmapped.open("w", encoding="utf-8") as fh:
                for char, count in comparison_analysis.unmapped_counts.most_common():
                    fh.write(f"{char}\t{count}\n")
        print(f"Saved comparison CSV stats to {comparison_csv}")
        if comparison_analysis.unmapped_counts:
            print(f"See {cmp_unmapped} for unmapped comparison characters")

    if analysis.unmapped_counts:
        with unmapped_path.open("w", encoding="utf-8") as fh:
            for char, count in analysis.unmapped_counts.most_common():
                fh.write(f"{char}\t{count}\n")

    print(f"Processed {analysis.total_characters} mapped characters (input slice length: {input_chars}).")
    if comparison_analysis:
        print(f"Processed {comparison_analysis.total_characters} mapped characters for comparison text.")
    print(f"Saved heatmap to {image_path}")
    print(f"Saved CSV stats to {csv_path}")
    if analysis.unmapped_counts:
        print(f"See {unmapped_path} for unmapped characters")


if __name__ == "__main__":
    main()
