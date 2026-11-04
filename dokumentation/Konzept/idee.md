# Idee: Jupyter-Notebook zu Experiment 3 des MRT-Praktikums

**Nachtrag 04.11.2026 – Phantom und ROI-Zuordnung:** Die Befüllung wurde als Wasserflasche mit Öl und Wasser präzisiert. Der erneute Vergleich aller neun Classic-Ebenen bestätigt, dass die mittlere Ebene (IP `IM_0090`, OP `IM_0089`) die Trennung zeigt. Die Scanner-Wasser-/Fettbilder `IM_0005`/`IM_0032` derselben Ebene unterstützen die Zuordnung qualitativ; sie stammen aus einer anderen Akquisition. Im dargestellten Bild liegt der ölreiche Bereich oben, der wasserreiche unten. Die Notebooks verwenden nun getrennte Wasser- und Öl-ROIs (Zeilen/Spalten: 350:410 / 310:360 bzw. 100:160 / 120:170). Die zuvor zentrale ROI 180:280 / 210:290 liegt im Übergangsbereich und wird nicht pauschal als wasserdominant behandelt. Die bekannte Befüllung erlaubt eine lokale Zuordnung der größeren/kleineren Modellanteile; exakte Mischungs-, Volumen- oder PDFF-Werte folgen daraus nicht. Alle Auswertungen bleiben auf **einer Schichtebene**. Der folgende Konzepttext dokumentiert den ursprünglichen Planungsstand; dieser Nachtrag präzisiert die Phantomkenntnis und die inzwischen umgesetzte ROI-Wahl.

Stand: 03.11.2026. Zielgruppe: Studierende im 3. Semester mit wenig oder keiner Python-Erfahrung.

Dieses Dokument beschreibt das Konzept und die nächsten Umsetzungsschritte. Das Notebook wird anschließend auf dieser Grundlage erstellt. Die DICOM-Struktur und ausgewählte Bilder wurden bereits untersucht; eine vollständige Dixon- oder B₀-Rekonstruktion der Messdaten ist noch nicht validiert.

Festlegung: Die B₀-Zusatzaufgabe verwendet direkt exportierte **Phasenbilder**, keine Re/Im-Rekonstruktion. Sie soll mit den durch die Scanner-Software erreichbaren Echozeiten eine **näherungsweise** Feld- und Homogenitätsdarstellung liefern. Ein exakt realisiertes 2π-/4π-Paar ist keine Voraussetzung. **Die Studierenden lesen die tatsächlichen Echozeiten aus ihren DICOM-Metadaten aus und berechnen daraus den Zeitabstand; im Auswertecode stehen keine fest eingetragenen Echozeiten.** Magnitudenbilder bleiben für die Dixon-Pflichtaufgabe und gegebenenfalls für die Signalmaske der B₀-Auswertung erhalten.

Festlegung zum Aufbau: **Der erste praktische Schritt ist das Laden einer DICOM-Datei. Danach folgt durchgehend: kurze Erklärung → eine oder zwei Codezeilen → nächste Teilaufgabe.** Python-Grundlagen werden direkt bei ihrer ersten Verwendung erklärt.

Festlegung zum Zeitrahmen: **Insgesamt 120 Minuten für die Notebook-Bearbeitung einschließlich der optionalen B₀-Aufgabe: 80 Minuten Pflichtteil, 30 Minuten B₀ beziehungsweise Vertiefung und 10 Minuten für Abschluss, Speichern und Puffer.** Die Auswerteumgebung und DICOM-Exporte stehen zu Beginn bereit.

## 1. Grundidee und Lernziele

Die Studierenden entwickeln die Auswertung einer selbst aufgenommenen MRT-Schicht Schritt für Schritt: Datei öffnen, Bild anzeigen, Bildwerte verrechnen, einen Bildbereich auswählen und das Ergebnis physikalisch erklären. Zuerst üben sie an den vorhandenen Beispieldaten. Anschließend verwenden sie denselben Ablauf mit ihren eigenen DICOM-Exporten.

Experiment 3 bleibt die einfache Fett-Wasser-Trennung. Die B₀-Karte wird als klar gekennzeichnete Zusatzaufgabe angeboten. DICOM-Sonderfälle und Phase-Unwrapping werden durch bereitgestellte Funktionen behandelt, damit die Studierenden sich auf Bilddaten, Rechenschritte und Interpretation konzentrieren können.

Am Ende sollen die Studierenden:

1. Markdown- und Codezellen unterscheiden und ein Notebook von oben nach unten ausführen können.
2. Variablen, einfache Rechnungen, Arrays, Bildindizes und eine einfache Maske verwenden können.
3. Magnitude, Phase, Echozeit und Schichtposition in einer vorbereiteten DICOM-Übersicht erkennen.
4. Passende In-Phase- und Out-of-Phase-Bilder derselben Schicht auswählen.
5. Eine einfache Dixon-Auswertung durchführen und deren Voraussetzungen benennen.
6. Einen näherungsweisen Fett-Signalanteil in einer ROI berechnen und seine Grenzen erklären.
7. Optional aus zwei geeigneten Phasenbildern eine Karte der lokalen Feldabweichung in ppm bestimmen.

## 2. Was Experiment 3 im Skript verlangt

Grundlage sind das 14-seitige „Versuchsskript Bildgebende Verfahren - Magnetresonanztomographie (MRT).pdf“, besonders Abschnitte 3.1 bis 3.5 auf PDF-Seiten 8 bis 11 und „Experiment 3: Bildakquisition & Rekonstruktion“ auf PDF-Seite 14. Die zweite PDF „Bildgebende Verfahren - Magnetresonanztomographie (MRT).pdf“ enthält denselben extrahierten Text. Die vorhandenen Notebooks unter `notebook_tasks_student` behandeln andere Bildverarbeitungsaufgaben; sie sind noch keine MRT-Auswertung.

| Vorgabe in Experiment 3 | Umsetzung im Notebook |
| --- | --- |
| Magnitudenbilder bei In-Phase- und Out-of-Phase-Echozeiten aufnehmen | Messprotokoll übernehmen und tatsächliche Echozeiten aus dem Export anzeigen |
| DICOM-Bilder auf den Auswerte-PC exportieren | Vorbereiteter Ordnerimport mit übersichtlicher Auswahl von Aufnahme, Bildtyp und Schicht |
| Addition und Subtraktion selbst implementieren | An den bereits geladenen Bildern jeweils eine Rechenzeile ergänzen; bei Bedarf ein kurzes Zahlenbeispiel direkt daneben erläutern |
| Näherungsweisen Fettgehalt berechnen | ROI auswählen, Signalanteil berechnen, mit Annahmen und Einheit dokumentieren |
| Randartefakte und Water-Fat-Swaps diskutieren | Vergleichsbilder, Ausschnittvergrößerung und kurze Antwortfelder |

### Fachliche Präzisierungen für die Aufgabenstellung

**Magnitude allein erlaubt keine allgemeine Wasser-Fett-Zuordnung.** Im idealisierten Modell gilt für nichtnegative Signalanteile:

$$
M_{\mathrm{IP}}=W+F,\qquad M_{\mathrm{OP}}=|W-F|.
$$

Daraus erhält man zunächst nur den größeren und den kleineren Anteil:

$$
A=\frac{M_{\mathrm{IP}}+M_{\mathrm{OP}}}{2}=\max(W,F),\qquad
B=\frac{M_{\mathrm{IP}}-M_{\mathrm{OP}}}{2}=\min(W,F).
$$

