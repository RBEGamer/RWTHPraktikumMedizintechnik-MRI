# Jupyter-Notebook zum MR-Praktikum

In diesem Praktikum untersuchen Sie eine mit Wasser und Öl gefüllte Flasche. Sie laden MRT-Bilder, vergleichen zwei Echos und werten einen Wasser- und einen Ölbereich aus. Alle Aufgaben beziehen sich auf **eine Schichtebene**. Die optionale Zusatzaufgabe behandelt die lokale Magnetfeldabweichung B₀.
Die benötigten Schritte werden im Notebook erklärt.

Die Scan-Anleitung zeigt, welche MRT-Aufnahmen Sie benötigen, wie Sie die gemeinsame Schichtebene planen und welche DICOM-Bilder Sie exportieren sollen.

## Musterlösung

[`experiment_loesung.ipynb`](experiment_loesung.ipynb) enthält die ausgefüllten Rechenwege, Kurzantworten und gespeicherten Ausgaben. Sie umfasst die Wasser-/Öl-Auswertung, den Vergleich mit Metallknopf und die optionale B₀-Karte. Alle **69 Codezellen** wurden mit den 20 mitgelieferten DICOM-Bildern unter Python 3.12 vollständig und ohne Ausführungsfehler getestet.

Die [Abbildungen und ROI-Tabellen](ergebnisse/loesung/) sowie der [Prüfbericht mit Paketversionen und Kennwerten](ergebnisse/loesung/pruefbericht.json) liegen separat unter `ergebnisse/loesung/`. Zum Wiederholen die Musterlösung im Ordner `notebook/` öffnen, bei Bedarf Schritt 0 ausführen und anschließend alle Zellen der Reihe nach starten. Die Zahlen in den Kurzantworten beziehen sich auf die voreingestellten Beispieldaten und ROIs.

## Einmalige Vorbereitung auf JupyterHub

Wenn Ihr JupyterHub-Profil mit dem [Dockerfile dieses Repositorys](../Dockerfile) gebaut wurde, sind die Bibliotheken bereits installiert. Wählen Sie **Python 3 (MRT-Praktikum)** und beginnen Sie mit Abschnitt 1. Das Bauen und Bereitstellen des Images ist in der [Repository-Übersicht](../README.md#how-to-run-the-coding-exercises-locally) beschrieben.

Ein Git-Klon enthält die Dateien, aber installiert die benötigten Python-Bibliotheken noch nicht. Öffnen Sie `experiment.ipynb` im Ordner `notebook/` und wählen Sie einen verfügbaren Python-3-Kernel. Der Name **Python 3 (MRT-Praktikum)** ist dafür nicht erforderlich.

Die erste Codezelle des Notebooks installiert die benötigten Bibliotheken. Führen Sie diese Zelle in Schritt 0 aus:

```python
%pip install -r requirements-jupyterhub.txt
```

Diese Paketliste enthält die Bibliotheken für die Auswertung. Die JupyterHub-Oberfläche und der bereits vorhandene Kernel werden darüber nicht neu installiert. `%pip` installiert in der Umgebung des aktuell ausgewählten Kernels ([IPython-Dokumentation](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip)).

Falls die zusätzliche Paketliste im bereits geklonten Stand noch fehlt, verwenden Sie direkt:

```python
%pip install numpy matplotlib pydicom scipy scikit-image ipywidgets
```

Warten Sie das Ende der Installation ab. Starten Sie anschließend über **Kernel → Restart Kernel…** den Kernel neu und fahren Sie mit **Schritt 1 · Eine DICOM-Datei laden** fort. Wenn die Bibliotheken bereits installiert sind, können Sie Schritt 0 überspringen.

Zum Prüfen der Installation können Sie eine Codezelle mit den folgenden Importen ausführen:

```python
import numpy, matplotlib, pydicom, scipy, skimage, ipywidgets
print("Bibliotheken sind verfügbar.")
```

Falls beim Installieren ein Fehler auftritt, halten Sie die vollständige Fehlermeldung sowie die Ausgabe von `import sys; print(sys.version)` fest. Falls die Imports funktionieren, aber die Regler nicht angezeigt werden, muss bei getrennten Server- und Kernel-Umgebungen gegebenenfalls die Widget-Unterstützung im JupyterHub durch die Betreuung eingerichtet werden ([Jupyter-Widgets-Dokumentation](https://ipywidgets.readthedocs.io/en/stable/user_install.html#installing-in-jupyterlab)).

## 1. Notebook öffnen

Die Arbeitsumgebung ist am Praktikumsrechner vorbereitet.

1. Öffnen Sie die bereitgestellte **JupyterLab-Umgebung** und wechseln Sie in Ihren Arbeitsordner.
2. Öffnen Sie dort **[`experiment.ipynb`](experiment.ipynb)** per Doppelklick.
3. Falls eine Kernel-Auswahl erscheint, wählen Sie den bereitgestellten **Python-3-Kernel**, gegebenenfalls **Python 3 (MRT-Praktikum)**. Der Kernel führt Ihre Codezellen aus.
4. Speichern Sie über **File → Save Notebook As…** eine eigene Fassung, beispielsweise `experiment3_bearbeitet.ipynb`, **im selben Ordner**.
5. Führen Sie bei Bedarf zuerst die Installationszelle in Schritt 0 aus. Starten Sie danach den Kernel neu und laden Sie in Schritt 1 das erste DICOM-Bild.

Der Ordner muss neben Ihrem Notebook die Datei `mrt_hilfen.py` und den Unterordner `daten` enthalten. Verschieben Sie das Notebook deshalb nicht einzeln. Wenn JupyterLab oder der passende Kernel fehlt, wenden Sie sich an die Betreuung.

Die 20 DICOM-Beispieldateien unter `daten/beispiel/` sind nach Objektzustand, Aufnahme, Echo und Bildtyp benannt. Die [Dateiübersicht](daten/beispiel/README.md) erklärt die Benennung und die Zuordnung zu den ursprünglichen Exportnamen.

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

Prüfen Sie vor der Abgabe:

- Ihr bearbeitetes Notebook ist gespeichert; Ihre Abbildungen, Zahlen und Kurzantworten sind sichtbar.
- Aufnahme, tatsächliche Echozeiten sowie Wasser- und Öl-ROI sind dokumentiert.
- Zu beiden Signalanteilen haben Sie die jeweilige Wasser/Fett-Zuordnung und die Grenzen der Auswertung erläutert.
- Falls Sie die B₀-Aufgabe bearbeitet haben, sind auch deren Karten, Maske und Kennwerte enthalten.


## Wenn etwas nicht funktioniert

Bei einer Fehlermeldung prüfen Sie zuerst, ob Sie die vorherigen Zellen ausgeführt und die erforderlichen `...` ersetzt haben. Bei „Datei nicht gefunden“ kontrollieren Sie den Pfad und den gemeinsamen Ordner von Notebook, Hilfsdatei und Daten. Wenn Sie nicht weiterkommen, zeigen Sie der Betreuung die betroffene Zelle und die Fehlermeldung.
