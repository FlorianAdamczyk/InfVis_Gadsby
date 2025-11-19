# Übungen Datenvisualisierung (WS 2025/26)

V1.1: 2025-11-12  
Änderungen/Anpassungen an Vorlesungsfolien in Gelb markiert

## 1) Überblick & Ziele
Sie üben, Verzerrungen in Diagrammen systematisch zu erkennen und zu vermeiden – etwa durch den korrekten Umgang mit Lie-Factor, Data-Ink und dem bewussten Einsatz bzw. Verzicht auf „Chartjunk“. Auf der Basis von Wahrnehmungsgrundlagen, präattentiven Merkmalen und Gestaltprinzipien treffen Sie fundierte Designentscheidungen. Sie wählen Farben zielgerichtet aus (sequentielle, divergierende und bivariate Skalen) und achten dabei konsequent auf Barrierefreiheit und ausreichende Kontraste. Darüber hinaus gestalten und vergleichen Sie Darstellungen für Netzwerke, Hierarchien und Zeitreihen und setzen Interaktion stets aufgabengerecht ein. Begleitend planen Sie Mini-Evaluationen – von Hypothesen über Studiendesigns bis hin zu geeigneten Metriken – und berichten Ergebnisse klar und kompakt. Alle Abgaben sind reproduzierbar angelegt: Daten und Code werden nachvollziehbar organisiert und in eine professionelle Präsentationsform überführt.

## 2) Organisatorisches
- Teilnehmende: alle, die eine Prüfungsleistung abgeben wollen
- Gruppenarbeit: Einzelarbeit oder 2er-Teams, freie Wahl. Teambildung selbstorganisiert; Mitglieder in der Abgabe kenntlich machen.
- Präsentationsdauer: Kurzvorstellung 5–10 Minuten, wenn Sie das selber vorstellen. Als Richtwert. Ebenfalls für hochgeladene Videos.
- Werkzeuge: frei wählbar, z. B. Excel, Python/Matplotlib/Altair, R/ggplot2, Observable/D3, Power BI, Tableau, …
- Prüfungsvorleistung: Die erfolgreiche Abgabe einer Übungsaufgabe - entweder Übung A oder eine der Aufgaben aus Übung B (ggf. mit kurzer Präsentation vgl. Modalitäten aus der Vorlesung) ist notwendig.

## 3) Abgabeformate & Benennung
a) Email mit Subject: „DV25 Übung“ oder „Übung InfoVis 2025-26“  
im Text der E-Mail: Name und Matrikelnummer (maximal 2er Teams)  
Downloadlink (z. B. JLUbox/Hessenbox) für eine Datei im MP4 Format: „InfoVis_Üxx_Initialen.mp4“  
bevorzugt: .mp4 / H.264 / AAC

b) Präsentationsfolien: pptx (empfohlen) oder PDF (Formatempfehlung: 16:9).

c) Dateiname: dv25_uXX_nachname_nachname_kurztitel.pdf  
(z. B. dv25_u02_mueller-meier_heatmap.pdf)

## 4) Barrierefreiheit & Ethik
- Verwenden Sie geeignete Farbpaletten (z. B. sequentiell/divergierend, bivariate) und prüfen Sie Kontraste. Bieten Sie – wo sinnvoll – eine farbfehlsichtrobuste Variante an.
- Datenquellen sauber zitieren (Autor/Institution, Jahr, Link/DOI, Lizenz). Keine personenbezogenen Daten ohne Rechtsgrundlage; Anonymisierung prüfen

---

# Übung B — Übungsaufgaben

### Hinweise zum Vorstellen der Übungsaufgaben
- Problem & Aufgabe (1 Folie) — Was ist das Ziel der Aufgabe
- Daten & Kodierungen (1 Folie)
- Designentscheidungen z. B. Layout, Farben, Interaktion, Alternativen
- Ergebnis & Fazit (1 Folie)
- Reflexion (optional): Grenzen, nächster Schritt

## Aufgabe 5 — Heatmaps
**Ziel & Kontext:** Machen Sie sich mit Heatmaps vertraut. Erinnern Sie sich an die Grundidee (oder recherchieren Sie kurz im Internet), wofür Heatmaps geeignet sind und wann nicht. Anschließend wenden Sie eine bestehende Keyboard-Heatmap exemplarisch an.

a) **Definition & Dateneignung:** Was wird mit einer Heatmap dargestellt? Welche Eigenschaften sollte die Datenbasis haben (z. B. Metrik vs. Kategorien, Auflösung/Binning, Skala, Ausreißer, Nullpunkt/Center)?

b) **Beispiele beurteilen:** Suchen Sie ein geeignetes und ein ungeeignetes Beispiel für Heatmaps. Begründen Sie Ihre Einschätzung (Aufgabe, Lesbarkeit, Farbskala, Legende, Aggregation, Alternativen).

Unter [1] finden Sie eine Visualisierung auf Basis von Heatmaps: Es wird die Häufigkeit der Tastennutzung auf einer Standard-QWERTY-Tastatur für beliebige Texte visualisiert.

c) **Anwendung:** Erstellen Sie einen Beispieltext auf Deutsch oder Englisch mit mindestens 100 Wörtern (darf aus anderen Quellen kopiert werden – bitte mit Quellenangabe). Wenden Sie ihn auf die Visualisierung an [1] an und speichern Sie das entstandene Bild.

d) **Diskussion:** Diskutieren Sie die Visualisierung. Was leiten Sie ab? Gehen Sie auch auf die Wichtigkeit verschiedener Buchstaben ein (z. B. im Vergleich zu anderen Kodierungen/Alphabeten wie dem Morsealphabet).

**Material:**  
[1] Keyboard-Heatmap (Patrick Wied): https://www.patrick-wied.at/projects/heatmap-keyboard/

**Hinweise:**
- Belege/Quellen bitte angeben (Beispiele, Textquelle, Tools).
- Sprechen Sie Farbskala & Legende an (z. B. sequentiell vs. divergend, Center/Nullpunkt).
- Reflektieren Sie Alternativen (z. B. Barcharts, Small Multiples), falls Heatmaps ungeeignet erscheinen.