Nur unter der zusätzlichen Annahme $W\geq F$ darf man $A$ als Wasser und $B$ als Fett bezeichnen. Diese Annahme wird in der Vorbereitungsaufgabe auf Seite 14 bereits genannt und muss auch im Notebook sichtbar bleiben. Zwei Beispiele mit $W=80,F=20$ und $W=20,F=80$ ergeben jeweils $M_{\mathrm{IP}}=100$ und $M_{\mathrm{OP}}=60$. Auch reines Wasser und reines Fett gleicher Signalstärke sind anhand dieser beiden Magnituden nicht unterscheidbar.

Deshalb zunächst `anteil_gross` und `anteil_klein` berechnen. Die Zuordnung zu Wasser/Fett erfolgt für die Basisaufgabe unter expliziter Annahme beziehungsweise anhand dokumentierter Phantom-Inhalte. Bei unbekannter Zusammensetzung bleibt die Zuordnung offen. Eine zuverlässige allgemeine Trennung erfordert zusätzliche Information oder eine weitergehende Rekonstruktion; eine B₀-Karte allein löst nicht alle Zuordnungsprobleme.

Weitere Punkte:

- Im komplexen Dixon-Modell werden komplexe Signale addiert/subtrahiert und erst danach Beträge gebildet. Das ist nicht dasselbe wie die Rechnung mit zwei Magnitudenbildern.
- Ein gemeinsamer Hintergrundphasenfaktor verändert für sich allein die Magnitude nicht. Die fehlende Wasser-Fett-Zuordnung darf daher nicht allein mit B₀-Inhomogenität erklärt werden. Innerhalb eines Pixels auftretende Dephasierung und Signalverluste sind zusätzliche Effekte.
- Das Ergebnis $F/(W+F)$ ist hier ein **Fett-Signalanteil**, keine validierte Proton-Density Fat Fraction und kein unmittelbar gemessener Fett-Volumenanteil. Bei den verwendeten Gradientenechos ist insbesondere T₂*- statt nur T₂-Abfall relevant; außerdem werden unter anderem T₁-Gewichtung, das Mehrpeak-Fettspektrum und Rauschen vereinfacht.
- Die Halbierung der Phasendifferenz in Abschnitt 3.5 beschreibt bei entsprechendem Echozeit-Schema eine Phasenentwicklung pro halbem Zeitabstand. Für B₀ wird immer die gesamte Phasendifferenz durch den zugehörigen gesamten Echozeitabstand geteilt. Der Faktor $1/2$ darf nicht zusätzlich in die allgemeine Feldkartenformel übernommen werden.

## 3. Befund der vorhandenen DICOM-Daten

### 3.1 Phasenbilder und Real-/Imaginärteile

Geprüft wurden alle 401 DICOM-Objekte der drei Exportordner, ohne `DICOMDIR`. Davon enthalten 347 Bildpixel. Bei Enhanced MR wurden zusätzlich die einzelnen Frames und ihre Metadaten ausgewertet. Classic und Enhanced sind zwei Exportformen derselben September-Aufnahmen und werden nicht als unabhängige Messwiederholungen gezählt.

| Ordner | Tatsächlicher Inhalt | Folgerung |
| --- | --- | --- |
| `20260917 MR Praktikum Test/Dicom Classic/DICOM` | 333 Bilddateien, darunter 108 separate Phasenbilder; außerdem Magnituden, Dixon-Ergebnisse und fertige B₀-Karten | Für den Einstieg besonders anschaulich: ein klassisches Bild pro Datei |
| `20260917 MR Praktikum Test/DICOM Enhanced/DICOM` | 11 Bilddateien mit zusammen 333 Frames: 207 Magnitudenframes, 108 Phasenframes, 18 als `REAL` markierte Feldkartenframes | Bildtyp, Echozeit und Skalierung müssen je Frame ausgewertet werden |
| `LfB BMT Praktikum/DICOM` | Drei Enhanced-MR-Bilddateien mit zusammen vier Magnitudenframes und einem tatsächlichen Realteil-Frame | Für Magnitudenübungen verwendbar; allein kein vollständiger Datensatz zur Phasendifferenz-B₀-Berechnung |

**Es wurde kein `IMAGINARY`-Bildanteil gefunden.** Der einzelne echte Realteil liegt in `LfB BMT Praktikum/DICOM/IM_0004`, Frameindex 1, bei TE = 9,201 ms. Magnitude plus Realteil liefert keine eindeutige Phase, weil das Vorzeichen des Imaginärteils unbekannt bleibt. Die anderen `REAL`-Frames im großen Enhanced-Export tragen `FrameType = … FIELD_MAP` und die Einheit Hz: Sie sind bereits berechnete Feldkarten, keine Realteile des ursprünglichen MR-Signals.

Die vorhandenen echten Phasenbilder reichen für die Zusatzaufgabe aus. Eine Rekonstruktion aus Re/Im ist für diese Beispieldaten nicht erforderlich und mangels Imaginärteil auch nicht möglich.

### 3.2 So werden Phasenbilder erkannt und skaliert

| Exportform | Erkennung | Physikalische Skalierung |
| --- | --- | --- |
| Classic | `ImageType (0008,0008) = ORIGINAL, PRIMARY, PHASE MAP, P, FFE` | `RescaleType (0028,1054) = mrad`; Slope/Intercept auf gespeicherte Pixel anwenden, danach durch 1000 teilen |
| Enhanced | In `PerFrameFunctionalGroupsSequence (5200,9230)`, innerhalb der `MRImageFrameTypeSequence (0018,9226)`: `ComplexImageComponent (0008,9208) = PHASE` und `FrameType (0008,9007)` mit `P` | `RealWorldValueMappingSequence (0040,9096)` mit `MeasurementUnitsCodeSequence (0040,08EA) = mrad`; danach Umrechnung in rad |

Für die geprüften September-Phasenbilder gilt näherungsweise:

$$
\phi_{\mathrm{rad}}=\frac{1{,}53455433455433\cdot \mathrm{Pixelwert}-3142}{1000}.
$$

Diese Zahlen sind ein Befund der Beispieldaten, keine universellen Konstanten. Im späteren Notebook liest der Import die Skalierung aus der jeweiligen Datei beziehungsweise dem jeweiligen Frame.

Wichtig beim Enhanced-Export: In der `PixelValueTransformationSequence` steht hier teilweise nur `RescaleType = US`, während die physikalische Einheit erst im Real-World-Mapping steht. Beide Transformationen sind alternative Abbildungen der gespeicherten Pixelwerte und werden **nicht hintereinander** angewandt. Eine beliebige Normierung der gespeicherten Werte auf $[-\pi,\pi]$ ist ebenfalls keine verlässliche Alternative. Grundlage: DICOM PS3.3, Abschnitt C.7.6.16.2 [3].

### 3.3 Geeignete Aufnahmen für das Notebook

Alle unten aufgeführten September-Echobilder besitzen neun Schichten mit 512 × 512 rekonstruierten Pixeln. Die Bildmatrix ist nicht automatisch die tatsächlich akquirierte räumliche Auflösung.

| Aufnahme | Classic-Seriennummern | Enhanced-Datei | TE in ms | Verwendung |
| --- | --- | --- | --- | --- |
| `T1W_FFE dual echo` | `701001`, `701002`, jeweils Magnitude und Phase | `IM_0012`, 36 Frames | 6,901 / 13,800 | Vorschlag für die Basisaufgabe: OP-/IP-Magnituden derselben Aufnahme |
| `T1W_FFE triple echo` | `801001`, `801002`, `801003`, jeweils Magnitude und Phase | `IM_0016`, 54 Frames | 9,201 / 16,101 / 23,001 | Zwei als IP geplante äußere Echos für B₀; mittleres Echo als OP-Beispiel |
| `T1W_FFE dual echo button` | `1101001`, `1101002` | `IM_0027`, 36 Frames | 6,901 / 13,800 | Vergleich mit Störeinfluss |
| `T1W_FFE triple echo button` | `1201001`, `1201002`, `1201003` | `IM_0029`, 54 Frames | 9,201 / 16,101 / 23,001 | Spätere Vertiefung bei stärkerer Inhomogenität |
| `T1W_FFE IP` / `T1W_FFE OP` | Phasenserien `501032` / `601032` | `IM_0004` / `IM_0008`, jeweils 18 Frames | 9,201 / 11,501 | Vorhandene Phasen demonstrieren; als IP-/OP-Paar keine einfache B₀-Karte im gemischten Phantom |
| Scanner-B₀ ohne / mit `button` | Feldkarten `1401089` / `1301089` | `IM_0035` / `IM_0030`, jeweils 18 Frames inklusive Magnitude | Feldkarten-TE als 0 gespeichert | Vergleichskarten in Hz; TE = 0 nicht als Echozeitabstand benutzen |

