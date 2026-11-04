"""Hilfen für ein MRT-Praktikum auf genau einer Schichtebene.

Die Dixon-, Hz- und ppm-Rechnungen stehen sichtbar im Notebook. Hier liegen
DICOM-Import, Auswahl, Darstellung, Maskenkontrolle und maskiertes Unwrapping.
"""
from pathlib import Path
from types import SimpleNamespace
from html import escape
import csv
import warnings
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import label
from skimage.restoration import unwrap_phase


def _fg(ds, frame, sequence):
    """Per-frame vor Shared Functional Groups; niemals Frame-Metadaten erraten."""
    for groups in (getattr(ds, 'PerFrameFunctionalGroupsSequence', []),
                   getattr(ds, 'SharedFunctionalGroupsSequence', [])):
        if not groups:
            continue
        item = groups[frame] if len(groups) > 1 else groups[0]
        seq = getattr(item, sequence, [])
        if seq:
            if sequence == 'RealWorldValueMappingSequence' and len(seq) != 1:
                raise ValueError('Mehrere Real-World-Mappings: eindeutige Auswahl erforderlich.')
            return seq[0]
    return ds


def _component(image_type, component=''):
    parts = {str(x).upper() for x in image_type}
    if 'FIELD_MAP' in parts or 'B0 MAP' in parts or 'B0' in parts:
        return 'FELDKARTE'
    if 'DERIVED' in parts:
        return 'ABGELEITET'
    if component == 'PHASE' or 'P' in parts or 'PHASE MAP' in parts:
        return 'PHASE'
    if component == 'MAGNITUDE' or 'M' in parts or 'M_FFE' in parts:
        return 'MAGNITUDE'
    return component or 'UNBEKANNT'


def _metadata(ds, path, frame=None):
    enhanced = frame is not None
    typ = _fg(ds, frame, 'MRImageFrameTypeSequence') if enhanced else ds
    image_type = getattr(typ, 'FrameType', getattr(ds, 'ImageType', []))
    kind = _component(image_type, str(getattr(typ, 'ComplexImageComponent', '')))
    pos = _fg(ds, frame, 'PlanePositionSequence') if enhanced else ds
    ori = _fg(ds, frame, 'PlaneOrientationSequence') if enhanced else ds
    pix = _fg(ds, frame, 'PixelMeasuresSequence') if enhanced else ds
    echo = _fg(ds, frame, 'MREchoSequence') if enhanced else ds
    te = getattr(echo, 'EffectiveEchoTime', getattr(echo, 'EchoTime', None))
    required = [(pos, 'ImagePositionPatient'), (ori, 'ImageOrientationPatient'),
                (pix, 'PixelSpacing'), (ds, 'StudyInstanceUID'), (ds, 'FrameOfReferenceUID')]
    for owner, key in required:
        if not hasattr(owner, key):
            raise ValueError(f'{path.name}: Pflichtmetadatum {key} fehlt.')
    if te is None or not np.isfinite(float(te)):
        raise ValueError(f'{path.name}: tatsächliche Echozeit fehlt oder ist ungültig.')
    acquisition = str(getattr(ds, 'AcquisitionNumber', ''))
    if not acquisition:
        # Konservativ: ohne Akquisitionsnummer keine verschiedenen Serien vereinigen.
        acquisition = 'Serie ' + str(ds.SeriesInstanceUID)
    description = str(getattr(ds, 'SeriesDescription', 'Ohne Beschreibung'))
    meta = dict(datei=str(path), frame=frame, komponente=kind, echozeit_ms=float(te),
                aufnahme=description, akquisition=acquisition,
                gruppe=(str(ds.StudyInstanceUID), str(ds.FrameOfReferenceUID), acquisition, description),
                position_mm=np.array(pos.ImagePositionPatient, float),
                orientierung=np.array(ori.ImageOrientationPatient, float),
                pixelabstand_mm=np.array(pix.PixelSpacing, float),
                form=(int(ds.Rows), int(ds.Columns)),
                referenz_mhz=float(getattr(ds, 'ImagingFrequency', np.nan)),
                schichtdicke_mm=float(getattr(pix, 'SliceThickness', np.nan)),
                referenzrahmen=str(ds.FrameOfReferenceUID))
    if not all(np.all(np.isfinite(meta[k])) for k in ['position_mm', 'orientierung', 'pixelabstand_mm']):
        raise ValueError('Nicht endliche Geometrieangaben.')
    if np.any(meta['pixelabstand_mm'] <= 0):
        raise ValueError('Pixelabstand muss positiv sein.')
    return meta


