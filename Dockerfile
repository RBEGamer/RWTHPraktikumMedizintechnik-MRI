ARG BASE_IMAGE=registry.git.rwth-aachen.de/jupyter/profiles/rwth-courses:latest
FROM ${BASE_IMAGE}

USER root

# Schriftunterstützung für die Matplotlib-Abbildungen im MRT-Praktikum.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libfontconfig1 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Die JupyterHub-Paketliste ergänzt die vorhandene RWTH-Arbeitsumgebung.
COPY notebook/requirements-jupyterhub.txt /srv/requirements.txt

# Bibliotheken und Kernelprofil für alle Benutzer des Images bereitstellen.
RUN python -m pip install --no-cache-dir -r /srv/requirements.txt \
    && python -m ipykernel install \
        --prefix=/usr/local \
        --name=mrt-praktikum \
        --display-name="Python 3 (MRT-Praktikum)"

USER ${NB_USER}

# Beim Image-Bau die Imports auch als späterer Notebook-Benutzer prüfen.
RUN MPLBACKEND=Agg python -c "import numpy, matplotlib.pyplot, pydicom, scipy.ndimage, skimage.restoration, ipywidgets; print('MRT-Bibliotheken verfügbar.')"