Beispiele für separate klassische Phasenbilder: `IM_0099` bei 6,901 ms, `IM_0100` bei 13,800 ms sowie `IM_0147`, `IM_0148`, `IM_0149` bei den drei Triple-Echo-Zeiten. Die tatsächliche Zusammengehörigkeit wird anhand der Geometrie geprüft, nicht aus den Dateinamen abgeleitet.

Beim Enhanced-Triple-Echo liegen beispielsweise in `IM_0016` die Phasen der ersten Schicht an den Python-Frameindizes 27, 28 und 29. Diese Indizes dienen nur der Nachvollziehbarkeit des Befunds; die spätere Auswahl darf sie nicht fest einprogrammieren.

Die Zuordnung IP/OP ist mit dem in Experiment 1 bestimmten Fett-Wasser-Frequenzabstand zu prüfen. Aus den vorhandenen Echozeiten lässt sich allein kein unabhängig gemessener Frequenzabstand behaupten. Der kleine LfB-Datensatz enthält bei 9,2/16,1 ms ein IP-/OP-Magnitudenpaar; das ist kein Paar aus zwei IP-Phasenbildern.

Die vom Scanner bereits getrennten Wasser-/Fettbilder der `2pt`-Serien dienen als qualitative Zusatzansicht. Sie werden nicht versehentlich als Roh-Echobilder importiert. Da sie aus anderen Akquisitionen stammen, sind sie auch kein unmittelbarer quantitativer Goldstandard für die selbst rekonstruierte Dual-Echo-Aufnahme.

## 4. Didaktischer Aufbau

Jede Teilaufgabe besteht aus einer kurzen Erklärung mit einem konkreten Arbeitsauftrag, unmittelbar gefolgt von einer Codezelle mit **einer oder zwei kurzen Codezeilen**. Danach beginnt die nächste Teilaufgabe. Wenn ein Arbeitsschritt mehr Code benötigt, wird er in mehrere Teilaufgaben aufgeteilt; mehrere Anweisungen werden nicht künstlich in eine lange Zeile gepackt.

Die Erklärung umfasst in der Regel ein bis drei kurze Sätze. Eine nötige Formel steht direkt beim zugehörigen Rechenschritt. Variablen, Bibliotheken, Funktionen und Arrays werden an den gerade geladenen DICOM-Daten erklärt. Die erste Zelle darf vollständig vorgegeben sein; später ergänzen die Studierenden einzelne Ausdrücke oder schreiben selbst eine bis zwei Zeilen.

- **Direkt mit DICOM beginnen:** Bereits die erste Codezelle importiert pydicom und lädt eine vorhandene Datei.
- `Shift + Enter` im ersten Arbeitsauftrag erklären. Weitere Bedienhinweise jeweils dann geben, wenn sie benötigt werden.
- Die Bedeutung von `=` beim geladenen DICOM-Objekt erläutern; `.shape` am ausgelesenen Bild, Indizes an dessen Pixeln und Division beim Auslesen beziehungsweise Umrechnen der Echozeit.
- Bibliotheken erst bei ihrer Verwendung importieren, ebenfalls in kleinen Zellen. Umfangreiche Vorbereitung erfolgt vor dem Praktikum.
- Zunächst eine einzige Schicht auswerten. Weitere Schichten später als Wiederholung anbieten.
- Verständliche Namen verwenden und Zwischenwerte sichtbar ausgeben, damit jede Teilaufgabe ein überprüfbares Ergebnis hat.
- Komplexere Dateisuche, Geometrieprüfung und Darstellung hinter dokumentierten Hilfsfunktionen bereitstellen. Deren Aufruf bleibt kurz; die eigentlichen Rechenformeln bleiben für die Studierenden sichtbar.
- Fachliche Hintergründe aus diesem Konzept sind Material für die Betreuung. Die ausführlichen Analysen und Herleitungen werden nicht als lange Textblöcke in das studentische Notebook übernommen.

### 4.1 Konkreter Einstieg des späteren Notebooks

Diese Vorschau zeigt das gewünschte Muster. Die Beispieldatei existiert im Projekt; der relative Pfad gilt bei einem Notebook-Start im Projektordner. Für die spätere Auslieferung wird der Pfad an den mitgelieferten Beispielordner angepasst.

**Teilaufgabe 1: Eine DICOM-Datei laden.** DICOM speichert Bilddaten und Angaben zur Aufnahme. Führen Sie die Zelle mit `Shift + Enter` aus; die Variable `dicom` enthält anschließend die geladene Datei.

```python
import pydicom
dicom = pydicom.dcmread("20260917 MR Praktikum Test/Dicom Classic/DICOM/IM_0081")
```

**Teilaufgabe 2: Die Bilddaten auslesen.** `pixel_array` liefert die gespeicherten Pixelwerte. Lesen Sie die Bildgröße mit `.shape` aus.

```python
pixelwerte = dicom.pixel_array
print(pixelwerte.shape)
```

**Teilaufgabe 3: Das geladene Bild ansehen.** Matplotlib kann ein Zahlenarray als Grauwertbild darstellen. Diese erste Ansicht zeigt die gespeicherten Werte; die Skalierung für die spätere Rechnung folgt als eigene Teilaufgabe.

```python
import matplotlib.pyplot as plt
plt.imshow(pixelwerte, cmap="gray")
```

**Teilaufgabe 4: Die tatsächliche Echozeit auslesen.** Im Classic-DICOM steht sie in `EchoTime`, in Millisekunden. Lesen Sie den Wert aus und geben Sie ihn mit Einheit aus.

```python
te_ms = float(dicom.EchoTime)
print("Echozeit [ms]:", te_ms)
```

Danach folgen in demselben Muster Bildtyp, Skalierung, zweites Bild und die eigentliche Dixon-Rechnung. Bei Enhanced-DICOM macht eine bereitgestellte Funktion die entsprechenden Frame-Metadaten genauso einfach zugänglich.

## 5. Zeitplan für 120 Minuten und Schritte des Pflichtteils

Das Notebook ist auf **120 Minuten insgesamt** ausgelegt. Der Pflichtteil umfasst 80 Minuten einschließlich der direkt an den DICOM-Daten erklärten Python-Grundlagen. Für die optionale B₀-Karte sind innerhalb desselben Zeitfensters 30 Minuten reserviert. Die letzten 10 Minuten dienen kurzen Rückfragen, dem Sichern der Ergebnisse und als Puffer. Die technische Umgebung und die aufgenommenen DICOM-Exporte werden vorher bereitgestellt; der erste studentische Arbeitsschritt ist unmittelbar das Laden einer DICOM-Datei.

### 5.1 Ablauf und Zeitmarken