def gleiche_geometrie(a, b):
    """Matrix, Position, Orientierung, Pixelabstand und Referenzrahmen prüfen."""
    return (a['form'] == b['form'] and a['referenzrahmen'] == b['referenzrahmen']
            and all(np.allclose(a[k], b[k], atol=tol, rtol=0) for k, tol in
                    [('position_mm', 1e-3), ('orientierung', 1e-5), ('pixelabstand_mm', 1e-5)]))


def katalog(ordner, referenz=None):
    """Classic/Enhanced-MR einschließlich endungsloser Dateien inventarisieren.

    Mit referenz (Classic-Dataset) wird exakt dessen Ebene beibehalten. Ohne
    Referenz muss der Ordner eine einzige Geometrie enthalten. Es gibt keine
    automatische Registrierung und keine stillschweigende Wahl einer Schicht.
    """
    root = Path(ordner)
    if not root.is_dir():
        raise ValueError(f'Datenordner fehlt: {root}')
    records, errors = [], []
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.name == 'DICOMDIR':
            continue
        try:
            ds = pydicom.dcmread(path, defer_size=1024)
        except pydicom.errors.InvalidDicomError:
            continue
        if getattr(ds, 'Modality', '') != 'MR' or not hasattr(ds, 'Rows') or 'PixelData' not in ds:
            continue
        frames = range(int(ds.NumberOfFrames)) if hasattr(ds, 'NumberOfFrames') else [None]
        for frame in frames:
            try:
                rec = _metadata(ds, path, frame)
                if rec['komponente'] in {'MAGNITUDE', 'PHASE'}:
                    records.append(rec)
            except ValueError as exc:
                errors.append(str(exc))
    if errors:
        warnings.warn(f'{len(errors)} Bild(er) übersprungen: {errors[0]}', stacklevel=2)
    if referenz is not None:
        ref = _metadata(referenz, Path('Referenz'))
        records = [r for r in records if gleiche_geometrie(ref, r)]
    if not records:
        raise ValueError('Keine passenden MR-Echobilder auf der gewählten Ebene gefunden.')
    if any(not gleiche_geometrie(records[0], r) for r in records):
        raise ValueError('Mehrere Schichtebenen/Geometrien: zuerst eine Classic-Referenzdatei laden und referenz=dicom angeben.')
    return records


def uebersicht(records):
    """Nur technische Metadaten anzeigen; keine vollständigen DICOM-Header."""
    from IPython.display import HTML, display
    rows = []
    for r in records:
        position = ', '.join(f'{x:.2f}' for x in r['position_mm'])
        rows.append('<tr>' + ''.join(f'<td>{escape(str(x))}</td>' for x in
                    [Path(r['datei']).name, r['aufnahme'], r['akquisition'], r['komponente'],
                     r['echozeit_ms'], position]) + '</tr>')
    display(HTML('<table><tr><th>Datei</th><th>Aufnahme</th><th>Akq.</th><th>Typ</th>'
                 '<th>TE [ms]</th><th>Position [mm]</th></tr>' + ''.join(rows) + '</table>'))


