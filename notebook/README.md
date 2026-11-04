# Jupyter-Notebook zum MRT-Praktikum

Sie untersuchen eine Wasser-/Ölflasche auf einer Schichtebene. Datenimport und Darstellung sind vorbereitet. Sie ergänzen vier Rechenschritte:

1. Die relative Phase zwischen OP- und IP-Echo berechnen.
2. Daraus ein Gesamtbild erzeugen: **Phase als Farbe, Magnitude als Helligkeit**.
3. Näherungsweise Wasser-/Fett-Signale und den Fett-Signalanteil **für jedes gültige Pixel** berechnen.
4. Aus der Phasendifferenz zwischen Echo 1 und Echo 3 der Triple-Echo-Aufnahme eine **B₀-Frequenzkarte in Hz** berechnen.

Die automatische Signalmaske legt für die Signalanteile fest, welche Pixel auswertbar sind. Die B₀-Karte zeigt die ganze Schicht **ohne Maske und ohne räumliches Entfalten**; der signalarme Hintergrund ist dort verrauscht. Es müssen keine Bildbereiche mit Reglern gewählt werden.

## Vorbereitung

Öffnen Sie [`experiment.ipynb`](experiment.ipynb) im Ordner `notebook/` mit einem Python-3-Kernel. Speichern Sie eine eigene Kopie **im selben Ordner**, beispielsweise `experiment_bearbeitet.ipynb`.

Ein Git-Klon enthält die Dateien, installiert aber noch keine Bibliotheken. Führen Sie bei Bedarf die erste Notebook-Zelle aus:

```python
%pip install -r requirements-jupyterhub.txt
```

Warten Sie das Ende der Installation ab. Starten Sie den Kernel neu und führen Sie danach die **Importzelle unter der Installationszelle** aus. Sind die Bibliotheken schon installiert, können Sie direkt mit den Importen beginnen.

Wenn das JupyterHub-Profil mit dem [Dockerfile dieses Repositorys](../Dockerfile) gebaut wurde, sind die Bibliotheken bereits vorhanden. Wählen Sie dann **Python 3 (MRT-Praktikum)**. Hinweise zum lokalen Container stehen in der [Repository-README](../README.md#how-to-run-the-coding-exercises-locally).

## Aufgaben bearbeiten

Arbeiten Sie von oben nach unten mit **Shift + Enter**. Nur die vier als Aufgaben markierten Rechenblöcke enthalten `...`. Ersetzen Sie alle Platzhalter im jeweiligen Block, bevor Sie ihn ausführen. Die Formeln und kurze Python-Hilfen stehen direkt darüber.

Die erste Aufnahme und die passenden Echos sind voreingestellt. Magnitude und Phase beider Echos werden in vier einzelnen Darstellungszellen geplottet. Nach einer Änderung der Echoauswahl müssen Sie die nachfolgenden Zellen erneut ausführen. Die Auswahlfelder funktionieren in einem laufenden Notebook, nicht in einer reinen Dateivorschau.

Für Kurzantworten doppelklicken Sie auf die Textzelle und schließen sie mit **Shift + Enter** ab. Speichern Sie regelmäßig mit **Strg + S / ⌘ + S**.

## Bilder richtig lesen

IP enthält Wasser- **und** Fettsignal. Die rote/blaue Farbe zeigt eine relative Phasenlage; sie ist noch kein gemessener Fettanteil. Erst die anschließende Modellrechnung verwendet zusätzlich beide Magnituden für eine pixelweise Prozentkarte.

Auch diese Prozentwerte sind **keine Stoffkonzentrationen oder exakten Volumenanteile**. Der vorgegebene globale Phasenbezug korrigiert keine räumlichen Feldunterschiede. Die Aufgaben erklären, woran Sie diese Grenzen erkennen.

Für die B₀-Karte sollte die chemische Phasendifferenz der äußeren Triple-Echos ungefähr null modulo 2π sein. Die zusätzliche gemessene Phasendifferenz liefert über den tatsächlichen Echoabstand die Frequenzabweichung. Ohne Entfalten bleiben die Werte modulo 1/ΔTE bestimmt; Sprünge können Phasenumbrüche sein. Diese einfache Frequenzkarte benötigt keine `phasenreferenz.json`.

## Eigene Daten

Laden Sie die DICOM-Dateien unter `daten/eigene/` hoch. Benötigt werden Magnitude und Phase beider Echos auf derselben Schichtebene. Ersetzen Sie in der Ladezelle den Datenordner, die Referenzdatei und die Aufnahme.

Für Ihre Messung benötigen Sie außerdem einen passenden globalen Phasenbezug von der Betreuung. Die Datei [`phasenreferenz.json`](daten/beispiel/phasenreferenz.json) gilt nur für die zugehörigen vier Beispielbilder. Ihr Bezug darf nicht auf andere Messungen übertragen werden; die Zuordnung wird beim Import geprüft.

Für B₀ werden zusätzlich die äußeren Phasenbilder Ihrer Triple-Echo-Aufnahme benötigt. Die Farbformel hängt nicht von der Bilddrehung ab. Folgen Sie den genauen Importhinweisen am Notebookende. Die [Dateiübersicht](daten/beispiel/README.md) erklärt die 20 mitgelieferten Beispielbilder.

## Abgabe und Musterlösung

Speichern Sie Ihr Notebook mit den sichtbaren Eingangsbildern, dem Farbbild, den Signalanteilkarten, der B₀-Frequenzkarte und Ihren drei Kurzantworten. Die Abbildungen und Zahlen bleiben direkt in den Zellenausgaben erhalten; geben Sie das gespeicherte Notebook ab.

[`experiment_loesung.ipynb`](experiment_loesung.ipynb) enthält die vollständige Musterlösung. Ihre **18 Codezellen** wurden mit den Beispieldaten unter Python 3.12 fehlerfrei ausgeführt. Die berechneten Ergebnisse und Abbildungen sind direkt im Lösungsnotebook sichtbar.

## Bei Fehlern

Prüfen Sie zuerst, ob alle vorherigen Zellen ausgeführt und alle `...` im aktuellen Aufgabenblock ersetzt wurden. Bei „Datei nicht gefunden“ kontrollieren Sie die Pfade; Notebook, `mrt_hilfen.py`, Datenordner und Referenzdatei müssen zusammen verfügbar sein. Bei einer unpassenden Phasenreferenz verwenden Sie die zur Messung gehörende Datei der Betreuung. Zeigen Sie bei weiteren Problemen die vollständige Fehlermeldung.