| Zeit ab Beginn | Dauer | Inhalt | Ziel am Ende des Blocks |
| --- | --- | --- | --- |
| 0–10 min | 10 min | DICOM laden, Pixelwerte auslesen, erstes Bild anzeigen; Schritte 1–3 | Ein MRT-Bild ist geladen und sichtbar |
| 10–25 min | 15 min | Echozeit und Bildtyp auslesen, Skalierung anwenden, Pixel und Ausschnitt ansehen; Schritte 4–7 | Grundlegende Python-Zugriffe und die Bedeutung der Bildwerte sind verstanden |
| 25–40 min | 15 min | Zweites Echo derselben Schicht auswählen, tatsächliche TE auslesen, IP/OP vergleichen; Schritte 8–9 | Ein geeignetes, geometrisch zusammengehöriges Bildpaar liegt vor |
| 40–55 min | 15 min | Addition/Subtraktion implementieren, Ergebnisbilder anzeigen und Wasser/Fett-Zuordnung begründen; Schritte 10–12 | Die einfache Dixon-Rekonstruktion ist durchgeführt |
| 55–70 min | 15 min | Signalmaske und ROI wählen, Mittelwerte und Fett-Signalanteil berechnen; Schritte 13–15 | Ein dokumentiertes ROI-Ergebnis liegt vor |
| 70–80 min | 10 min | Eigene Exporte über dieselbe Auswahl einlesen und die vorhandenen Rechenzellen erneut ausführen; kurze Ergebnisdiskussion; Schritte 16–17 | Der Ablauf funktioniert auch mit eigenen Daten und deren tatsächlichen Echozeiten |
| 80–110 min | 30 min | Optional B₀ aus zwei Phasenbildern bestimmen; alternativ Pflichtteil fertigstellen und Ergebnisse vertiefen | Eine näherungsweise ppm-Karte mit ROI-Kennwerten oder eine vertiefte Dixon-Auswertung liegt vor |
| 110–120 min | 10 min | Kurze Rückfragen, Ergebnisse kontrollieren und speichern; verbleibender Puffer | Notebook und Ergebnisabbildungen sind gesichert |
| **Gesamt** | **120 min** | **Pflichtteil + optionale B₀-Aufgabe beziehungsweise Vertiefung + Abschluss/Puffer** | **Kein zusätzliches Zeitfenster für B₀ erforderlich** |

Die B₀-Aufgabe bleibt freiwillig. Wer sie nicht bearbeitet, nutzt den Block 80–110 Minuten zum Fertigstellen, für eine zweite ROI oder zum Vergleich einer weiteren Schicht. Diese Tätigkeiten erweitern den Pflichtumfang nicht.

Für den Zeitrahmen genügen im Pflichtteil zunächst ein ausgewähltes Echo-Paar und eine ROI. Der Wechsel zu eigenen Daten verwendet die bereits geschriebenen Zellen; ein zweites vollständiges Programmieren derselben Auswertung ist nicht eingeplant. Die Betreuung bietet an den Zeitmarken kurze Hilfen an, damit sich einzelne Import- oder Syntaxfehler nicht über den ganzen Versuch fortsetzen.

### 5.2 Kleine Teilaufgaben des Pflichtteils

| Schritt | Inhalt und studentische Tätigkeit | Sichtbares Ergebnis / Lernkontrolle |
| --- | --- | --- |
| 1. DICOM laden | pydicom importieren und die erste Datei mit `dcmread` öffnen; `=` am geladenen Objekt erklären | Die erste Datei ist geladen; zwei Codezeilen |
| 2. Pixelwerte auslesen | `pixel_array` einer Variablen zuweisen und `.shape` ausgeben | Die Bildgröße ist sichtbar; zwei Codezeilen |
| 3. Erstes Bild anzeigen | Matplotlib importieren und `imshow` aufrufen | Das erste MRT-Bild erscheint; zwei Codezeilen |
| 4. Echozeit auslesen | `EchoTime` in eine Zahl umwandeln und mit Einheit ausgeben | Die tatsächliche TE aus der Datei ist sichtbar; zwei Codezeilen |
| 5. Bildtyp erkennen | Den technischen Bildtyp ausgeben und Magnitude/Phase unterscheiden | Der verwendete Bildtyp ist bekannt; eine Codezeile und eine kurze Antwort |
| 6. Skalierung anwenden | In getrennten Teilaufgaben Pixelwerte in Gleitkommazahlen überführen, Skalierung auslesen und anwenden | Ein für die Rechnung geeignetes Array liegt vor; je ein bis zwei Zeilen |
| 7. Einzelpixel und Ausschnitt | Einen Pixel ausgeben; danach in der nächsten Teilaufgabe einen kleinen Ausschnitt wählen | Indizes und Array-Ausschnitte werden am echten Bild verstanden |
| 8. Zweites Echo laden | In kurzen aufeinanderfolgenden Zellen Aufnahme/Schicht auswählen, zweites Bild laden und dessen Echozeit auslesen; Importhilfe unterstützt beide Exportformen | Ein passendes Echo-Paar derselben Schicht liegt vor |
| 9. IP und OP vergleichen | Beide Echos in getrennten kurzen Darstellungsaufgaben anzeigen; TE-Werte und Messprotokoll zur Zuordnung nutzen | Der Unterschied zwischen IP- und OP-Kontrast wird sichtbar |
| 10. Größeren Signalanteil berechnen | Formel für `(ip + op) / 2` in eine Codezeile übersetzen | Erstes Rekonstruktionsbild; die folgende Teilaufgabe zeigt es an |
| 11. Kleineren Signalanteil berechnen | Formel für `(ip - op) / 2` in eine Codezeile übersetzen | Zweites Rekonstruktionsbild; die folgende Teilaufgabe zeigt es an |
| 12. Wasser/Fett zuordnen | Die Annahme W ≥ F beziehungsweise dokumentierte Phantom-Inhalte prüfen; ein kurzes Zahlenbeispiel verdeutlicht bei Bedarf die Mehrdeutigkeit | Die Bildbeschriftung beruht auf einer benannten Annahme |
| 13. Maske und ROI wählen | Zuerst eine Signal-Schwelle setzen, danach eine rechteckige ROI wählen und anzeigen; jede Tätigkeit erhält eine eigene kurze Teilaufgabe | Die ausgewertete Fläche ist sichtbar kontrolliert |
| 14. Mittelwerte bestimmen | `mean` für Wasser und Fett verwenden; `std` bei Bedarf in einer weiteren Teilaufgabe ergänzen | ROI-Signalwerte sind sichtbar |
| 15. Signalanteil berechnen | Unter dokumentierter Zuordnung $100\overline F/(\overline W+\overline F)$ berechnen und ausgeben | Näherungsweiser Fett-Signalanteil in Prozent; zwei Codezeilen |
| 16. Beobachtungen erklären | Nacheinander kurze Fragen zu ROI-Verschiebung, Rändern, Rauschen und Zuordnung beantworten | Kurze Antworten beziehen sich unmittelbar auf die angezeigten Bilder |
| 17. Eigene Daten einsetzen | Datenpfad beziehungsweise Auswahl ändern und dieselben kurzen Aufgaben erneut ausführen; am Ende speichern | Eigene DICOM-Daten werden mit ihren tatsächlichen TE-Werten ausgewertet |

Eine Tabellenzeile kann mehrere kleine Teilaufgaben beschreiben. Im Notebook werden diese jeweils in das feste Muster Erklärung → ein bis zwei Codezeilen → nächste Erklärung aufgeteilt. Auch Vergleiche, Bildtitel und Speichern werden nicht zu langen Sammelzellen zusammengezogen.

### Wichtige Details der Pflichtauswertung