def _scale(ds, pixels, frame, kind):
    """Eine physikalische Abbildung anwenden; RWVM hat Vorrang vor Rescale."""
    rw = _fg(ds, frame, 'RealWorldValueMappingSequence') if frame is not None else ds
    if frame is None and hasattr(ds, 'RealWorldValueMappingSequence'):
        if len(ds.RealWorldValueMappingSequence) != 1:
            raise ValueError('Mehrere Real-World-Mappings: eindeutige Auswahl erforderlich.')
        rw = ds.RealWorldValueMappingSequence[0]
    if hasattr(rw, 'RealWorldValueSlope'):
        slope, intercept = float(rw.RealWorldValueSlope), float(rw.RealWorldValueIntercept)
        unit = str(rw.MeasurementUnitsCodeSequence[0].CodeValue).lower()
    else:
        tr = _fg(ds, frame, 'PixelValueTransformationSequence') if frame is not None else ds
        if hasattr(tr, 'ModalityLUTSequence') or hasattr(rw, 'RealWorldValueLUTData'):
            raise ValueError('Nichtlineare Skalierung wird in dieser Lehrhilfe nicht unterstützt.')
        if hasattr(tr, 'RescaleSlope') != hasattr(tr, 'RescaleIntercept'):
            raise ValueError('Unvollständige Rescale-Skalierung.')
        slope, intercept = float(getattr(tr, 'RescaleSlope', 1)), float(getattr(tr, 'RescaleIntercept', 0))
        unit = str(getattr(tr, 'RescaleType', '')).lower()
    if not np.all(np.isfinite([slope, intercept])) or slope == 0:
        raise ValueError('Ungültige DICOM-Skalierung.')
    array = pixels.astype(np.float64) * slope + intercept
    if kind == 'PHASE':
        if unit == 'mrad':
            array /= 1000
        elif unit not in {'rad', 'radian', 'radians'}:
            raise ValueError(f'Unbekannte Phaseneinheit {unit!r}; keine Normierung auf ±π erraten.')
        unit = 'rad'
    else:
        unit = unit or 'a.u.'
    return array, unit


def lade(record):
    ds = pydicom.dcmread(record['datei'])
    pixels = ds.pixel_array
    if record['frame'] is not None:
        pixels = pixels[record['frame']]
    if pixels.ndim != 2:
        raise ValueError('Für das Praktikum ist genau ein 2D-Bild erforderlich.')
    data, unit = _scale(ds, pixels, record['frame'], record['komponente'])
    return data, dict(record, einheit=unit)


def echo_auswahl(records, aufnahme, modus='dixon'):
    """Echo-Paar interaktiv wählen, mit konservativer Prüfung bei lade_paar.

    Dixon: erstes Feld ist OP, zweites IP; B0: zwei Phasen aufsteigend nach TE.
    Die Voreinstellung ist ein Lehrvorschlag und keine automatische IP-Erkennung.
    """
    import ipywidgets as w
    from IPython.display import display
    kind = 'MAGNITUDE' if modus == 'dixon' else 'PHASE'
    options = {}
    for r in records:
        if r['komponente'] == kind:
            options[f"{r['aufnahme']} · Akq. {r['akquisition']}"] = r['gruppe']
    if not options:
        raise ValueError('Passendes Phasenpaar fehlt.' if kind == 'PHASE' else 'Magnitudenpaar fehlt.')
    default = next((g for label_, g in options.items() if label_.startswith(aufnahme + ' ·')), next(iter(options.values())))
    scan = w.Dropdown(options=list(options.items()), value=default, description='Aufnahme:', layout=w.Layout(width='650px'))
    first = w.Dropdown(description='OP:' if modus == 'dixon' else 'Phase 1:', layout=w.Layout(width='650px'))
    second = w.Dropdown(description='IP:' if modus == 'dixon' else 'Phase 2:', layout=w.Layout(width='650px'))
    def refresh(change=None):
        candidates = sorted([(i, r) for i, r in enumerate(records) if r['gruppe'] == scan.value and r['komponente'] == kind], key=lambda pair: pair[1]['echozeit_ms'])
        opts = [(f"TE {r['echozeit_ms']:g} ms · {Path(r['datei']).name}" + (f" · Frame {r['frame']}" if r['frame'] is not None else ''), i) for i, r in candidates]
        first.options = second.options = opts
        if opts:
            first.value, second.value = opts[0][1], opts[-1][1]
    scan.observe(refresh, names='value')
    refresh()
    display(w.VBox([scan, first, second, w.HTML('Echo-Zuordnung anhand des Messprotokolls prüfen. Nach jeder Änderung die nachfolgenden Zellen erneut ausführen.')]))
    return SimpleNamespace(records=records, scan=scan, first=first, second=second, modus=modus)


