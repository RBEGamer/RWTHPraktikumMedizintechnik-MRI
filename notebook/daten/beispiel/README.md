# DICOM-Beispieldaten · eine Schichtebene

Dieser Ordner enthält 20 DICOM-Bilder der Wasser-/Ölflasche auf derselben geometrischen Ebene. Die Dateien sind nach Objektzustand, Aufnahme, Echonummer und Bildtyp benannt. Die DICOM-Inhalte und Metadaten wurden beim Umbenennen nicht verändert.

## Dateinamen lesen

- `wasser_oel_dual_echo1_magnitude.dcm`: Wasser-/Ölflasche ohne Knopf, Dual-Echo-Aufnahme, erstes Echo, Magnitude.
- `wasser_oel_triple_echo3_phase.dcm`: dieselbe Objektvariante, Triple-Echo-Aufnahme, drittes Echo, direkte Phase.
- `wasser_oel_mit_knopf_dual_echo2_magnitude.dcm`: Wasser-/Ölflasche mit Metallknopf, Dual-Echo-Aufnahme, zweites Echo, Magnitude.

`echo1`, `echo2` und `echo3` zählen die Echos nach aufsteigender tatsächlicher TE innerhalb der jeweiligen Aufnahme. Eine Echonummer allein legt IP oder OP nicht fest. Diese Zuordnung wird anhand von TE und Wasser-Fett-Frequenzabstand geprüft.

| Aufnahme | Echos | Bildtypen | Dateien |
| --- | --- | --- | ---: |
| Wasser/Öl · Dual-Echo | 1–2 | Magnitude und Phase | 4 |
| Wasser/Öl · Triple-Echo | 1–3 | Magnitude und Phase | 6 |
| Wasser/Öl mit Knopf · Dual-Echo | 1–2 | Magnitude und Phase | 4 |
| Wasser/Öl mit Knopf · Triple-Echo | 1–3 | Magnitude und Phase | 6 |

## Im Notebook verwenden

Das Notebook lädt die Bilder über feste Dateinamen. Voreingestellt sind `DATENORDNER = "daten/beispiel"` und `PRAEFIX = "wasser_oel"`; für die Flasche mit Metallknopf setzen Sie `PRAEFIX = "wasser_oel_mit_knopf"`. Pro Variante werden die vier Dual-Echo- und die sechs Triple-Echo-Bilder geladen.

Die Wasser-/Öl-Zuordnung erfolgt anhand der bekannten Befüllung und dokumentierten Lagerung, bei den Beispieldaten oben Öl und unten Wasser. Die Bildhelligkeit allein legt diese Zuordnung nicht fest; auch die neutrale Farbansicht ist keine Stoffkennzeichnung.

## Ursprüngliche Dateien zuordnen

[manifest.csv](manifest.csv) enthält für jedes Bild den aktuellen Dateinamen (`datei`), den ursprünglichen Exportnamen (`original_datei`), die Aufnahme, die Bildkomponente, die tatsächliche TE und die Schichtposition. Die Komponentenkürzel bedeuten `M` = Magnitude und `P` = Phase.

Eigene Exporte gehören in den benachbarten Ordner `../eigene/` und werden dort nach demselben Schema mit dem Präfix `eigene` benannt.
