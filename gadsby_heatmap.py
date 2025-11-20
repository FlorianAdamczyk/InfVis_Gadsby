from __future__ import annotations

import argparse
from pathlib import Path

from keyboard_heatmap import (
    QWERTY_LAYOUT,
    analyze_text,
    load_text,
    relative_point_difference,
    render_keyboard_heatmap,
)
from keyboard_heatmap.text_counts import export_counts_to_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a keyboard heatmap for a given text.")
    parser.add_argument("--input", required=True, help="Path to the input text file")
    parser.add_argument("--compare-with", help="Optional second text file for relative comparison")
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
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of characters to read from the text",
    )
    parser.add_argument(
        "--scale-type",
        choices=["auto", "sequential", "diverging"],
        default="auto",
        help="Control how the color scale should be interpreted (sequential, diverging, or auto).",
    )
    parser.add_argument(
        "--center",
        type=float,
        default=0.0,
        help="Center/zero point for diverging color scales (default: 0.0).",
    )
    parser.add_argument(
        "--log-scale",
        action="store_true",
        help="Apply logarithmic scaling to the heatmap intensities to reduce the impact of outliers.",
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

    comparison_analysis = None
    comparison_chars = None
    if args.compare_with:
        compare_text = load_text(args.compare_with)
        if args.limit:
            compare_text = compare_text[: args.limit]
        comparison_chars = len(compare_text)
        comparison_analysis = analyze_text(compare_text, QWERTY_LAYOUT, excludes=args.exclude)

    image_path = output_dir / "keyboard_heatmap_qwerty.png"
    csv_path = output_dir / "keyboard_letter_counts.csv"
    unmapped_path = output_dir / "unmapped_characters.txt"

    scale_type = args.scale_type
    colorbar_label = "Relative key frequency"
    point_source = analysis.point_counts
    center = args.center

    if comparison_analysis:
        scale_type = "diverging" if scale_type == "auto" else scale_type
        colorbar_label = "Relative frequency difference (A - B)"
        point_source = relative_point_difference(analysis, comparison_analysis)
        compare_csv = output_dir / "keyboard_letter_counts_compare.csv"
        export_counts_to_csv(compare_csv, comparison_analysis)
    elif scale_type == "auto":
        scale_type = "sequential"

    render_keyboard_heatmap(
        point_source,
        output_path=image_path,
        layout_name="QWERTY",
        gradient=args.cmap,
        use_log_scale=args.log_scale,
        scale_type=scale_type,
        center=center,
        colorbar_label=colorbar_label,
    )

    export_counts_to_csv(csv_path, analysis)

    if analysis.unmapped_counts:
        with unmapped_path.open("w", encoding="utf-8") as fh:
            for char, count in analysis.unmapped_counts.most_common():
                fh.write(f"{char}\t{count}\n")

    print(f"Processed {analysis.total_characters} mapped characters (input slice length: {input_chars}).")
    if comparison_analysis:
        print(
            f"Comparison text processed {comparison_analysis.total_characters} mapped characters "
            f"(input slice length: {comparison_chars})."
        )
    print(f"Saved heatmap to {image_path}")
    print(f"Saved CSV stats to {csv_path}")
    if analysis.unmapped_counts:
        print(f"See {unmapped_path} for unmapped characters")


if __name__ == "__main__":
    main()