1. **Skalierung vor der Rechnung:** Rohpixel erst in Gleitkommazahlen überführen. Die vom Import gelieferten Bildwerte verwenden. Kein Subtrahieren von `uint16`-Arrays mit möglichem Überlauf.
2. **Vergleichbare Signalwerte:** Für die Basis möglichst zwei Echos derselben Akquisition auswählen. Slope/Intercept korrigieren die gespeicherte Skalierung, garantieren aber keine identische Signalnormalisierung zwischen getrennten Messungen. Bilder nicht einzeln auf ihren Maximalwert normieren.
3. **Bilddarstellung:** Für direkt verglichene Magnituden eine gemeinsame, erläuterte Fenstereinstellung verwenden. Für Rechnungen keine Fensterung, keine Screenshots und keine auf 8 Bit reduzierten Bilder benutzen.
4. **Zuordnung:** Im idealen Fall ist `anteil_klein / (anteil_gross + anteil_klein)` höchstens 50 %. Das ist ohne weitere Information der kleinere Signalanteil, nicht automatisch der Fettanteil. Für fettdominante ROIs muss die Zuordnung begründet umgekehrt werden.
5. **Ungültige Ergebnisse sichtbar behandeln:** Wenn durch Rauschen, Relaxation oder Fehlzuordnung $M_{\mathrm{OP}}>M_{\mathrm{IP}}$ auftritt, dies markieren und diskutieren. Werte nicht stillschweigend durch Betrag oder Clipping scheinbar plausibel machen.
6. **Zwei Arten von Mittelwerten unterscheiden:** $\overline F/(\overline W+\overline F)$ ist nicht allgemein dasselbe wie der Mittelwert einer pixelweisen Quotientenkarte. In der Pflichtaufgabe das erste, einfachere Verfahren klar benennen.
7. **Phantomwissen:** Lage und Zusammensetzung der Röhrchen beziehungsweise Proben aus dem Messprotokoll übernehmen. Die DICOM-Metadaten liefern keine verlässlichen bekannten Mischungsverhältnisse. Sind solche Referenzbereiche nicht dokumentiert, keine Prozentgenauigkeit gegenüber einer vermeintlichen Grundwahrheit angeben.

## 6. Importkonzept für Beispiel- und eigene Daten

Die Studierenden erhalten einen vorbereiteten, kommentierten Import mit einer einfachen Bedienoberfläche im Notebook. Sie sollen ein DICOM-Bild verstehen, müssen aber keinen vollständigen DICOM-Importer programmieren.

Vorgesehene Bedienung:

1. Einen Datenordner einstellen. Als Standard den September-Classic-Export vorgeben.
2. Eine Übersicht mit Aufnahme, Bildkomponente, Echozeit, Schichtposition und Anzahl anzeigen.
3. Die gewünschte Aufnahme und eine Schicht wählen.
4. Die Funktion liefert eindeutige 2D-Arrays mit zugehörigen Metadaten und Einheiten zurück.
5. Für eigene Daten nur Datenordner, Aufnahmeauswahl und bei Bedarf ROI-Koordinaten ändern.

Der allererste praktische Notebook-Schritt lädt direkt eine einzelne DICOM-Datei. Die robuste Ordnerverarbeitung folgt danach über eine bereitgestellte Hilfsdatei. Deren Aufrufe benötigen im Notebook jeweils nur eine oder zwei Zeilen. Kommentare, Typannotationen, kurze Docstrings und verständliche Fehlermeldungen sind insbesondere in dieser Hilfsdatei vorgesehen; die Einstiegszellen bleiben für Anfänger übersichtlich.

Der Import muss folgende Fälle handhaben:

- Auch Dateien ohne `.dcm`-Endung erkennen. `DICOMDIR`, Präsentationszustände und herstellerspezifische Verwaltungsobjekte ohne Bildpixel überspringen.
- Classic MR und Enhanced MR unterstützen. Bei Enhanced Bildkomponente, Echozeit, Geometrie und Skalierung pro Frame beziehungsweise aus den gemeinsam geltenden Functional Groups lesen.
- Aufnahmeidentität und Bildkomponente getrennt führen: Eine Classic-Serie kann gleichzeitig Magnituden und Phasen enthalten; Enhanced-Dateien können mehrere Echozeiten und Bildtypen enthalten.
- Schichten nach ihrer räumlichen Position entlang der Schichtnormalen sortieren. Echos anhand von Position, Orientierung, Pixelabstand, Matrix und Aufnahmezugehörigkeit paaren; gleiche Arrayform allein reicht nicht.
- Auf Mehrfachkandidaten hinweisen und eine Auswahl verlangen, statt automatisch die erste Datei oder eine ähnlich benannte Serie zu verwenden.
- Pixel-Skalierung genau einmal anwenden und physikalische Einheiten erhalten. Unbekannte Phasenskalierung nicht erraten.
- Inkonsistente Geometrie oder fehlende Pflichtbilder verständlich melden. Bei Bedarf Aufnahme neu auswählen; keine automatische Registrierung als versteckten Reparaturschritt einführen.
- Nur die für den Versuch benötigten technischen Metadaten anzeigen. Keine vollständigen DICOM-Header in das Abgabenotebook drucken.

## 7. Optionale Aufgabe: Näherungsweise B₀-Karte aus zwei Phasenbildern

**Zeitbudget: 30 Minuten innerhalb der insgesamt 120 Minuten, vorgesehen für Minute 80 bis 110.** Die Aufgabe verwendet einen einzigen Datensatz, eine Schicht und eine zusammenhängende ROI. Import, Skalierung, Maskendarstellung und gegebenenfalls Unwrapping sind als Hilfsfunktionen vorbereitet. Die Studierenden lesen die Echozeiten aus und führen die sichtbaren Rechenschritte zu Hz und ppm selbst aus.

| Zeit ab Beginn | Dauer | Teilaufgaben der B₀-Auswertung |
| --- | --- | --- |
| 80–85 min | 5 min | Zwei passende Phasenbilder auswählen; tatsächliche Echozeiten, Einheit und Referenzfrequenz auslesen |
| 85–95 min | 10 min | Phasen darstellen, Signalmaske kontrollieren, zirkuläre Differenz bilden und bei Bedarf vorgegebenes Unwrapping aufrufen |
| 95–103 min | 8 min | ΔTE selbst berechnen, ms in s umrechnen, Feldabweichung in Hz und anschließend ppm bestimmen |
| 103–110 min | 7 min | Karte anzeigen, relative ROI-Homogenität mit Standardabweichung und Peak-to-Peak beschreiben, kurze Interpretation formulieren |
| **B₀ gesamt** | **30 min** | **Eine näherungsweise Karte mit dokumentiertem Zeitabstand, Maske und ROI-Ergebnis** |

Vergleiche mit mehreren Schichten, der `button`-Aufnahme oder einer Scanner-Feldkarte sowie zusätzliche Perzentil-Kennwerte sind Vertiefungen bei verbleibender Zeit. Für die vorgesehene B₀-Aufgabe sind sie nicht erforderlich. Auch im Zusatzteil gilt das Muster kurze Erklärung → eine oder zwei Codezeilen → nächste Teilaufgabe.

### 7.1 Messidee: Zwei möglichst ähnliche Fett-Wasser-Phasenzustände

Für die Erklärung dienen zunächst zwei ideale Echozeiten, bei denen Fett und Wasser relativ zueinander um $2\pi$ beziehungsweise $4\pi$ präzediert sind. Beide Zustände sind damit In-Phase. Mit dem Betrag des in Experiment 1 bestimmten chemischen Frequenzabstands gilt im vereinfachten Einpeak-Modell:

$$
TE_{2\pi}=\frac{1}{|\Delta f_{\mathrm{cs}}|},\qquad
TE_{4\pi}=\frac{2}{|\Delta f_{\mathrm{cs}}|}.
$$

Bei der groben Skriptannahme $|\Delta f_{\mathrm{cs}}|=220\,\mathrm{Hz}$ liegen diese Zeiten bei ungefähr 4,55 und 9,09 ms. Bei ungefähr 217,4 Hz ergeben sich ungefähr 4,6 und 9,2 ms. Das dient der Einordnung; solche Werte müssen am Scanner nicht exakt einstellbar sein.