def lade_paar(auswahl):
    if auswahl.first.value is None or auswahl.second.value is None:
        raise ValueError('Zwei geeignete Echos auswählen.')
    a, b = (auswahl.records[box.value] for box in [auswahl.first, auswahl.second])
    if a['gruppe'] != b['gruppe'] or not gleiche_geometrie(a, b):
        raise ValueError('Echos gehören nicht zur gleichen Aufnahme und Schichtebene.')
    if a['echozeit_ms'] <= 0 or b['echozeit_ms'] <= 0 or a['echozeit_ms'] == b['echozeit_ms']:
        raise ValueError('Zwei unterschiedliche, positive Echozeiten erforderlich.')
    if auswahl.modus == 'b0':
        a, b = sorted([a, b], key=lambda r: r['echozeit_ms'])
        if not np.isfinite(a['referenz_mhz']) or a['referenz_mhz'] <= 0 or not np.isclose(a['referenz_mhz'], b['referenz_mhz'], rtol=1e-8):
            raise ValueError('Gleiche gültige Referenzfrequenz in beiden Phasenbildern erforderlich.')
    x, ma = lade(a)
    y, mb = lade(b)
    if ma['einheit'] != mb['einheit']:
        raise ValueError('Die Echos besitzen unterschiedliche Skalierungseinheiten.')
    print(f"{a['aufnahme']} | TE {a['echozeit_ms']:g} / {b['echozeit_ms']:g} ms | eine Ebene, {x.shape[0]} × {x.shape[1]} Pixel")
    return x, y, ma, mb


def magnitude_zu_phase(records, meta):
    found = [r for r in records if r['gruppe'] == meta['gruppe'] and r['komponente'] == 'MAGNITUDE'
             and np.isclose(r['echozeit_ms'], meta['echozeit_ms'], rtol=0, atol=1e-6)
             and gleiche_geometrie(r, meta)]
    if len(found) != 1:
        raise ValueError(f'Zur Phase wird genau eine passende Magnitude benötigt; gefunden: {len(found)}.')
    return lade(found[0])[0]


def phase_zu_magnitude(records, meta):
    """Genau die zur Magnitude gehörende exportierte Phase in rad laden."""
    found = [r for r in records if r['gruppe'] == meta['gruppe'] and r['komponente'] == 'PHASE'
             and np.isclose(r['echozeit_ms'], meta['echozeit_ms'], rtol=0, atol=1e-6)
             and gleiche_geometrie(r, meta)]
    if len(found) != 1:
        raise ValueError('Zur Magnitude wird genau eine passende Phase derselben Aufnahme, '
                         f'Ebene und Echozeit benötigt; gefunden: {len(found)}. '
                         'Die Phasenbilder beider Echos mit exportieren.')
    return lade(found[0])


def fenster(*images):
    """Gemeinsame robuste Darstellungsgrenze; verändert keine Rechendaten."""
    return (0., float(np.percentile(np.concatenate([a.ravel() for a in images]), 99)))


def _extent(meta, shape):
    dy, dx = meta['pixelabstand_mm']
    return (-dx / 2, (shape[1] - .5) * dx, (shape[0] - .5) * dy, -dy / 2)


def bild(data, titel, meta=None, grenzen=None, cmap='gray', ausschnitt=None):
    fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
    limits = {} if grenzen is None else dict(vmin=grenzen[0], vmax=grenzen[1])
    im = ax.imshow(data, cmap=cmap, extent=_extent(meta, data.shape) if meta else None, **limits)
    if np.ma.isMaskedArray(data):
        ax.set_facecolor('#e8edf2')
    if ausschnitt is not None:
        x0, x1, y0, y1 = ausschnitt
        ax.set_xlim(x0, x1)
        ax.set_ylim(y1, y0)
    ax.set(title=titel, xlabel='x in Schichtebene [mm]' if meta else 'Spalte [Pixel]', ylabel='y in Schichtebene [mm]' if meta else 'Zeile [Pixel]')
    fig.colorbar(im, ax=ax, shrink=.8)
    plt.show()
    return fig


