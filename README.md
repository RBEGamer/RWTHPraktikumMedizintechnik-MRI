# Medizintechnik-Praktikum · Magnetresonanztomographie

Dieses Repository enthält die Unterlagen zum Versuch **Magnetresonanztomographie (MRT)** im Medizintechnik-Praktikum. Dazu gehören das Versuchsskript, eine bebilderte Scan-Anleitung, die vorbereitete Philips-ExamCard und ein Jupyter-Notebook mit DICOM-Beispieldaten zur Auswertung.

## Unterlagen

| Unterlage | Inhalt |
| --- | --- |
| [Versuchsskript](<dokumentation/Versuchsskript Bildgebende Verfahren - Magnetresonanztomographie.pdf>) | Grundlagen und Aufgaben zum Versuch Magnetresonanztomographie. |
| [Scan-Anleitung (PDF)](dokumentation/MRT_Scananleitung/scan_anleitung.pdf) | Versuchsaufbau, Bedienung des Scanners, Messablauf und DICOM-Export. Die [LaTeX-Quelle](dokumentation/MRT_Scananleitung/scan_anleitung.tex) liegt im selben Ordner. |
| [Philips-ExamCard](dokumentation/philips_ambition_ExamCard/LfB_MR_Praktikum.ExamCard) | Vorbereitete Messsequenzen für das MRT-Praktikum. |
| [Jupyter-Notebook](notebook/experiment.ipynb) | Aufgaben zur einfachen Dixon-Auswertung und zur optionalen näherungsweisen B₀-Karte. |
| [DICOM-Beispieldaten](notebook/daten/beispiel/README.md) | Magnituden- und Phasenbilder einer gemeinsamen Schichtebene, jeweils mit und ohne Metallknopf. |

## Versuch und Auswertung

Im Praktikum untersuchen Sie unter anderem eine mit Wasser und Öl gefüllte Flasche. Sie planen die Aufnahmen, untersuchen den Einfluss von Messparametern und bestimmen den Frequenzabstand zwischen Wasser und Fett. Anschließend vergleichen Sie die Echos und werten die Wasser- und Ölbereiche im Notebook aus. Eine optionale Zusatzaufgabe behandelt die lokale Magnetfeldabweichung B₀.

## Einstieg

1. Lesen Sie das Versuchsskript zur Vorbereitung.
2. Verwenden Sie die Scan-Anleitung für die Durchführung der Messungen mit der Betreuung.
3. Öffnen Sie zur Auswertung das Jupyter-Notebook. Die [Startanleitung zum Notebook](notebook/README.md) erklärt die Bedienung und die Verwendung eigener Messdaten.

Die benötigten Python-Pakete sind in [notebook/requirements.txt](notebook/requirements.txt) aufgeführt. Das Notebook benötigt die Hilfsdatei `mrt_hilfen.py` und den Unterordner `daten` neben sich; behalten Sie diese Ordnerstruktur beim Kopieren bei.