**Praktisches Beispiel:** Die vorhandenen Phasen bei 9,201 und 23,001 ms derselben Triple-Echo-Aufnahme haben einen Abstand von 13,800 ms. Die Fett-Wasser-Phase durchläuft dazwischen näherungsweise drei volle Umdrehungen. Dieses Paar ist für die grobe Auswertung deshalb ebenfalls sinnvoll, obwohl es nicht das ideale 2π-/4π-Paar ist. Diese Zahlen sind ausschließlich die Beschreibung der Beispieldaten. Das Notebook liest für jede neu ausgewählte Aufnahme deren tatsächliche Echozeiten ein.

Die chemische Phasenentwicklung soll sich zwischen den Echos ungefähr um ein ganzzahliges Vielfaches von $2\pi$ unterscheiden. Kleine Abweichungen werden als Näherungsfehler akzeptiert. Die Studierenden sollen keine exakten Echozeiten erzwingen und die exportierten Phasen auch nicht künstlich auf ideale Werte korrigieren. Werden ganz andere Echozeiten eingestellt, funktioniert die Rechnung mit den neuen Metadaten weiter; ob chemische Phase die Interpretation als B₀ beeinflusst, bleibt eine physikalische Voraussetzung und wird kurz besprochen.

**2π und 4π bezeichnen die chemische Fett-Wasser-Phasenentwicklung.** Sie sind weder eine Einstellung des darstellbaren Phasenbereichs noch zwei Bilder, die man durch Multiplizieren derselben Phase erzeugt. Die exportierte Phase bleibt modulo $2\pi$ gespeichert und enthält zusätzlich unter anderem Empfangsphase und lokale Off-Resonanz.

Für eigene Messungen möglichst beide Echos in einer gemeinsamen Gradientenecho-Akquisition mit direktem Phasenexport aufnehmen. Gleiche Schicht, Orientierung, Auflösung, Objektlage, Shim- und Frequenzeinstellung beibehalten. Bei getrennten Scans können zusätzliche Phasenoffsets entstehen, die bei der Subtraktion nicht zuverlässig verschwinden. Die Software darf die erreichbaren Echozeiten vorgeben; die Rechnung passt sich diesen Zeiten an.

### 7.2 Was mit den vorhandenen Beispielen möglich ist

- Echte Phasen sind vorhanden; kein Re/Im-Umweg ist nötig.
- Ein direktes **2π-/4π-Phasenpaar** ist in den geprüften Exporten nicht enthalten und wird für diese Aufgabe nicht nachgefordert.
- Das erste Lernbeispiel nutzt die äußeren Echos der Triple-Echo-Aufnahme. Nach dem vorgesehenen Timing entsprechen sie ungefähr 4π und 10π, also zwei annähernden IP-Zeitpunkten. Die Bildtitel zeigen immer die ausgelesenen tatsächlichen Echozeiten.
- Das mittlere Triple-Echo bei 16,101 ms sowie das frühe Dual-Echo bei 6,901 ms sind nach diesem Timing OP-Zeitpunkte. Ein beliebiges IP-/OP-Phasenpaar vermischt in gemischten Proben chemische Phase und Feldphase und wird nicht als einfache B₀-Messung verwendet.
- Vorhandene Scanner-Feldkarten in Hz eignen sich als Plausibilitätsvergleich, sofern Schicht, Objektzustand und Einstellungen zusammenpassen. Sie stammen aus eigenen Akquisitionen; Abweichungen sind nicht ausschließlich Rekonstruktionsfehler.

Die reale Fettresonanz besitzt mehrere Peaks. Auch bei nominellen IP-Zeitpunkten ist daher eine vollständige chemische Phasenauslöschung nur eine Näherung. Zunächst einen ausreichend signalstarken, möglichst wasserhaltigen Bereich verwenden. In gemischten und fetthaltigen Bereichen die Karte ausdrücklich als näherungsweise Feldabweichung beschriften.

Einordnung des Timingfehlers an einem einfachen Rechenbeispiel: Bei angenommenen 220 Hz und ΔTE = 13,8 ms entstehen 3,036 statt genau 3 chemische Umdrehungen. Der Rest entspricht 0,226 rad. Für reines Fett im Einpeak-Modell würde das als zusätzlicher Frequenzbetrag von ungefähr 2,61 Hz beziehungsweise 0,041 ppm erscheinen. Das ist eine Modellabschätzung, kein aus den Daten gemessener Fehler und keine allgemeine Fehlergrenze für alle Mischungen. Die Beobachtung lässt sich im Notebook kurz als „Echozeiten nur ungefähr passend“ erklären; sie verhindert die grobe Lehr-Auswertung nicht.

### 7.3 Rechenweg: rad → Hz → ppm

Unter der gewählten Phasenkonvention und bei gleichbleibendem, TE-unabhängigem Phasenoffset beschreibt

$$
\phi(x,y,TE)=\phi_0(x,y)+2\pi\,\Delta f(x,y)\,TE
$$

die Off-Resonanz. Zwei geeignete Echos entfernen den gemeinsamen Offset. Zuerst die korrekt skalierten Phasen in rad und die Echozeitdifferenz in Sekunden bestimmen.

**Die Echozeiten lesen die Studierenden aus ihren ausgewählten DICOM-Bildern aus:**

| Export | Quelle der tatsächlichen Echozeit | Einheit |
| --- | --- | --- |
| Classic MR | `EchoTime (0018,0081)`, direkt als `ds.EchoTime` zugänglich | ms |
| Enhanced MR | `EffectiveEchoTime (0018,9082)` in der `MREchoSequence`, pro Frame oder in gemeinsam geltenden Functional Groups | ms |

Die bereitgestellte Importfunktion macht diese Information für beide Exportformen unter demselben Metadatenfeld `echozeit_ms` zugänglich. Die Studierenden übernehmen den Wert selbst in eine Variable, geben ihn aus und berechnen anschließend die Differenz. Auch hier bleibt jede Codezelle auf eine oder zwei Zeilen begrenzt. Schematische Folge, nachdem `meta_1` und `meta_2` beim DICOM-Import entstanden sind:

**Teilaufgabe: Echozeiten übernehmen.** Lesen Sie die Werte der beiden ausgewählten Echos aus den DICOM-Metadaten aus.

```python
te_1_ms: float = float(meta_1["echozeit_ms"])
te_2_ms: float = float(meta_2["echozeit_ms"])
```

**Nächste Teilaufgabe: Werte kontrollieren.** Geben Sie die beiden Echozeiten mit Einheit aus.

```python
print("Echo 1 [ms]:", te_1_ms)
print("Echo 2 [ms]:", te_2_ms)
```

**Nächste Teilaufgabe: Zeitabstand berechnen.** Ziehen Sie die Echozeiten voneinander ab und rechnen Sie Millisekunden in Sekunden um.

```python
delta_te_ms: float = te_2_ms - te_1_ms
delta_te_s: float = delta_te_ms / 1000.0
```

**Nächste Teilaufgabe: Ergebnis ausgeben.** Kontrollieren Sie den Zeitabstand, bevor Sie damit die Feldkarte berechnen.

```python
print("Echozeitabstand [s]:", delta_te_s)
```

Der Import beziehungsweise die Auswahl ordnet Echo 1 und 2 nach der tatsächlichen Echozeit und hält Bilder und Metadaten zusammen. Bei fehlender oder identischer Echozeit folgt eine verständliche Meldung. Es gibt keinen stillen Ersatz durch die Beispielwerte. Ändern die Studierenden am Scanner die Echozeiten, ändern sich nach erneutem Import entsprechend ΔTE, Bildtitel und das Ergebnis in Hz/ppm.

Die zirkuläre Differenz ist

$$
\Delta\phi_{\mathrm{wrapped}}=
\arg\!\left[\exp\!\left(i(\phi_2-\phi_1)\right)\right].
$$

