# Eigene DICOM-Echos

Laden Sie hier Ihre Exporte hoch: Magnitude und Phase beider Echos auf derselben Schichtebene. Dateiendungen sind nicht erforderlich.

Ändern Sie im Abschnitt „Daten laden und verstehen“ den Datenordner auf `daten/eigene/`, den Dateipfad auf eine eigene Magnitudendatei und die Aufnahme auf Ihren Katalogeintrag. Die Referenzdatei legt die gemeinsame Schichtebene fest; mehrere Schichten im Export sind daher erlaubt. Prüfen Sie die tatsächlichen Echozeiten und die IP-/OP-Zuordnung anhand Ihres Messprotokolls.

Verwenden Sie außerdem die zu Ihrer Messung gehörende `phasenreferenz.json` von der Betreuung. Sie enthält den globalen Phasenbezug sowie die Dateizuordnung. Der Phasenbezug der Beispieldaten darf nicht für andere Messungen verwendet werden. Änderungen von Feld oder Frequenzeinstellung können die Phasenreferenz verändern; eine Bilddrehung allein ändert die Farbformel nicht.

Führen Sie nach dem Wechsel alle folgenden Zellen erneut aus. Die Signalmaske wird automatisch berechnet; die Aufgaben sind der Phasen-Magnitude-Blend und die Signalanteile für jedes gültige Pixel.

Für die B₀-Frequenzkarte benötigen Sie außerdem die Phasenbilder der äußeren Triple-Echos derselben Aufnahme. Wählen Sie die Triple-Echo-Aufnahme im entsprechenden Notebook-Abschnitt und prüfen Sie den tatsächlichen Echoabstand sowie die chemische Gleichphasigkeit. Die B₀-Rechnung erfolgt ohne Maske und benötigt keinen globalen Phasenbezug aus der JSON-Datei.
