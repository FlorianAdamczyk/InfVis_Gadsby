import itertools
import os
import re
import subprocess
import sys


def safe_label(label: str) -> str:
    s = label.replace(" ", "_")
    s = re.sub(r"[^A-Za-z0-9_\\-]", "", s)
    return s


def main():
    works = [
        {
            "path": "01_Harry Potter - The Philosopher's Stone.txt",
            "label": "Harry Potter EN",
        },
        {
            "path": "01_Harry Potter und der Stein der Weisen.txt",
            "label": "Harry Potter DE",
        },
        {"path": "Gadsby_ Ernest Vincent Wright_1939.txt", "label": "Gadsby"},
    ]

    base_out = os.path.join("output_alt_viz")
    os.makedirs(base_out, exist_ok=True)

    pairs = list(itertools.permutations(works, 2))
    results = []

    for a, b in pairs:
        slug_a = safe_label(a["label"])
        slug_b = safe_label(b["label"])
        outdir = os.path.join(base_out, f"{slug_a}_vs_{slug_b}")
        os.makedirs(outdir, exist_ok=True)

        cmd = [
            sys.executable,
            os.path.join(".", "alternative_visualizations.py"),
            "--input",
            a["path"],
            "--compare-input",
            b["path"],
            "--input-label",
            a["label"],
            "--compare-label",
            b["label"],
            "--output-dir",
            outdir,
        ]

        print("\n--> Running:", " ".join(cmd))
        try:
            proc = subprocess.run(cmd, check=False)
            rc = proc.returncode
        except Exception as e:
            print(f"Command failed to start: {e}")
            rc = -1

        results.append((outdir, rc))
        if rc == 0:
            print(f"OK: output written to {outdir}")
        else:
            print(f"ERROR (code {rc}): see above output for {outdir}")

    print("\nSummary:")
    for outdir, rc in results:
        status = "OK" if rc == 0 else f"ERROR({rc})"
        print(f" - {outdir}: {status}")


if __name__ == "__main__":
    main()