Diese Rechnung vermeidet künstliche Sprünge durch die getrennte Speicherung der Phasen, ist aber **noch kein Unwrapping**. Nach gegebenenfalls notwendigem Unwrapping gilt [4]:

$$
\Delta f_{\mathrm{Hz}}(x,y)=
\frac{\Delta\phi_{\mathrm{unwrapped}}(x,y)}{2\pi\,(TE_2-TE_1)}.
$$

Mit der Referenzfrequenz $f_0$ in Hz wird daraus die relative Feldabweichung:

$$
\Delta B_{0,\mathrm{ppm}}(x,y)=10^6\frac{\Delta f_{\mathrm{Hz}}(x,y)}{f_0}.
$$

`ImagingFrequency` beziehungsweise `TransmitterFrequency` aus dem DICOM-Export ist in MHz angegeben und muss dafür mit $10^6$ in Hz umgerechnet werden. In den September-Echobildern beträgt die Frequenz ungefähr 63,889604 MHz; 1 ppm entspricht dort ungefähr 63,89 Hz. Innerhalb eines ausgewählten Echo-Paars muss dieselbe Referenz gelten.

Falls keine verlässliche Referenzfrequenz exportiert wurde, ist ein ausdrücklich dokumentierter Näherungswert $f_0=(\gamma/2\pi)B_{\mathrm{ref}}$ für Protonen möglich, mit $\gamma/2\pi\approx42{,}5775\,\mathrm{MHz/T}$. Die nominalen 1,5 T nicht stillschweigend mit der exakten Frequenzreferenz gleichsetzen. Das Vorzeichen der resultierenden Karte hängt von der Scanner-Phasenkonvention ab und wird einmal im Pilotlauf geprüft.

### 7.4 Kleinschrittige Aufgabenfolge

Auch diese Zusatzaufgabe verwendet durchgehend kurze Erklärungen und jeweils eine oder zwei Codezeilen. Jeder Listenpunkt wird bei Bedarf in weitere Teilaufgaben aufgeteilt; Aufrufen, Berechnen und Anzeigen sind getrennte Aufgaben.

1. Ein Magnitudenbild und die zwei ausgewählten Phasenbilder derselben Schicht laden; Echozeiten und Einheiten anzeigen.
2. Die Magnitude und beide Phasen nebeneinander darstellen. Für die Phase eine zyklische Farbskala mit Beschriftung in rad verwenden.
3. An einem Zahlenbeispiel zeigen, dass Phasen nahe $+\pi$ und $-\pi$ nahe beieinander liegen können.
4. Die bereitgestellte zirkuläre Differenzfunktion anwenden und das Differenzbild betrachten. Komplexe Exponentialfunktionen müssen die Studierenden hierfür nicht selbst implementieren.
5. Eine Maske aus ausreichend hohem Signal in **beiden** Magnitudenbildern bilden, mit einer inneren Objekt-ROI kombinieren und als Overlay kontrollieren. In Luft und an Signal-Auslöschungen ist die Phase nicht zuverlässig.
6. Falls erforderlich, eine vorgegebene Funktion zum maskierten 2D-Unwrapping aufrufen. Danach beide Phasendifferenzbilder vergleichen. Rauschpixel nicht als Verbindungen zwischen getrennten Objektteilen verwenden [5].
7. Die beiden Echozeiten aus den DICOM-Metadaten auslesen, zur Kontrolle ausgeben, den Zeitabstand selbst berechnen und von ms in Sekunden umrechnen. Eine andere Aufnahme auswählen und beobachten, wie sich die ausgelesenen Werte ändern.
8. In einer kurzen Rechenzelle durch $2\pi\Delta TE$ teilen: Ergebnis in Hz.
9. Die Referenzfrequenz von MHz in Hz umrechnen und selbst die ppm-Formel anwenden.
10. Die ppm-Karte mit einer divergierenden Farbskala, transparenter Außenmaske und mm-Achsen darstellen. Bei Vergleichen dieselbe Farbskala verwenden.
11. Für eine zusammenhängende ROI zunächst eine **relative** Karte durch Abzug des ROI-Mittelwerts zeigen und Standardabweichung sowie Peak-to-Peak-Spannweite berechnen. Optional P95 − P5 ergänzen. Die nicht zentrierte Karte bleibt zur Einordnung erhalten, besitzt aber ohne gesicherte Referenz gegebenenfalls einen unbekannten globalen Offset.
12. Erklären, welche Aussage die Karte über genau diese Schicht und ROI erlaubt und welche Pixel ausgeschlossen wurden.

### 7.5 Eindeutigkeitsgrenzen und Auswertung der Homogenität

Ohne zusätzliche Information ist die Feldfrequenz aus zwei Echos nur modulo $1/\Delta TE$ bestimmbar. Das um null zentrierte, nicht gewrappte Intervall ist:

$$
-\frac{1}{2\Delta TE}\leq\Delta f<\frac{1}{2\Delta TE}.
$$

Beim vorhandenen Triple-Echo-Abstand von 13,8 ms sind das ungefähr ±36,23 Hz beziehungsweise ±0,567 ppm. Schon für moderate Feldvariationen können deshalb Wraps auftreten. Bei einem neuen 2π-/4π-Paar mit $\Delta TE\approx4{,}55$ ms erweitert sich das Intervall auf ungefähr ±110 Hz beziehungsweise ±1,72 ppm bei der Beispiel-Referenzfrequenz. Auch dieses Paar garantiert keine wrapfreie Karte.

Räumliches Unwrapping kann bei hinreichend glatten, signalstarken Bereichen helfen. Es bestimmt aber keinen grundsätzlich unbekannten globalen Ganzzahl-Offset; getrennte Objektteile können zudem unterschiedliche unbekannte Offsets behalten. Einen solchen Offset nur anhand einer unabhängigen Referenz beziehungsweise eines begründeten Feldbereichs festlegen. Ein späteres Kürzerecho-Paar könnte die Eindeutigkeit erweitern, muss im gemischten Phantom aber chemische Phasenanteile berücksichtigen.

Für die Lehraufgabe daher zuerst eine zusammenhängende, verlässlich entfaltbare ROI verwenden und die relative Homogenität darin bestimmen. Dafür ist ein unbekannter gemeinsamer konstanter Offset unerheblich. Statistiken über mehrere getrennte Röhrchen erst nach gesicherter gemeinsamer Referenz bilden. Falls ein Bereich wegen Signalverlust oder unzuverlässigem Unwrapping nicht auswertbar ist, ihn ausblenden und die gültige Auswertefläche anzeigen. Die Zusatzaufgabe verlangt keine absolute hochgenaue Feldkalibrierung.

Die Karte zeigt die **lokale Feldabweichung**. Homogenität beschreiben anschließend Streuungsmaße innerhalb einer benannten ROI:

- Standardabweichung in ppm.
- Peak-to-Peak in ppm: Maximum minus Minimum; stark empfindlich gegenüber Ausreißern.
- Optional P95 − P5 in ppm, mit Hinweis auf die verbleibende ROI-Abhängigkeit.

Den ROI-Mittelwert zusätzlich als Frequenz-/Feldoffset berichten. Für eine relative Homogenitätsdarstellung kann er abgezogen werden; das muss in Titel und Ergebnis stehen. Eine einzelne Schicht beschreibt nicht die Homogenität eines ganzen dreidimensionalen Messvolumens. Signalverlust nahe dem Störobjekt ist fehlende Information und kein Beleg für ein homogenes Feld.

## 8. Vorbereitung und spätere Dateien

Für den Pflichtteil genügen Python, JupyterLab, NumPy, Matplotlib und pydicom. Für das vorgegebene 2D-Unwrapping kommt scikit-image hinzu. Die bestehende `requirements.txt` enthält bisher kein pydicom und kein scikit-image; für das MRT-Notebook ist deshalb eine eigene kleine Abhängigkeitsliste sinnvoll.

