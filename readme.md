# README — Übungen Datenvisualisierung (WS 2025/26)  

Dieses Repository enthält die Abgaben zu Übung B — Aufgabe 5 (Heatmaps). Die README fasst Ziele, Anforderungen und Abliefermodalitäten der Aufgabe zusammen.

## Kurzüberblick & Ziele

- Ziel: Verzerrungen in Diagrammen erkennen und vermeiden; fundierte Designentscheidungen auf Basis von Wahrnehmung, Farbwahl und Barrierefreiheit treffen.  
- Speziell Aufgabe 5: Verständnis und Anwendung von Heatmaps; exemplarische Anwendung einer Keyboard-Heatmap.

## Organisatorisches

- Arbeit: 3er-Team (Mitglieder: Aaron, Christopher, Flo).  
- Präsentation: Kurzvorstellung 5–10 Minuten (falls gehalten).  
- Werkzeuge: frei wählbar (z. B. Excel, Python/Matplotlib/Altair, R/ggplot2, Observable/D3, Power BI, Tableau).

## Abgabeformate & Benennung

- Videodatei (wenn vorhanden): MP4, H.264/AAC, Dateiname: `InfoVis_Üxx_Initialen.mp4`  
- Präsentationsfolien: PPTX empfohlen oder PDF (16:9).  
- PDF-Abgabe: `dv25_uXX_nachname_nachname_kurztitel.pdf` (z. B. `dv25_u02_mueller-meier_heatmap.pdf`)  
- Liefere reproduzierbar: Quellcode, Daten, Skripte und erzeugte Bilder im Repo.

## Aufgabe 5 — Heatmaps (Kurzversion)

a) Definition & Dateneignung  

- Beschreibe, was eine Heatmap darstellt und welche Dateneigenschaften geeignet sind (metrische Werte, Bin-Größe/Auflösung, Skala, Ausreißer, Nullpunkt/Center).

b) Beispiele beurteilen  

- Suche je ein geeignetes und ein ungeeignetes Heatmap-Beispiel und begründe (Aufgabe, Lesbarkeit, Farbskala, Legende, Aggregation, Alternativen).

c) Anwendung  

- Erstelle oder kopiere einen Beispieltext (Deutsch/Englisch) ≥ 100 Wörter (mit Quellenangabe).  
- Wende den Text auf die Keyboard-Heatmap an und speichere das resultierende Bild ins Repo.

d) Diskussion  

- Analysiere die Heatmap: Erkenntnisse, Bedeutung einzelner Buchstaben, Vergleich zu anderen Kodierungen (z. B. Morse), Bewertung von Farbskala & Legende.

Material: [Keyboard-Heatmap (Patrick Wied)](https://www.patrick-wied.at/projects/heatmap-keyboard/)

## Barrierefreiheit & Ethik

- Verwende geeignete Farbpaletten (sequentiell/divergierend); prüfe Kontraste und biete wenn sinnvoll eine farbfehlsichtrobuste Variante an.  
- Datenquellen sauber zitieren; keine personenbezogenen Daten ohne Rechtsgrundlage.

## Abgabeinhalt (Pflicht)

- Präsentation (PDF/PPTX) mit: Problem & Ziel, Daten & Kodierungen, Designentscheidungen, Ergebnis & Fazit (je 1 Folie), Reflexion optional.  
- Generierter Heatmap-Bilddatei (PNG/JPG) und Skript/Code zur Reproduktion.  
- Quellenangaben für Text, Beispiele und Tools.

## Reproduzierbare Keyboard-Heatmaps

Das Skript `gadsby_heatmap.py` erzeugt auf Basis der Patrick-Wied-Tastaturgrafik eine Heatmap samt CSV-Auswertung. Die Python-Implementierung nutzt dieselben Koordinaten wie das Original und stellt mehrere Farbskalen bereit (sequentiell via Matplotlib, divergend oder die drei Presets `standard`, `nightly`, `fanzy`).

### Vorbereitung

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Heatmap generieren

```pwsh
python gadsby_heatmap.py --input "Gadsby_ Ernest Vincent Wright_1939.txt" --output-dir output --cmap cividis
```

- `--cmap` akzeptiert jeden Matplotlib-Colormap-Namen oder die Presets `standard`, `nightly`, `fanzy`.
- `--scale-type` steuert die Normalisierung: `sequential` startet beim kleinsten Wert, `diverging` nutzt den Center-Wert (Default: auto).
- `--center` verschiebt den Nullpunkt bei divergierenden Skalen (default `0`).
- `--log-scale` aktiviert eine logarithmische Betrachtung der Häufigkeiten.
- Optional `--exclude` für zusätzliche Zeichenfilter sowie `--limit` zum Beschneiden langer Texte.
- Output: `keyboard_heatmap_qwerty.png`, `keyboard_letter_counts.csv` (inkl. normierter Counts & Koordinaten) und `unmapped_characters.txt`.

### Zwei Texte vergleichen (divergierende Heatmap)

```pwsh
python gadsby_heatmap.py --input "text_a.txt" --compare-with "text_b.txt" --output-dir output_compare --cmap coolwarm --scale-type diverging
```

- Ergebnis ist eine divergierende Heatmap mit farbiger Legende: Mittelwert = gleich häufig, linke Skala = Text A seltener, rechte Skala = Text A häufiger (relativ zu Text B).
- Es werden zwei CSV-Dateien erzeugt (`keyboard_letter_counts.csv` für Text A und `keyboard_letter_counts_compare.csv` für Text B).

## Hinweise zur Bewertung

- Nachvollziehbarkeit/Reproduzierbarkeit, Designbegründung (Farbskalen, Legende), Barrierefreiheit, Qualität der Diskussion und Reflexion.
