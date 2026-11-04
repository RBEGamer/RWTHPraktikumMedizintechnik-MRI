# Eigene DICOM-Echos

Laden Sie hier Ihre Exporte hoch: Magnitude und Phase beider Echos auf derselben Schichtebene. Dateiendungen sind nicht erforderlich.

Ändern Sie im Abschnitt „Daten laden und verstehen“ den Datenordner auf `daten/eigene/`, den Dateipfad auf eine eigene Magnitudendatei und die Aufnahme auf Ihren Katalogeintrag. Die Referenzdatei legt die gemeinsame Schichtebene fest; mehrere Schichten im Export sind daher erlaubt. Prüfen Sie die tatsächlichen Echozeiten und die IP-/OP-Zuordnung anhand Ihres Messprotokolls.

Zusätzliche Phasenkalibrierdateien werden nicht benötigt. Die Farbansicht zeigt die gemessene Phasendifferenz in zwei neutralen Farben. Rot und Blau legen keine Wasser-/Öl-Zuordnung fest. Aus den Magnituden werden die Modellanteile A und B sowie der relative Anteil B berechnet.

Führen Sie nach dem Wechsel alle folgenden Zellen erneut aus. Die Signalmaske wird automatisch berechnet; gedrehte Flaschenbilder benötigen keine andere Farbformel.

Für die B₀-Frequenzkarte benötigen Sie außerdem die Phasenbilder der äußeren Triple-Echos derselben Aufnahme. Wählen Sie die Triple-Echo-Aufnahme im entsprechenden Notebook-Abschnitt und prüfen Sie den tatsächlichen Echoabstand sowie die chemische Gleichphasigkeit. Die B₀-Rechnung erfolgt ohne Maske.
