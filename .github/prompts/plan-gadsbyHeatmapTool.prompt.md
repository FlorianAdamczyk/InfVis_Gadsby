Zielbild

- Input: beliebiger Text (z. B. dein Gadsby‑Ausschnitt) aus Datei oder String, plus Optionen (Layout, Farbskala, Normalisierung, Ausgabeformat).
- Output: PNG/SVG einer QWERTY‑Tastatur mit Heatmap‑Überlagerung, plus optional alternative Diagramme (Balkendiagramm, Small Multiples, andere Farbskalen).

1) Daten- und Layout-Grundlage

- Keyboard-Modell:
  - Definiere in Python eine Datenstruktur für Tasten mit Position und Label, z. B. ein Dict `key -> (row, col, width)`.
  - QWERTY-Layout in drei/fünf Reihen: `["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]`, Sondertasten (Space, Enter) optional.
  - Aus dieser Struktur berechnest du Koordinaten (x, y, Breite, Höhe) für Matplotlib‑Patches; so kannst du später leicht andere Layouts (z. B. deutsches QWERTZ) ergänzen.

- Text-Vorverarbeitung und Zählung:
  - Funktion, die Text einliest, normalisiert (wahlweise: alles zu Groß- oder Kleinbuchstaben), nicht‑alphabetische Zeichen optional entfernt oder getrennt zählt (Space, Punkt).
  - Ausgabe: ein `Counter` oder Dict `letter -> count`.
  - Optional: Normalisierung auf relative Häufigkeiten (Anteil) oder pro 1.000 Zeichen.

2) Kern-Heatmap auf QWERTY-Tastatur

- Mapping Text → Keyboard:
  - Mappe jeden Buchstaben auf die passende Taste (z. B. `e` → `E`‑Taste).
  - Umgang mit unbekannten Zeichen planen
  -   Unmapped Characters nicht einfach still ignorieren, sondern eine Liste/Statistik führen: welche Zeichen kamen vor, haben aber keinen Eintrag im Layout.
Optional im Batch-Output (z.B. als Textdatei oder Konsole) ausgeben, um im Bericht/Reflexion diskutieren zu können.

- Visualisierung mit Matplotlib:
  - Erzeuge eine Figur mit fixem Seitenverhältnis (z. B. 16:9), Achsen aus.
  - Für jede Taste zeichnest du ein Rechteck (`Rectangle`‑Patch) an der berechneten Position.
  - Färbung: benutze eine sequentielle Farbskala (z. B. `viridis`, `magma`, `plasma`, `cividis` – letztere farbfehlsichtrobust) über `Normalize(vmin=0, vmax=max_count)` oder quantile‑basiert.
  - Beschriftung der Tasten mit dem Buchstaben, optional Frequenz (z. B. als kleine Zahl oder im Tooltip, falls interaktiv).

- Konfigurierbarkeit (wichtig für Aufgabe b/d):
  - Parameter in der Hauptfunktion:
    - `cmap` (Farbskala, sequentiell vs. divergend),
    - `normalize` (z. B. `"absolute"`, `"relative"`, `"zscore"`),
    - `log_scale` (für sehr ungleich verteilte Häufigkeiten),
    - `show_legend` (Farblegende mit Skala und Einheit),
    - `include_non_letters` (Zählen von Space, Punkt etc.),
    - `background_style` (`"plain"`, `"custom_image"` – wenn du später ein Bild als Keyboard-Hintergrund nimmst).
  - So kannst du später leicht Varianten ausprobieren und für deine Folien nebeneinanderstellen.

3) Umgang mit „Keyboard-Background“

- Variante A – rein programmatisch (empfohlen):
  - Nutze nur Rechtecke und Text in Matplotlib. Vorteil: perfekte Alignment‑Kontrolle, kein Frickeln mit Pixel‑Offsets.
  - Du kannst das Keyboard dezent grau zeichnen und die Heatmap darüberlegen (Alpha‑Wert < 1) oder direkt die Tasten einfärben.


4) Alternative Visualisierungen (für die Aufgaben b/d)

Zusätzlich zur Keyboard‑Heatmap kannst du mit denselben Daten weitere Views erzeugen:

- Balkendiagramm Buchstabenhäufigkeiten:
  - Sortiertes Bar‑Chart (`plt.bar`) der wichtigsten 10–15 Buchstaben.
  - Farbskala identisch zur Heatmap (z. B. gleiche `cmap` basierend auf Frequenz), um die Verknüpfung hervorzuheben.
- Vergleich verschiedener Texte (Small Multiples):
  - Option, mehrere Texte (z. B. Gadsby vs. normaler englischer Text) einzulesen und:
    - ein differenzielles Layout (Heatmap der Differenz, mit divergierender Skala).
- Tabellarische Ausgabe oder CSV:
  - Exportiere `letter -> relative frequency` als CSV, um ggf. in anderen Tools (Excel, Power BI) weitere Diagramme zu bauen.

5) API-/Skript-Design in Python

Strukturvorschlag im Projektordner:

- `keyboard_heatmap/`
  - `__init__.py`
  - `layout.py` – Definition von QWERTY (später erweiterbar).
  - `counts.py` – Funktionen für Textverarbeitung und Frequenzberechnung.
  - `plot_keyboard.py` – Matplotlib‑Code für Keyboard‑Heatmap.
  - `plot_alternatives.py` – Bar‑Charts, Small Multiples.
- `gadsby_heatmap.py` – kleines CLI-Skript, das:
  - `Gadsby_ Ernest Vincent Wright_1939.txt` einliest,
  - ggf. nur einen Ausschnitt nimmt (z. B. die ersten 10.000 Zeichen),
  - Heatmap + Alternativen rendert (z. B. `output/keyboard_heatmap_gadsby.png`, `output/letter_bars_gadsby.png`).
- `requirements.txt` – mindestens `matplotlib`, optional `pandas`, `numpy`.

CLI‑Beispiel:

```bash
python gadsby_heatmap.py --input "Gadsby_ Ernest Vincent Wright_1939.txt" ^
    --output-dir output ^
    --layout qwerty ^
    --cmap cividis ^
    --normalize relative
```

6) Konkrete nächste Schritte (Umsetzungsvorschlag)

1. Ein kleines Python‑Modul `keyboard_heatmap` mit oben genannter Struktur anlegen.
2. Die QWERTY‑Layout‑Definition und eine robuste Zählfunktion implementieren.
3. Die Matplotlib‑Keyboard‑Heatmap schreiben und eine erste Version für Gadsby in `gadsby_heatmap.py` bauen.
4. Danach ergänzen wir auf Wunsch die alternativen Darstellungen (Balkendiagramm, Vergleichs‑Heatmaps).
