# DICOM-Daten des Knee-Phantoms · eine Schichtebene

Dieser Ordner enthält 10 DICOM-Bilder des Knee-Phantoms (Untersuchung `KneePhantomKostia`, 05.11.2026, 1,5 T) auf derselben geometrischen Ebene. Es ist die dritte von fünf Schichten der FFE-Aufnahmen (Schichtposition 11,8 mm), die Schicht mit dem stärksten Signal und dem vollständigen Querschnitt. Die Dateien sind nach Aufnahme, Echonummer und Bildtyp benannt. Die DICOM-Inhalte und Metadaten wurden beim Umbenennen nicht verändert.

## Dateinamen lesen

- `knee_dual_echo1_magnitude.dcm`: Dual-Echo-Aufnahme, erstes Echo (6,9 ms), Magnitude.
- `knee_dual_echo2_phase.dcm`: Dual-Echo-Aufnahme, zweites Echo (13,8 ms), direkte Phase.
- `knee_triple_echo3_magnitude.dcm`: Triple-Echo-Aufnahme, drittes Echo (23,0 ms), Magnitude.

`echo1`, `echo2` und `echo3` zählen die Echos nach aufsteigender tatsächlicher TE innerhalb der jeweiligen Aufnahme. Eine Echonummer allein legt IP oder OP nicht fest. Diese Zuordnung wird anhand von TE und Wasser-Fett-Frequenzabstand geprüft.

| Aufnahme | Echos | TE [ms] | Bildtypen | Dateien |
| --- | --- | --- | --- | ---: |
| Knee-Phantom · Dual-Echo | 1–2 | 6,9 / 13,8 | Magnitude und Phase | 4 |
| Knee-Phantom · Triple-Echo | 1–3 | 9,2 / 16,1 / 23,0 | Magnitude und Phase | 6 |

Alle Bilder haben 864 × 864 Pixel bei 0,266 mm Pixelabstand und 10 mm Schichtdicke. Die Echozeiten sind dieselben wie bei den Flaschen-Beispieldaten in `../beispiel/`.

## Im Notebook verwenden

Setzen Sie in der Ladezelle von `experiment.ipynb` `DATENORDNER = "daten/knee"` und `PRAEFIX = "knee"`. Das Notebook lädt dann die vier Dual-Echo- und die sechs Triple-Echo-Bilder über ihre festen Dateinamen.

Der Datensatz enthält ausschließlich Magnituden und direkte Phasen der Dual- und Triple-Echo-Aufnahmen. Die im Export ebenfalls vorhandenen Einzelaufnahmen `T1W_FFE IP` und `T1W_FFE OP` stammen aus getrennten Akquisitionen und sind deshalb nicht enthalten. Beim Knee-Phantom ist das späte Echo durch T₂*-Zerfall fast überall dunkler als das frühe; die Kontrolle meldet deshalb für viele Pixel eine Modellverletzung.

## Ursprüngliche Dateien zuordnen

[manifest.csv](manifest.csv) enthält für jedes Bild den aktuellen Dateinamen (`datei`), den ursprünglichen Exportnamen (`original_datei`) aus dem Classic-DICOM-Export, die Aufnahme, die Bildkomponente, die tatsächliche TE und die Schichtposition. Die Komponentenkürzel bedeuten `M` = Magnitude und `P` = Phase.
