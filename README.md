Copyright (C) 2020 by RWTH Aachen University

[http://www.rwth-aachen.de](http://www.rwth-aachen.de)

License:

This software is dual-licensed under:

- Commercial license (please contact: [lfb@lfb.rwth-aachen.de](mailto:lfb@lfb.rwth-aachen.de))
- [AGPL (GNU Affero General Public License)](LICENSE.txt) open source license

# MRI Laboratory

Welcome to the Magnetic Resonance Imaging (MRI) experiment of the Medical Engineering Laboratory at the Institute of Imaging and Computer Vision, RWTH Aachen University.

This repository contains the course materials for the experiment, including the preparation script, an illustrated scan guide, a Philips ExamCard, and a Jupyter notebook with DICOM example data. The course materials and notebook instructions are provided in German.

During the experiment, you investigate a water/oil phantom, plan MRI acquisitions, explore imaging parameters, and determine the frequency difference between water and fat. In the notebook, you calculate a phase/magnitude colour blend, approximate water/fat signal fractions for each valid pixel, and a simple B₀ frequency map from the outer triple echoes.

Work through the preparation script before the laboratory session. Use the scan guide during the measurements, then practise the analysis with the [Jupyter notebook](notebook/experiment.ipynb).

## Course materials

| Material | Description |
| --- | --- |
| [Preparation script](dokumentation/Versuchsskript/Versuchsskript.pdf) | Background and exercises for the MRI experiment. |
| [Scan guide](dokumentation/Versuchsdurchfuehrung/Versuchsdurchfuehrung.pdf) | Scanner operation, acquisition planning, measurements, and DICOM export. The [LaTeX source](dokumentation/Versuchsdurchfuehrung/Versuchsdurchfuehrung.tex) is included. |
| [Philips ExamCard](dokumentation/MRSequenzExamCard/LfB_MR_Praktikum.ExamCard) | Prepared measurement sequences. |
| [Jupyter notebook](notebook/experiment.ipynb) | Phase/magnitude colour blend, pixelwise water/fat signal fractions, and a triple-echo B₀ frequency map. See the [notebook instructions](notebook/README.md) for details. |
| [DICOM example data](notebook/daten/beispiel/README.md) | Magnitude and phase images of one slice, with and without the metal button. |

## How to run the coding exercises locally?

The following commands use Bash syntax. Run them from the root directory of your local copy of this repository.

1. Install [Docker](https://www.docker.com/).

2. Clone this repository and open a terminal in its root directory.

3. Build the image for the MRI experiment using the included [Dockerfile](Dockerfile):

   ```bash
   docker build -t mrt-praktikum .
   ```

   The image installs the required libraries and registers the kernel **Python 3 (MRT-Praktikum)**. If the RWTH registry returns `403 Forbidden` when downloading the base image, sign in with an account authorised to access it and repeat the build:

   ```bash
   docker login registry.git.rwth-aachen.de
   ```

4. Start the container and mount your local repository so that your work is saved on your computer:

   ```bash
   docker run --rm -it --name mrt-praktikum \
     -p 127.0.0.1:8888:8888 \
     --mount "type=bind,source=$(pwd),target=/srv/mrt-praktikum" \
     --workdir /srv/mrt-praktikum \
     --entrypoint jupyter \
     mrt-praktikum lab --ip=0.0.0.0 --port=8888 --no-browser \
     --ServerApp.root_dir=/srv/mrt-praktikum
   ```

5. Open [http://localhost:8888](http://localhost:8888) in your browser. Follow the access instructions printed in the terminal; if a token is requested, use the token shown there. Open `notebook/experiment.ipynb`, select **Python 3 (MRT-Praktikum)**, and save your own working copy. Changes to files under the mounted repository are saved on your computer.

6. When you are finished, save your notebook and stop the container from another terminal:

   ```bash
   docker stop mrt-praktikum
   ```

   The container is removed after it stops; your files remain in the local repository folder.

**Note:** The local container workflow has not yet been verified with the RWTH base image because the registry denied the anonymous image download. Access to the base image is required to build it. The runtime options are documented in the [Docker reference](https://docs.docker.com/reference/cli/docker/container/run/).

## How to run the coding exercises on JupyterHub?

If your JupyterHub profile uses the image built from this repository, select **Python 3 (MRT-Praktikum)** and open the notebook. The image must first be built, published to the appropriate registry, and configured as a JupyterHub profile by the course administrators.

For an existing Python kernel, follow the [JupyterHub setup instructions](notebook/README.md#einmalige-vorbereitung-auf-jupyterhub). The required analysis libraries are listed in [notebook/requirements-jupyterhub.txt](notebook/requirements-jupyterhub.txt); [notebook/requirements.txt](notebook/requirements.txt) contains the full version-pinned environment list.

Keep `mrt_hilfen.py` and the `daten` directory next to the notebook when copying the materials.
