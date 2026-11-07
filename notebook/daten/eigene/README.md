# Eigene DICOM-Echos

Laden Sie hier Ihre Exporte hoch. Benötigt werden nur **Einzelbilder einer Schicht**: die Bilder der Dual-Echo- und der Triple-Echo-Aufnahme, jeweils Magnitude und Phase je Echo.

Führen Sie im Notebook `mh.dateiliste("daten/eigene")` aus. Die Liste zeigt für jede Datei Aufnahme, Bildtyp, Echozeit und Schichtposition. Benennen Sie die zehn Dateien Ihrer gewählten Schicht danach mit festen Namen um; Echo 1 ist jeweils das Echo mit der kürzesten Echozeit:

```
eigene_dual_echo1_magnitude.dcm    eigene_dual_echo1_phase.dcm
eigene_dual_echo2_magnitude.dcm    eigene_dual_echo2_phase.dcm
eigene_triple_echo1_magnitude.dcm  eigene_triple_echo1_phase.dcm
eigene_triple_echo2_magnitude.dcm  eigene_triple_echo2_phase.dcm
eigene_triple_echo3_magnitude.dcm  eigene_triple_echo3_phase.dcm
```

Setzen Sie anschließend in der Ladezelle `DATENORDNER = "daten/eigene"` und `PRAEFIX = "eigene"` und führen Sie alle Zellen erneut aus. Die Hilfsdatei prüft, dass alle Bilder zur selben Aufnahme und Schichtebene gehören.
