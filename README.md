# Medizintechnik-Praktikum · Magnetresonanztomographie

Dieses Repository enthält die Unterlagen zum Versuch **Magnetresonanztomographie (MRT)** im Medizintechnik-Praktikum. Dazu gehören das Versuchsskript, eine bebilderte Scan-Anleitung, die vorbereitete Philips-ExamCard und ein Jupyter-Notebook mit DICOM-Beispieldaten zur Auswertung.

## Unterlagen

| Unterlage | Inhalt |
| --- | --- |
| [Versuchsskript](dokumentation/Versuchsskript/Versuchsskript.pdf) | Grundlagen und Aufgaben zum Versuch Magnetresonanztomographie. |
| [Scan-Anleitung (PDF)](dokumentation/Versuchsdurchfuehrung/Versuchsdurchfuehrung.pdf) | Versuchsaufbau, Bedienung des Scanners, Messablauf und DICOM-Export. Die [LaTeX-Quelle](dokumentation/Versuchsdurchfuehrung/Versuchsdurchfuehrung.tex) liegt im selben Ordner. |
| [Philips-ExamCard](dokumentation/MRSequenzExamCard/LfB_MR_Praktikum.ExamCard) | Vorbereitete Messsequenzen für das MRT-Praktikum. |
| [Jupyter-Notebook](notebook/experiment.ipynb) | Aufgaben zur einfachen Dixon-Auswertung und zur optionalen näherungsweisen B₀-Karte. |
| [DICOM-Beispieldaten](notebook/daten/beispiel/README.md) | Magnituden- und Phasenbilder einer gemeinsamen Schichtebene, jeweils mit und ohne Metallknopf. |

## Versuch und Auswertung

Im Praktikum untersuchen Sie unter anderem eine mit Wasser und Öl gefüllte Flasche. Sie planen die Aufnahmen, untersuchen den Einfluss von Messparametern und bestimmen den Frequenzabstand zwischen Wasser und Fett. Anschließend vergleichen Sie die Echos und werten die Wasser- und Ölbereiche im Notebook aus. Eine optionale Zusatzaufgabe behandelt die lokale Magnetfeldabweichung B₀.

## Einstieg

1. Lesen Sie das Versuchsskript zur Vorbereitung.
2. Verwenden Sie die Scan-Anleitung für die Durchführung der Messungen mit der Betreuung.
3. Öffnen Sie zur Auswertung das Jupyter-Notebook. Die [Startanleitung zum Notebook](notebook/README.md) erklärt die Bedienung und die Verwendung eigener Messdaten.

Für einen vorhandenen JupyterHub-Kernel verwenden Sie [notebook/requirements-jupyterhub.txt](notebook/requirements-jupyterhub.txt). Die [JupyterHub-Einrichtung](notebook/README.md#einmalige-vorbereitung-auf-jupyterhub) erklärt die einmalige Installation im Notebook. Die vollständige Paketliste für eine separat eingerichtete Arbeitsumgebung steht in [notebook/requirements.txt](notebook/requirements.txt).

Das Notebook benötigt die Hilfsdatei `mrt_hilfen.py` und den Unterordner `daten` neben sich; behalten Sie diese Ordnerstruktur beim Kopieren bei.

## Docker-Image für JupyterHub

Das [Dockerfile](Dockerfile) erweitert das RWTH-Image `rwth-courses` um die benötigten MRT-Bibliotheken aus [notebook/requirements-jupyterhub.txt](notebook/requirements-jupyterhub.txt). Es registriert den Kernel **Python 3 (MRT-Praktikum)** und prüft die Bibliotheksimporte beim Image-Bau.

Das Image aus dem Hauptordner dieses Repositorys bauen:

```bash
docker build -t mrt-praktikum .
```

Falls die RWTH-Registry den Abruf des Basis-Images mit `403 Forbidden` verweigert, melden Sie sich mit einem für dieses Image berechtigten Konto an und wiederholen Sie den Bau:

```bash
docker login registry.git.rwth-aachen.de
```

Ein anderes Basis-Image kann über `--build-arg BASE_IMAGE=...` gewählt werden. Für die Verwendung auf JupyterHub muss das gebaute Image in der vorgesehenen Registry bereitgestellt und als JupyterHub-Profil eingerichtet werden. Starten Sie anschließend einen Server mit diesem Profil und wählen Sie im Notebook **Python 3 (MRT-Praktikum)**. Die Unterlagen können Sie dort per Git klonen.