def vierer(ip, op, gross, klein, meta_ip, meta_op):
    fig, axes = plt.subplots(2, 2, figsize=(10, 9), constrained_layout=True)
    lim = fenster(ip, op)
    for ax, data, title in zip(axes.ravel(), [ip, op, gross, klein],
                              [f"IP · TE {meta_ip['echozeit_ms']:g} ms", f"OP · TE {meta_op['echozeit_ms']:g} ms", 'Größerer Modellanteil A', 'Kleinerer Modellanteil B']):
        im = ax.imshow(data, cmap='gray', vmin=lim[0], vmax=lim[1], extent=_extent(meta_ip, data.shape))
        if title.startswith('Kleinerer'):
            ax.imshow(np.ma.masked_where(klein >= 0, np.ones_like(klein)), cmap=ListedColormap(['#ec5545']), alpha=.8, vmin=0, vmax=1, extent=_extent(meta_ip, data.shape))
        ax.set(title=title, xlabel='x [mm]', ylabel='y [mm]')
        fig.colorbar(im, ax=ax, shrink=.75, label='Signal [a.u.]')
    fig.suptitle('Gleiche Grauwertskala · Rot: B < 0 (Modellverletzung)', fontsize=12)
    plt.show()
    return fig


class ROI:
    """Rechteck mit exklusiver oberer Indexgrenze und Live-Vorschau."""
    def __init__(self, data, meta, signalmaske=None, start=(350, 410, 310, 360)):
        import ipywidgets as w
        from IPython.display import display
        from io import BytesIO
        self.data, self.meta = data, meta
        self.signalmaske = np.ones(data.shape, bool) if signalmaske is None else np.asarray(signalmaske, bool)
        if self.signalmaske.shape != data.shape:
            raise ValueError('Signalmaske und Bild müssen dieselbe Form besitzen.')
        h, width = data.shape
        # Standardrechteck ist an die Beispieldaten angepasst; für kleinere Bilder zentral starten.
        if not (0 <= start[0] < start[1] <= h and 0 <= start[2] < start[3] <= width):
            start = (h//3, 2*h//3, width//3, 2*width//3)
        self.y = w.IntRangeSlider(value=start[:2], min=0, max=h, description='Zeilen:', continuous_update=False, layout=w.Layout(width='600px'))
        self.x = w.IntRangeSlider(value=start[2:], min=0, max=width, description='Spalten:', continuous_update=False, layout=w.Layout(width='600px'))
        preview = w.Image(format='png', layout=w.Layout(max_width='600px'))
        def redraw(change=None):
            fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
            ax.imshow(data, cmap='gray', extent=_extent(meta, data.shape), vmin=0, vmax=fenster(data)[1])
            ax.imshow(np.ma.masked_where(~self.maske, np.ones_like(data)), cmap=ListedColormap(['#38bf78']), alpha=.4, vmin=0, vmax=1, extent=_extent(meta, data.shape))
            ax.set(title=f'ROI ∩ Signalmaske · {self.maske.sum()} Pixel', xlabel='x [mm]', ylabel='y [mm]')
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=100)
            preview.value = buffer.getvalue()
            plt.close(fig)
            self.figure = fig
        self.y.observe(redraw, names='value')
        self.x.observe(redraw, names='value')
        display(w.VBox([self.y, self.x, w.HTML('Grün = ausgewertete Fläche. Danach die Zelle mit roi = … und die folgenden Rechnungen erneut ausführen.'), preview]))
        redraw()

    @property
    def maske(self):
        mask = np.zeros(self.data.shape, bool)
        mask[self.y.value[0]:self.y.value[1], self.x.value[0]:self.x.value[1]] = True
        return mask & self.signalmaske

    @property
    def grenzen(self):
        return (*self.y.value, *self.x.value)


def roi_waehlen(data, meta, signalmaske=None, start=(350, 410, 310, 360)):
    return ROI(data, meta, signalmaske, start)


def pruefe_roi(mask, zusammenhaengend=False):
    if np.count_nonzero(mask) < 16:
        raise ValueError('ROI enthält weniger als 16 gültige Pixel. Rechteck oder Signalschwelle ändern.')
    components = label(mask)[1]
    if zusammenhaengend and components != 1:
        raise ValueError(f'ROI hat {components} getrennte Teile. Ein einziges zusammenhängendes Objektinnere wählen; Offsets sind sonst nicht vergleichbar.')
    print(f'{mask.sum()} gültige Pixel, {components} zusammenhängende(r) Bereich(e).')