Geplante Vorbereitung durch die Lehrenden:

1. Eine lauffähige Umgebung vor dem Praktikum einrichten und auf den Auswerte-PCs prüfen. Im Praktikum keine individuelle Paketinstallation voraussetzen.
2. Eine anschauliche Beispielschicht festlegen und Phantom-Inhalte beziehungsweise geeignete ROIs dokumentieren.
3. Den Import für Classic und Enhanced vorbereiten und eine verständliche Auswahlansicht erstellen.
4. Zuerst das Basisnotebook ohne B₀ fertigstellen und mit einer Person mit wenig Python-Erfahrung innerhalb des 80-Minuten-Budgets durchgehen: Der Einstieg muss die DICOM-Datei laden, jede Codezelle umfasst nur eine oder zwei kurze Zeilen, und neue Python-Begriffe werden unmittelbar an der jeweiligen Aufgabe erklärt.
5. Anschließend die B₀-Zusatzaufgabe mit dem vorhandenen Triple-Echo-Beispiel im 30-Minuten-Budget prüfen. Falls der Umfang zu groß ist, zusätzliche Vergleiche und Interpretationsfragen kürzen; der gesamte Ablauf einschließlich Abschluss und Puffer bleibt auf 120 Minuten begrenzt.
6. Für den eigentlichen Versuch zwei mit der Scanner-Software erreichbare, annähernde IP-Echos inklusive direkt exportierter Phase verwenden. Die tatsächlichen Echozeiten werden im Notebook aus den DICOM-Metadaten gelesen; keine exakten 2π-/4π-Zeitpunkte verlangen.

Vorgesehene Dateistruktur für die spätere Umsetzung:

| Datei / Ordner | Zweck |
| --- | --- |
| `experiment3_student.ipynb` | Erklärungen, kurze Ergänzungsaufgaben und Antwortfelder |
| `experiment3_loesung.ipynb` | Vollständige Fassung mit Hinweisen für die Betreuung |
| `mrt_hilfen.py` | Dokumentierter Import, Geometrieprüfung, Skalierung und gegebenenfalls Unwrapping |
| `requirements_mrt.txt` | Kleine, nach Erprobung festgelegte Paketliste |
| `daten/beispiel/` und `daten/eigene/` | Austauschbare Eingabedaten; Originalexporte erhalten |
| `ergebnisse/` | Gespeichertes Notebook, Abbildungen und ROI-Ergebnistabelle |

Die Startanleitung soll konkret erklären: Voraussetzungen installieren beziehungsweise vorbereitete Umgebung wählen, JupyterLab im Praktikumsordner starten, `experiment3_student.ipynb` öffnen und die Zellen von oben nach unten ausführen. Diese Dateien sind geplant und wurden in diesem Konzeptschritt noch nicht erstellt.

## 9. Abgabe und sinnvolle Erprobung

Pflichtabgabe: ausgeführtes Notebook mit ausgewählter Aufnahme und Schicht, tatsächlichen Echozeiten, Viereransicht, sichtbarer ROI, begründet zugeordnetem Signalanteil und kurzen Antworten zur Mehrdeutigkeit und zu den Modellgrenzen. Optional dazu B₀-Karte in ppm, Maske, Echozeitabstand, Referenzfrequenz, Angaben zum Unwrapping und eine ROI-Tabelle zur Homogenität.

Für die spätere Implementierung sind folgende fachliche Prüfungen sinnvoll:

1. An den Zahlenbeispielen Wasser/Fett-Vertauschung und den auf 50 % begrenzten kleineren Signalanteil nachvollziehen.
2. Für dieselbe ausgewählte Schicht Classic- und Enhanced-Import nach Skalierung vergleichen; Magnitude, Phase, Echozeit und Geometrie müssen bis auf dokumentierte Rundungsabweichungen übereinstimmen.
3. Sicherstellen, dass das kleine LfB-Beispiel für die B₀-Aufgabe verständlich „passendes Phasenpaar fehlt“ meldet und nicht den Realteil als Phase verwendet.
4. Einen künstlich vorgegebenen Frequenzoffset in zwei simulierte Phasen übersetzen und zurückrechnen. Beispiel: 1 ppm bei 63,889604 MHz und ΔTE = 4,6 ms erzeugt ungefähr 1,847 rad Phasendifferenz. Dadurch lassen sich ms/s-, mrad/rad- und MHz/Hz-Fehler erkennen.
5. Ein Beispiel mit Wrap und eines mit getrennten Objektteilen prüfen; die Grenzen der Referenzierung müssen sichtbar bleiben.
6. Eine eigene neue Exportserie mit **anderen Echozeiten** ohne Dateiumbenennung durchlaufen lassen: Das Notebook muss die neuen TE-Werte aus den DICOM-Metadaten anzeigen und mit dem neuen ΔTE rechnen. Anschließend aus einem frisch gestarteten Kernel vollständig ausführen.

Ein vollständiger automatischer Testkatalog ist für diesen Konzeptschritt nicht erforderlich. Vor einer studentischen Nutzung müssen insbesondere die gewählte Beispielslice, die Signal-Zuordnung und die reale B₀-Auswertung fachlich erprobt werden.

Bereits im Konzeptschritt geprüft: Die kurzen Python-Schritte zum Timing lesen die realen Metadaten zweier unterschiedlicher Echo-Paare und berechnen entsprechend 13,800 ms beziehungsweise 6,899 ms Abstand, ohne Änderung der Rechnung. Außerdem stimmen die skalierten Phasen und die Schichtgeometrie der beispielhaft verglichenen Triple-Echo-Bilder aus Classic und Enhanced bis auf numerische Rundung überein. Das bestätigt Import- und Timing-Grundlagen; eine vollständige B₀-Auswertung ist damit noch nicht validiert.

## 10. Quellen und Bezugspunkte

Die Empfehlungen zur Unterrichtsstruktur sind Konzeptvorschläge. Die Zahlen und Exportbefunde stammen aus der lokalen Prüfung vom 03.11.2026. Die Referenzen dienen der methodischen Einordnung und späteren Umsetzung.

1. Lokales Versuchsskript, PDF-Seiten 8 bis 11 und 14; lokale DICOM-Exporte in `20260917 MR Praktikum Test` und `LfB BMT Praktikum`.
2. Dixon, W. T. (1984). *Simple proton spectroscopic imaging*. Radiology 153(1), 189–194. [Originalarbeit](https://doi.org/10.1148/radiology.153.1.6089263). Ergänzend zur Zuordnungsfrage: Ahmad et al. (2010), *A method for automatic identification of water and fat images from a symmetrically sampled dual-echo Dixon technique*, MRI 28(3), 427–433. [Originalarbeit](https://doi.org/10.1016/j.mri.2009.11.005).
3. DICOM PS3.3, *Common Functional Group Macros*, besonders Pixel Value Transformation und Real World Value Mapping. [Offizieller Standard](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.16.2.html).
4. NiPreps SDCFlows, *Methods and implementation*, Abschnitt *Phase-difference B0 estimation*: Zusammenhang zwischen Phasendifferenz, Echozeitabstand und Feldkarte. [Offizielle Methodendokumentation](https://www.nipreps.org/sdcflows/2.12/methods.html).
5. scikit-image, `restoration.unwrap_phase`: 2D-Unwrapping und Verwendung maskierter Arrays. [Offizielle Dokumentation](https://scikit-image.org/docs/stable/api/skimage.restoration.html#skimage.restoration.unwrap_phase).
6. pydicom, Pixelverarbeitung und Rescale-Operationen. [Offizielle Dokumentation](https://pydicom.github.io/pydicom/stable/reference/pixels.html).
