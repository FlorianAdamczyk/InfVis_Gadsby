# Benutzung — Keyboard Heatmap

Dieses Dokument fasst alle derzeit umgesetzten Einstellmöglichkeiten zusammen und bewertet die Abdeckung der Anforderungen aus `Task.md`.

## Verfügbare CLI-Optionen (`gadsby_heatmap.py`)

- `--input <DATEI>`: Textquelle, UTF-8.
- `--output-dir <VERZ>`: Zielverzeichnis (Standard `output`).
- `--cmap <NAME>`: Matplotlib-Colormap oder Preset (`standard`, `nightly`, `fanzy`).
- `--scale {linear,log}`: Linear (Standard) oder logarithmisch, um Ausreißer zu entschärfen.
- `--compare-input <DATEI>`: Zweiter Text für relative Häufigkeitsvergleiche (benötigt divergierende Palette, z. B. `coolwarm`).
- `--exclude <ZEICHEN …>`: Zusätzliche Zeichen, die ignoriert werden sollen (Space wird immer ignoriert).
- `--limit <N>`: Optionaler Ausschnitt beider Texte (auch für Vergleich angewandt).

## Rendering & Ausgabe

- Heatmap nutzt Gauß-Blur (konfigurierbar im Code via `blur_sigma`, `blur_truncate`) und Gamma (`gamma`).
- Jeder Export enthält automatisch eine horizontal platzierte Legende inkl. Colormap-Namen.
- Dateien: `keyboard_heatmap_qwerty(.png)`, CSV (`keyboard_letter_counts*.csv`) sowie `unmapped_characters*.txt`.

### Alternative Visualisierungen

- Script: `alternative_visualizations.py`
	- Argumente: `--input`, `--compare-input`, optionale Labels, `--limit`, `--output-dir` (Standard `output_alt_viz`).
	- Nutzt denselben Analysepfad (`keyboard_heatmap.analyze_text`) und erzeugt derzeit vier Darstellungen ohne Keyboard-Layout:
		1. **Sortiertes Balkendiagramm** der Buchstabenhäufigkeiten für Text A (`01_<label>_bar.png`).
		2. **Gruppierte Balken** (Top 15 Zeichen) zum direkten Vergleich (`02_grouped_top15.png`).
		3. **Divergierende Differenzbalken** (Text A – Text B) mit Null-Linie (`03_diverging_difference.png`).
		4. **Kumulative Abdeckung**: Linienplot zeigt, wie viele Buchstabenanteile mit den häufigsten Zeichen erklärt werden (`04_cumulative_coverage.png`).
- Alle Diagramme verwenden farbfehlsichtrobuste Paletten (ColorBrewer-inspirierte Grüntöne/Orangetöne) und beschriftete Achsen/Legenden gemäß Aufgabenstellung.

## Farbskalen & Vergleichbarkeit (Bezug zu `Task.md`)

- **Sequentiell vs. Divergierend:** Alle Matplotlib-Skalen verfügbar → sequentielle (z. B. `cividis`) und divergierende (`coolwarm`, `seismic`).
- **Logarithmische Betrachtung:** Via `--scale log` aktivierbar (nur im Single-Text-Modus, Kombination mit Vergleich nicht sinnvoll).
- **Relative Vergleiche:** `--compare-input` erzeugt eine TwoSlopeNorm (Center = 0). Gleich häufig → Mittelwert der Palette; weniger/häufiger → linke/rechte Farbhälfte.
- **Legende:** Wird unterhalb ausgegeben (inkl. Hinweis linear/log bzw. relative diff).

## Definition & Dateneignung (Zusammenfassung)

- Die Heatmap stellt pro Taste die (relative) Häufigkeit als Farbintensität dar.
- Geeignet für metrische Häufigkeiten mit räumlicher Zuordnung; Binning erfolgt per Key-Koordinate, nicht pixelweise.
- Skalensteuerung: linear/log (Single), divergierend mit Center (Comparison). Ausreißer=Log/PowerNorm, Nullpunkt=TwoSlopeNorm.

## Noch offene Punkte

1. **CLI-Exposition zusätzlicher Renderparameter** (`blur_sigma`, `gamma`, `opacity`).
2. **Automatische Farbschemata für Barrierefreiheit** (z. B. Shortcut `--colorblind`).
3. **Mehrfach-Exports pro Lauf** (z. B. sequentiell + divergierend für Präsentationsfolien).
4. **Optionale Binning-/Resolution-Kontrolle** über ein separates Raster.

Mit den aktuellen Optionen lassen sich jedoch bereits alle in `Task.md` genannten Aspekte (Farbskala, Legende, Nullpunkt/Center, logarithmische Betrachtung) gezielt adressieren.