def entfalte(wrapped, mask):
    """2D-Unwrapping nur innerhalb einer geprüften, zusammenhängenden ROI."""
    pruefe_roi(mask, zusammenhaengend=True)
    if not np.all(np.isfinite(wrapped[mask])):
        raise ValueError('Phasen innerhalb der Maske müssen endlich sein.')
    masked = np.ma.array(wrapped, mask=~mask)
    # rng hieß in älteren skimage-Versionen seed.
    import inspect
    keyword = 'rng' if 'rng' in inspect.signature(unwrap_phase).parameters else 'seed'
    result = unwrap_phase(masked, **{keyword: 0})
    return np.ma.filled(result, np.nan)


def phasenvergleich(wrapped, unfolded, mask, meta):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), constrained_layout=True)
    finite = unfolded[mask]
    lo, hi = min(-np.pi, float(finite.min())), max(np.pi, float(finite.max()))
    for ax, data, title in zip(axes, [wrapped, unfolded], ['Zirkuläre Differenz', 'Räumlich entfaltet (Offset offen)']):
        im = ax.imshow(np.ma.masked_where(~mask, data), cmap='twilight', vmin=lo, vmax=hi, extent=_extent(meta, data.shape))
        ax.set(title=title, xlabel='x [mm]', ylabel='y [mm]')
        fig.colorbar(im, ax=ax, label='rad')
    plt.show()
    return fig


def feldkarte(data, mask, meta, titel, grenze=.6):
    y, x = np.nonzero(mask)
    if len(y) == 0:
        raise ValueError('Feldkarte benötigt eine nicht leere Maske.')
    dy, dx = meta['pixelabstand_mm']
    # Die ganze Schicht ist in der ROI-Ansicht dokumentiert; hier ROI vergrößern.
    bounds = ((x.min()-10)*dx, (x.max()+10)*dx, (y.min()-10)*dy, (y.max()+10)*dy)
    return bild(np.ma.masked_where(~mask, data), titel, meta, (-grenze, grenze), 'RdBu_r', bounds)


