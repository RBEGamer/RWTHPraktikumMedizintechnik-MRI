# Startanleitung für Studierende · MRT-Praktikum

In diesem Praktikum untersuchen Sie eine mit Wasser und Öl gefüllte Flasche. Sie laden MRT-Bilder, vergleichen zwei Echos und werten einen Wasser- und einen Ölbereich aus. Alle Aufgaben beziehen sich auf **eine Schichtebene**. Die optionale Zusatzaufgabe behandelt die lokale Magnetfeldabweichung B₀.

Python-Vorkenntnisse sind nicht erforderlich; die benötigten Schritte werden im Notebook erklärt.

Die [Scan-Anleitung für Studierende](output/pdf/scan_anleitung.pdf) zeigt, welche MRT-Aufnahmen Sie benötigen, wie Sie die gemeinsame Schichtebene planen und welche DICOM-Bilder Sie exportieren sollen.

## 1. Notebook öffnen

Die Arbeitsumgebung ist am Praktikumsrechner vorbereitet.

1. Öffnen Sie die bereitgestellte **JupyterLab-Umgebung** und wechseln Sie in Ihren Arbeitsordner.
2. Öffnen Sie dort **`experiment3_student.ipynb`** per Doppelklick.
3. Falls eine Kernel-Auswahl erscheint, wählen Sie **Python 3 (MRT-Praktikum)**. Der Kernel führt Ihre Codezellen aus.
4. Speichern Sie über **File → Save Notebook As…** eine eigene Fassung, beispielsweise `experiment3_bearbeitet.ipynb`, **im selben Ordner**.
5. Klicken Sie in die erste Codezelle und drücken Sie **Shift + Enter**. Diese Zelle lädt bereits das erste DICOM-Bild.

Der Ordner muss neben Ihrem Notebook die Datei `mrt_hilfen.py` und den Unterordner `daten` enthalten. Verschieben Sie das Notebook deshalb nicht einzeln. Wenn JupyterLab oder der passende Kernel fehlt, wenden Sie sich an die Betreuung.

## 2. Aufgaben bearbeiten

- Lesen Sie jeweils die kurze Erklärung und führen Sie anschließend die zugehörige Codezelle mit **Shift + Enter** aus. Arbeiten Sie von oben nach unten.
- Ersetzen Sie die markierten Stellen **`...`** durch Ihren Code. Eine noch offene Ergänzungsaufgabe kann eine Fehlermeldung auslösen.
- Für schriftliche Antworten doppelklicken Sie auf das jeweilige Textfeld im Notebook. Tragen Sie Ihre Antwort ein und schließen Sie mit **Shift + Enter** ab.
- Speichern Sie regelmäßig mit **Strg + S** beziehungsweise **⌘ + S**.

Beginnen Sie mit den voreingestellten Beispieldaten. Die Echozeiten lesen Sie aus den DICOM-Dateien aus; die Aufgaben führen Sie durch die einzelnen Rechenschritte.

## 3. Aufnahme und Bildbereich auswählen

Die Auswahlfelder bestimmen die Aufnahme und die Echos. Mit den Schiebereglern wählen Sie eine **ROI**, also einen auszuwertenden Bildbereich. Die grüne Markierung zeigt die gültige Auswahl.

**Nach einer Änderung müssen Sie die nachfolgenden Rechenzellen erneut ausführen.** Beim ROI-Regler beginnen Sie mit der Zelle, die die Auswahl übernimmt. Bereits berechnete Zahlen ändern sich durch das Verschieben des Reglers allein noch nicht.

Die Regler funktionieren in einem laufenden Notebook. Eine reine Dateivorschau reicht dafür nicht aus.

## 4. Eigene Messdaten verwenden

Wechseln Sie erst beim Abschnitt **„Eigene Daten und kurze Diskussion“** zu Ihren eigenen Aufnahmen. Dort steht, welche Dateipfade und Auswahlfelder Sie ändern müssen. Legen Sie Ihre Exporte unter `daten/eigene/` ab und folgen Sie den Schritten im Notebook.

Falls keine eigenen Daten vorliegen, verwenden Sie die im Notebook vorgeschlagene zweite Beispielaufnahme auf derselben Schichtebene.

## 5. Ergebnisse abgeben

Die Speicherzellen im Notebook legen Ihre Abbildungen und Ergebnistabellen unter `ergebnisse/` ab. Führen Sie diese Zellen nach Ihrer endgültigen Auswahl erneut aus.

Prüfen Sie vor der Abgabe:

- Ihr bearbeitetes Notebook ist gespeichert; Ihre Abbildungen, Zahlen und Kurzantworten sind sichtbar.
- Aufnahme, tatsächliche Echozeiten sowie Wasser- und Öl-ROI sind dokumentiert.
- Zu beiden Signalanteilen haben Sie die jeweilige Wasser/Fett-Zuordnung und die Grenzen der Auswertung erläutert.
- Falls Sie die B₀-Aufgabe bearbeitet haben, sind auch deren Karten, Maske und Kennwerte enthalten.

Geben Sie **Ihr bearbeitetes Notebook und die zugehörigen PNG- und CSV-Dateien aus `ergebnisse/`** nach den Vorgaben der Betreuung ab.

## Wenn etwas nicht funktioniert

Bei einer Fehlermeldung prüfen Sie zuerst, ob Sie die vorherigen Zellen ausgeführt und die erforderlichen `...` ersetzt haben. Bei „Datei nicht gefunden“ kontrollieren Sie den Pfad und den gemeinsamen Ordner von Notebook, Hilfsdatei und Daten. Wenn Sie nicht weiterkommen, zeigen Sie der Betreuung die betroffene Zelle und die Fehlermeldung.
