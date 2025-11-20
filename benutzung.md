# Benutzung — Keyboard Heatmap

## Zweck

Kurzüberblick über alle derzeit implementierten Optionen (CLI und Rendering), Zuordnung zu den Anforderungen aus `Task.md` sowie offene Punkte.

## Verfügbare Optionen

### Eingabe / CLI

- `--input <DATEI>`: Haupttext (Pflicht).
- `--compare-with <DATEI>`: Zweiter Text für relative Analyse (optional, erzwingt divergierende Skala).
- `--output-dir <VERZ>`: Ziel für PNG/CSV (Standard `output`).
- `--limit <N>`: Textlänge beschränken (wird auf beide Texte angewandt).
- `--exclude <ZEICHEN...>`: Zusätzliche auszuschließende Zeichen.
- `--cmap <NAME>`: Matplotlib-Colormap oder Preset (`standard`, `nightly`, `fanzy`).
- `--scale-type {auto,sequential,diverging}`: Steuerung der Normierung. `auto` = sequentiell, außer bei Vergleich.
- `--center <WERT>`: Nullpunkt für divergierende Skalen (default `0`).
- `--log-scale`: Logarithmische Betrachtung der Häufigkeiten (auch bei Vergleichen möglich).

### Rendering

- Heatmap basiert auf identischen Koordinaten wie Patrick Wied (`patrick-wied.at/keyboard-layouts.js`).
- Gaussian Blur (`blur_sigma`, `blur_truncate`) plus Gamma-Tuning (Standardwerte im Code) sorgen für weiche Übergänge.
- Sequentiale Skalen beginnen stets beim kleinsten Wert; divergierende Skalen werden symmetrisch um den Center-Wert aufgespannt.
- Optionaler Log-Schalter reduziert den Einfluss extremer Ausreißer (`log1p`).
- Vergleichsmodus erzeugt relative Frequenzdifferenzen (Text A − Text B) auf Basis normalisierter Key-Häufigkeiten.
- Jede Ausgabe enthält eine horizontale Farbskala/Legende mit Label (inkl. Hinweis auf Log-Skalierung).

### Output

- PNG: `keyboard_heatmap_qwerty.png` (inkl. Hintergrund + Legende).
- CSV: `keyboard_letter_counts.csv` (Text A) sowie, falls vorhanden, `keyboard_letter_counts_compare.csv` (Text B).
- `unmapped_characters.txt` mit Zeichen, die keinem Layout zugeordnet werden konnten.

## Bezug zu `Task.md`

| Task-Aspekt | Aktueller Stand |
| --- | --- |
| **Farbskala & Legende** | Sequentielle und divergierende Skalen über Matplotlib/Preset frei wählbar, inklusive farbiger Legende unterhalb des Bildes. Center/Nullpunkt steuerbar. |
| **Definition & Dateneignung** | Heatmap visualisiert metrische Häufigkeiten der Tastendrücke (bzw. deren Differenzen). Datenbasis wird beim Einlesen aggregiert (pro Key, optional log-skaliert). |
| **Ausreißer / Skala** | Log-Schalter (`--log-scale`) reduziert Ausreißer; Gamma-Weichzeichnung sorgt für flüssige Übergänge. |
| **Vergleich / Alternativen** | Vergleich zweier Texte (relative Häufigkeiten) verfügbar. Für Alternativen (Bar-/Small-Multiples) werden Hinweise in der Dokumentation empfohlen. |

## Fehlende bzw. optionale Ergänzungen

- **Weitere Layouts**: Parser unterstützt zwar alle im JS definierten Layouts, CLI bietet jedoch derzeit nur QWERTY an.
- **Direkte CLI-Steuerung für Blur/Gamma/Opacity**: derzeit nur über Codeänderung anpassbar.
- **Automatischer Export mehrerer Skalen**: aktuell ein Lauf = eine Skala; könnte erweitert werden, um sequentielle und divergierende Varianten parallel zu erstellen.
- **Kontrast-/Farbfehlsicht-Checks**: manuelle Prüfung nötig; optionale Presets/Validierung denkbar.
- **Weitere analytische KPIs**: z. B. Fingerbelastung, Zeilen-/Hand-Cluster könnten zur Reflexion beitragen.

## Beispielbefehle

```pwsh
# Sequentielle Heatmap mit Log-Skalierung
python gadsby_heatmap.py --input "text.txt" --cmap viridis --log-scale

# Vergleich zweier Texte mit divergierender Skala und Center 0
python gadsby_heatmap.py --input "text_a.txt" --compare-with "text_b.txt" --cmap coolwarm --scale-type diverging --center 0
```