def wasser_oel_phasenblend(ip, op, phase_ip, phase_op, meta, wasserreferenz):
    """IP/OP-Phasenlage als Farbgewicht, IP-Magnitude als Helligkeit.

    Eine bekannte Wasser-ROI setzt den globalen Phasenbezug. Es gibt keine
    Annahme über oben/unten und keine räumliche B0-Korrektur. Farbgewichte
    sind keine Stoff- oder Signalanteile einer Dixon-Rekonstruktion.
    """
    from matplotlib.patches import Patch

    ip, op, phase_ip, phase_op = (np.asarray(a, dtype=float) for a in
                                  (ip, op, phase_ip, phase_op))
    referenz = np.asarray(wasserreferenz, dtype=bool)
    if ip.ndim != 2 or any(a.shape != ip.shape for a in (op, phase_ip, phase_op, referenz)):
        raise ValueError('Magnituden, Phasen und Wasserreferenz müssen dieselbe 2D-Form besitzen.')
    endlich = np.isfinite(ip) & np.isfinite(op) & np.isfinite(phase_ip) & np.isfinite(phase_op)
    if not endlich.any():
        raise ValueError('Keine endlichen Bildwerte für den Phasenblend.')
    skala_ip, skala_op = (float(np.percentile(a[endlich], 99)) for a in (ip, op))
    if min(skala_ip, skala_op) <= 0:
        raise ValueError('Der Phasenblend benötigt Signal in beiden Echos.')
    signal_ip = np.isfinite(ip) & (ip > .15 * skala_ip)
    gueltig = endlich & signal_ip & (op > .15 * skala_op)
    referenz = referenz & gueltig
    if referenz.sum() < 16:
        raise ValueError('Wasserreferenz enthält weniger als 16 Pixel mit Signal in beiden Echos.')

    # Zirkulär mitteln: ein Sprung von +pi nach -pi darf den Bezug nicht ändern.
    phasor = np.zeros(ip.shape, dtype=complex)
    phasor[gueltig] = np.exp(1j * (phase_op[gueltig] - phase_ip[gueltig]))
    gewichte = (ip[referenz] / skala_ip) * (op[referenz] / skala_op)
    bezug = np.sum(gewichte * phasor[referenz]) / gewichte.sum()
    kohaerenz = float(abs(bezug))
    if kohaerenz < .5:
        raise ValueError('Phasen in der Wasserreferenz sind inkohärent. '
                         'Eine kleinere signalstarke Wasser-ROI wählen.')
    offset = float(np.angle(bezug))
    delta_phase = np.full(ip.shape, np.nan)
    delta_phase[gueltig] = np.angle(phasor[gueltig] * np.exp(-1j * offset))
    oelgewicht = (1 - np.cos(delta_phase)) / 2
    wassergewicht = 1 - oelgewicht

    # Nur die Darstellung wird auf [0, 1] begrenzt; keine Rechendaten verändern.
    helligkeit = np.zeros(ip.shape)
    helligkeit[signal_ip] = np.clip(ip[signal_ip] / skala_ip, 0, 1)
    rgb = np.zeros((*ip.shape, 3))
    rgb[..., 0][gueltig] = oelgewicht[gueltig] * helligkeit[gueltig]
    rgb[..., 2][gueltig] = wassergewicht[gueltig] * helligkeit[gueltig]
    grau = signal_ip & ~gueltig
    rgb[grau] = helligkeit[grau, None]

    fig, ax = plt.subplots(figsize=(7, 7.5), constrained_layout=True)
    extent = _extent(meta, ip.shape)
    ax.imshow(rgb, extent=extent, interpolation='nearest')
    dy, dx = meta['pixelabstand_mm']
    ax.contour(np.arange(ip.shape[1])*dx, np.arange(ip.shape[0])*dy,
               referenz.astype(float), levels=[.5], colors='white', linewidths=.8)
    ax.set(title='Öl rot · Wasser blau\nPhasenblend mit Magnitude als Helligkeit',
           xlabel='x in Schichtebene [mm]', ylabel='y in Schichtebene [mm]')
    ax.legend(handles=[Patch(color='red', label='öltypische Phasenlage'),
                       Patch(color='blue', label='wassertypische Phasenlage'),
                       Patch(color='.6', label='Phase nicht auswertbar'),
                       Patch(facecolor='none', edgecolor='black', label='Weißer Umriss: Wasserreferenz')],
              loc='upper center', bbox_to_anchor=(.5, -.11), ncol=2, frameon=False)
    fig.supxlabel('Farbe: relative IP/OP-Phase · Helligkeit: IP-Magnitude\n'
                  'Wasserreferenziert · keine räumliche B₀-Korrektur / Konzentrationskarte', fontsize=9)
    plt.show()
    return SimpleNamespace(figure=fig, rgb=rgb, delta_phase_rad=delta_phase,
                           oelgewicht=oelgewicht, wassergewicht=wassergewicht,
                           gueltig=gueltig, referenzmaske=referenz,
                           phasenoffset_rad=offset, referenz_kohaerenz=kohaerenz)


def speichere_bild(fig, name):
    path = Path('ergebnisse') / name
    path.parent.mkdir(exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches='tight')
    print(f'Gespeichert: {path}')


def protokoll(name, meta1, meta2, roi_box, **werte):
    """Eine CSV-Zeile mit Auswahl, ROI und frei benannten Kennwerten sichern."""
    row = dict(aufnahme=meta1['aufnahme'], datei_1=Path(meta1['datei']).name,
               datei_2=Path(meta2['datei']).name, te_1_ms=meta1['echozeit_ms'], te_2_ms=meta2['echozeit_ms'],
               referenz_mhz=meta1['referenz_mhz'], position_mm=';'.join(map(str, meta1['position_mm'])),
               roi_zeilen_spalten=str(roi_box.grenzen), pixel=int(roi_box.maske.sum()),
               flaeche_mm2=float(roi_box.maske.sum()*np.prod(meta1['pixelabstand_mm'])), **werte)
    path = Path('ergebnisse') / name
    path.parent.mkdir(exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)
    print(f'Gespeichert: {path}')
