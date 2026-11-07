# Jupyter-Notebook zum MRT-Praktikum

Sie werten die Dual-Echo- und die Triple-Echo-Aufnahme einer Wasser-/Ölflasche auf einer Schichtebene aus. Laden, Prüfen und Anzeigen der Bilder sind vollständig vorbereitet. **Sie programmieren nur die Formeln** in fünf Aufgaben:

1. Die Phasenverschiebung von Fett gegenüber Wasser in Grad aus Echozeit und Wasser-Fett-Frequenzabstand.
2. Die relative Phase zwischen OP- und IP-Echo.
3. Das Farbbild: **Phase als Farbe, Magnitude als Helligkeit**.
4. Den größeren Modellanteil A, den kleineren Modellanteil B und den Signalanteil B **für jedes gültige Pixel**.
5. Eine **B₀-Frequenzkarte in Hz** aus der Phasendifferenz zwischen Echo 1 und Echo 3 der Triple-Echo-Aufnahme.

## Vorbereitung

Öffnen Sie [`experiment.ipynb`](experiment.ipynb) im Ordner `notebook/` mit einem Python-3-Kernel. Speichern Sie eine eigene Kopie **im selben Ordner**, beispielsweise `experiment_bearbeitet.ipynb`.

Ein Git-Klon enthält die Dateien, installiert aber noch keine Bibliotheken. Führen Sie bei Bedarf die erste Notebook-Zelle aus:

```python
%pip install -r requirements-jupyterhub.txt
```

Starten Sie danach den Kernel neu und führen Sie die Importzelle aus. Wenn das JupyterHub-Profil mit dem [Dockerfile dieses Repositorys](../Dockerfile) gebaut wurde, sind die Bibliotheken bereits vorhanden; wählen Sie dann **Python 3 (MRT-Praktikum)**. Hinweise zum lokalen Container stehen in der [Repository-README](../README.md#how-to-run-the-coding-exercises-locally).

## Aufgaben bearbeiten

Arbeiten Sie von oben nach unten mit **Shift + Enter**. In den Aufgabenzellen ersetzen Sie jedes `...` durch Ihre Formel; die Formel und kurze Python-Hilfen stehen direkt darüber. Alle anderen Zellen sind fertig und müssen nur ausgeführt werden.

Mit Ihren Phasenverschiebungen aus Aufgabe 1 ordnet eine vorbereitete Zelle zu, welches Echo IP (Restwinkel nach vollen 360°-Runden nahe 0°) und welches OP (nahe 180°) ist. Alle Größen in den Codezellen sind mit ihrer Einheit kommentiert. Nach Aufgabe 4 prüft eine Kontrollzelle Ihre Formeln. Für Kurzantworten doppelklicken Sie auf die Textzelle und schließen sie mit **Shift + Enter** ab. Speichern Sie regelmäßig mit **Strg + S / ⌘ + S**.

## Daten mit festen Dateinamen

Das Notebook lädt die Bilder ohne Auswahlfelder über feste Dateinamen. In der Ladezelle stehen nur der Datenordner und ein Präfix:

```python
DATENORDNER = "daten/beispiel"
PRAEFIX = "wasser_oel"
```

Daraus ergeben sich die zehn Dateinamen `<PRAEFIX>_dual_echo1_magnitude.dcm`, `<PRAEFIX>_dual_echo1_phase.dcm`, `<PRAEFIX>_dual_echo2_…` sowie `<PRAEFIX>_triple_echo1_…` bis `<PRAEFIX>_triple_echo3_phase.dcm`. Die Echos sind nach aufsteigender Echozeit nummeriert. Die Hilfsdatei prüft, dass Magnitude und Phase zusammenpassen und alle Echos aus derselben Aufnahme und Schichtebene stammen.

| Datensatz | `DATENORDNER` | `PRAEFIX` |
| --- | --- | --- |
| Wasser-/Ölflasche (Voreinstellung) | `daten/beispiel` | `wasser_oel` |
| Wasser-/Ölflasche mit Metallknopf | `daten/beispiel` | `wasser_oel_mit_knopf` |
| Knee-Phantom | `daten/knee` | `knee` |
| Eigene Messdaten | `daten/eigene` | `eigene` |

## Eigene Daten

Benötigt werden nur **Einzelbilder einer Schicht**: die Bilder der Dual-Echo- und der Triple-Echo-Aufnahme, jeweils Magnitude und Phase je Echo, also zehn Bilddateien. Laden Sie die DICOM-Dateien in `daten/eigene/` hoch und führen Sie in einer neuen Notebook-Zelle `mh.dateiliste("daten/eigene")` aus. Die Liste zeigt für jede Datei Aufnahme, Bildtyp, Echozeit und Schichtposition. Benennen Sie die zehn Dateien Ihrer gewählten Schicht nach dem obigen Schema mit dem Präfix `eigene` um. Setzen Sie dann `DATENORDNER = "daten/eigene"` und `PRAEFIX = "eigene"` und führen Sie alle Zellen erneut aus. Setzen Sie in Aufgabe 1 Ihren im Spektrum gemessenen Frequenzabstand ein.

## Bilder richtig lesen

IP enthält Wasser- **und** Fettsignal. Rot und Blau zeigen ausschließlich die gemessene OP-/IP-Phasendifferenz: nahe 0 wird blau, nahe ±π rot. Eine feste Zuordnung „Rot = Öl, Blau = Wasser“ wird nicht vorgenommen.

Die Signalanteile werden unabhängig von den Farben aus beiden Magnituden berechnet: A ist im idealen Modell der größere, B der kleinere Beitrag. A und B können ohne zusätzliches Wissen nicht eindeutig Wasser und Fett zugeordnet werden; die Prozentwerte sind keine Stoffkonzentrationen.

Für die B₀-Karte sollte die chemische Phasendifferenz der äußeren Triple-Echos ungefähr null modulo 2π sein. Die Karte zeigt die ganze Schicht ohne Maske und ohne räumliches Entfalten; die Werte sind nur modulo 1/ΔTE bestimmt.

## Abgabe und Musterlösung

Speichern Sie Ihr Notebook mit allen Abbildungen und Ihren drei Kurzantworten und geben Sie das gespeicherte Notebook ab.

[`experiment_loesung.ipynb`](experiment_loesung.ipynb) enthält die vollständige Musterlösung mit zusätzlichen Codekommentaren. Sie wurde mit den Beispieldaten der Wasser-/Ölflasche unter Python 3.12 fehlerfrei ausgeführt; alle Ergebnisse und Abbildungen sind gespeichert.

## Bei Fehlern

Prüfen Sie zuerst, ob alle vorherigen Zellen ausgeführt und alle `...` in der aktuellen Aufgabenzelle ersetzt wurden. Bei „Datei nicht gefunden“ kontrollieren Sie `DATENORDNER`, `PRAEFIX` und die Dateinamen; Notebook, `mrt_hilfen.py` und der Ordner `daten/` müssen zusammen im Ordner `notebook/` liegen. Zeigen Sie bei weiteren Problemen die vollständige Fehlermeldung.
