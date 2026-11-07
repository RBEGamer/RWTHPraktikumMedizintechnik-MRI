"""Hilfen für das MRT-Praktikum: Laden, Prüfen und Anzeigen.

Alle Formeln (chemische Phasenverschiebung, Phasendifferenz, Farbgewichte,
Signalanteile, B0-Frequenz) stehen sichtbar im Notebook. Dieses Modul lädt
die Dual- und Triple-Echo-Bilder mit festen Dateinamen, prüft, dass sie
zusammengehören, und zeichnet die Abbildungen.

Feste Dateinamen im Datenordner (PRAEFIX z. B. "wasser_oel"):
    <PRAEFIX>_dual_echo1_magnitude.dcm    <PRAEFIX>_dual_echo1_phase.dcm
    <PRAEFIX>_dual_echo2_magnitude.dcm    <PRAEFIX>_dual_echo2_phase.dcm
    <PRAEFIX>_triple_echo1_magnitude.dcm  <PRAEFIX>_triple_echo1_phase.dcm
    <PRAEFIX>_triple_echo2_magnitude.dcm  <PRAEFIX>_triple_echo2_phase.dcm
    <PRAEFIX>_triple_echo3_magnitude.dcm  <PRAEFIX>_triple_echo3_phase.dcm
Die Echos sind nach aufsteigender Echozeit nummeriert.
"""
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


# ----------------------------------------------------------------------------
# DICOM lesen
# ----------------------------------------------------------------------------

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
        raise ValueError(f'{path.name}: nicht endliche Geometrieangaben.')
    if np.any(meta['pixelabstand_mm'] <= 0):
        raise ValueError(f'{path.name}: Pixelabstand muss positiv sein.')
    return meta


def gleiche_geometrie(a, b):
    """Matrix, Position, Orientierung, Pixelabstand und Referenzrahmen prüfen."""
    return (a['form'] == b['form'] and a['referenzrahmen'] == b['referenzrahmen']
            and all(np.allclose(a[k], b[k], atol=tol, rtol=0) for k, tol in
                    [('position_mm', 1e-3), ('orientierung', 1e-5), ('pixelabstand_mm', 1e-5)]))


def _scale(ds, pixels, kind):
    """Eine physikalische Abbildung anwenden; RWVM hat Vorrang vor Rescale."""
    rw = ds
    if hasattr(ds, 'RealWorldValueMappingSequence'):
        if len(ds.RealWorldValueMappingSequence) != 1:
            raise ValueError('Mehrere Real-World-Mappings: eindeutige Auswahl erforderlich.')
        rw = ds.RealWorldValueMappingSequence[0]
    if hasattr(rw, 'RealWorldValueSlope'):
        slope, intercept = float(rw.RealWorldValueSlope), float(rw.RealWorldValueIntercept)
        unit = str(rw.MeasurementUnitsCodeSequence[0].CodeValue).lower()
    else:
        if hasattr(ds, 'ModalityLUTSequence') or hasattr(rw, 'RealWorldValueLUTData'):
            raise ValueError('Nichtlineare Skalierung wird in dieser Lehrhilfe nicht unterstützt.')
        if hasattr(ds, 'RescaleSlope') != hasattr(ds, 'RescaleIntercept'):
            raise ValueError('Unvollständige Rescale-Skalierung.')
        slope, intercept = float(getattr(ds, 'RescaleSlope', 1)), float(getattr(ds, 'RescaleIntercept', 0))
        unit = str(getattr(ds, 'RescaleType', '')).lower()
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


def lade_bild(pfad, komponente):
    """Ein 2D-Bild laden; komponente ist 'MAGNITUDE' oder 'PHASE' (Phase in rad)."""
    pfad = Path(pfad)
    if not pfad.is_file():
        raise FileNotFoundError(f'Datei nicht gefunden: {pfad}')
    ds = pydicom.dcmread(pfad)
    if hasattr(ds, 'NumberOfFrames') and int(ds.NumberOfFrames) > 1:
        raise ValueError(f'{pfad.name}: Enhanced-DICOM mit mehreren Bildern. Bitte als Classic DICOM exportieren.')
    meta = _metadata(ds, pfad)
    if meta['komponente'] != komponente:
        raise ValueError(f'{pfad.name}: erwartet {komponente}, gefunden {meta["komponente"]}. '
                         'Dateinamen und Bildtyp prüfen.')
    pixels = ds.pixel_array
    if pixels.ndim != 2:
        raise ValueError(f'{pfad.name}: Für das Praktikum ist genau ein 2D-Bild erforderlich.')
    data, unit = _scale(ds, pixels, komponente)
    return data, dict(meta, einheit=unit)


def lade_echos(ordner, praefix, aufnahme, anzahl):
    """Magnitude und Phase aller Echos einer Aufnahme mit festen Dateinamen laden.

    aufnahme: 'dual_echo' (anzahl=2) oder 'triple_echo' (anzahl=3).
    Rückgabe mit den Feldern magnitude, phase, te_ms, meta (je eine Liste,
    Index 0 = Echo 1) und f0_mhz (Scannerfrequenz in MHz).
    """
    ordner = Path(ordner)
    magnitude, phase, meta = [], [], []
    for k in range(1, anzahl + 1):
        m, mm = lade_bild(ordner / f'{praefix}_{aufnahme}{k}_magnitude.dcm', 'MAGNITUDE')
        p, mp = lade_bild(ordner / f'{praefix}_{aufnahme}{k}_phase.dcm', 'PHASE')
        if not np.isclose(mm['echozeit_ms'], mp['echozeit_ms'], rtol=0, atol=1e-6):
            raise ValueError(f'Echo {k}: Magnitude und Phase haben verschiedene Echozeiten.')
        magnitude.append(m)
        phase.append(p)
        meta.append(mm)
    alle = meta
    for mm in alle[1:]:
        if mm['gruppe'] != alle[0]['gruppe'] or not gleiche_geometrie(mm, alle[0]):
            raise ValueError('Die Echos stammen nicht aus derselben Aufnahme und Schichtebene.')
    te_ms = [mm['echozeit_ms'] for mm in meta]
    if te_ms[0] <= 0 or any(b <= a for a, b in zip(te_ms, te_ms[1:])):
        raise ValueError(f'Echozeiten müssen positiv und aufsteigend nummeriert sein: {te_ms} ms.')
    f0 = meta[0]['referenz_mhz']
    if not np.isfinite(f0) or f0 <= 0:
        raise ValueError('Scannerfrequenz (ImagingFrequency) fehlt in den DICOM-Daten.')
    print(f"{meta[0]['aufnahme']} | {anzahl} Echos | TE = "
          + ' / '.join(f'{t:g}' for t in te_ms) + f" ms | {magnitude[0].shape[0]} × "
          f"{magnitude[0].shape[1]} Pixel | Ordner {ordner}")
    return SimpleNamespace(magnitude=magnitude, phase=phase, te_ms=te_ms, meta=meta, f0_mhz=f0)


def dateiliste(ordner):
    """Alle DICOM-Bilder eines Ordners mit Aufnahme, Bildtyp und TE auflisten.

    Hilft beim Umbenennen eigener Exporte in die festen Dateinamen.
    """
    zeilen = []
    for path in sorted(Path(ordner).rglob('*')):
        if not path.is_file():
            continue
        try:
            ds = pydicom.dcmread(path, stop_before_pixels=True)
            meta = _metadata(ds, path)
        except Exception:
            continue
        zeilen.append((str(path.relative_to(ordner)), meta['aufnahme'], meta['komponente'],
                       meta['echozeit_ms'], meta['position_mm'][2]))
    if not zeilen:
        print(f'Keine lesbaren DICOM-Bilder in {ordner}.')
        return
    print(f"{'Datei':40s} {'Aufnahme':28s} {'Typ':10s} {'TE [ms]':>8s} {'z [mm]':>8s}")
    for z in zeilen:
        print(f'{z[0]:40s} {z[1]:28s} {z[2]:10s} {z[3]:8.3f} {z[4]:8.2f}')


# ----------------------------------------------------------------------------
# Vorbereitete Schritte, die keine Aufgabe sind
# ----------------------------------------------------------------------------

def ip_op_zuordnen(dual, phase_cs_1_grad, phase_cs_2_grad):
    """IP- und OP-Echo anhand der chemischen Phasenverschiebung in Grad zuordnen.

    Von jeder Phasenverschiebung werden alle vollen Runden (360°) abgezogen.
    Das Echo mit dem Restwinkel näher an 0° ist IP, das andere OP.
    Rückgabe: ip, op [a.u.], phase_ip, phase_op [rad], meta_ip, meta_op.
    """
    winkel = (phase_cs_1_grad, phase_cs_2_grad)
    rest = [w % 360 for w in winkel]                    # Restwinkel 0 bis 360 [°]
    abstand_0 = [min(r, 360 - r) for r in rest]          # Abstand zu 0° bzw. 360° [°]
    i_ip = 0 if abstand_0[0] < abstand_0[1] else 1
    i_op = 1 - i_ip
    for i, name in ((i_ip, 'IP (Restwinkel nahe 0°)'), (i_op, 'OP (Restwinkel nahe 180°)')):
        print(f'Echo {i + 1}: TE {dual.te_ms[i]:g} ms, Phasenverschiebung {winkel[i]:.0f}° '
              f'= {int(winkel[i] // 360)} volle Runde(n) + {rest[i]:.0f}° → {name}')
    if abstand_0[i_ip] > 72 or abs(abstand_0[i_op] - 180) > 72:
        print('Hinweis: Die Echos sind nur grob IP/OP. Rechnung und Echozeiten prüfen.')
    return (dual.magnitude[i_ip], dual.magnitude[i_op], dual.phase[i_ip], dual.phase[i_op],
            dual.meta[i_ip], dual.meta[i_op])


def signalmaske(ip, op, phase_ip, phase_op, schwelle=0.15):
    """Pixel mit genügend Signal in beiden Echos (Anteil des 99. Perzentils).

    Rückgabe: maske (beide Echos gültig) und signal_ip (nur IP-Signal).
    """
    signal_ip = np.isfinite(ip) & (ip > schwelle * np.percentile(ip, 99))
    maske = (signal_ip & np.isfinite(op) & np.isfinite(phase_ip) & np.isfinite(phase_op)
             & (op > schwelle * np.percentile(op, 99)))
    if not maske.any():
        raise ValueError('Kein gemeinsamer signalstarker Bereich in beiden Echos.')
    print(f'Auswertbare Pixel: {int(maske.sum())} von {maske.size}')
    return maske, signal_ip


def fenster(*images):
    """Gemeinsame robuste Darstellungsgrenze (99. Perzentil); ändert keine Daten."""
    return (0., float(np.nanpercentile(np.concatenate([a.ravel() for a in images]), 99)))


# ----------------------------------------------------------------------------
# Darstellung
# ----------------------------------------------------------------------------

def _extent(meta, shape):
    dy, dx = meta['pixelabstand_mm']
    return (-dx / 2, (shape[1] - .5) * dx, (shape[0] - .5) * dy, -dy / 2)


def bild(data, titel, meta=None, grenzen=None, cmap='gray'):
    fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
    limits = {} if grenzen is None else dict(vmin=grenzen[0], vmax=grenzen[1])
    im = ax.imshow(data, cmap=cmap, extent=_extent(meta, data.shape) if meta else None, **limits)
    ax.set(title=titel, xlabel='x in Schichtebene [mm]' if meta else 'Spalte [Pixel]',
           ylabel='y in Schichtebene [mm]' if meta else 'Zeile [Pixel]')
    fig.colorbar(im, ax=ax, shrink=.8)
    plt.show()
    return fig


def eingangsbilder(echos, titel):
    """Oben die Magnituden (gemeinsame Grauwertskala), unten die Phasen in rad."""
    n = len(echos.magnitude)
    fig, axes = plt.subplots(2, n, figsize=(4.6 * n, 8.4), constrained_layout=True, squeeze=False)
    lim = fenster(*echos.magnitude)[1]
    ext = _extent(echos.meta[0], echos.magnitude[0].shape)
    for k in range(n):
        te = echos.te_ms[k]
        im_m = axes[0, k].imshow(echos.magnitude[k], cmap='gray', vmin=0, vmax=lim, extent=ext)
        axes[0, k].set(title=f'Echo {k + 1} · TE {te:g} ms · Magnitude', xlabel='x [mm]', ylabel='y [mm]')
        im_p = axes[1, k].imshow(echos.phase[k], cmap='twilight', vmin=-np.pi, vmax=np.pi, extent=ext)
        axes[1, k].set(title=f'Echo {k + 1} · TE {te:g} ms · Phase', xlabel='x [mm]', ylabel='y [mm]')
    fig.colorbar(im_m, ax=axes[0, :], shrink=.8, label='Signal [a.u.]')
    fig.colorbar(im_p, ax=axes[1, :], shrink=.8, label='Phase [rad]')
    fig.suptitle(f'{titel}: gleiche Grauwertskala für alle Magnituden, Phasen von −π bis π', fontsize=12)
    plt.show()
    return fig


def farbbild_anzeigen(rot, blau, helligkeit, maske, signal_ip, meta):
    """Aus den im Notebook berechneten Kanälen ein RGB-Bild bauen und zeigen.

    Pixel ohne gültige Phase, aber mit IP-Signal werden grau, Hintergrund schwarz.
    Rückgabe: das RGB-Bild (Zeilen × Spalten × 3, Werte 0 bis 1).
    """
    rgb = np.stack((rot, np.zeros_like(rot), blau), axis=-1)
    rgb[~maske] = 0
    grau = signal_ip & ~maske
    rgb[grau] = np.asarray(helligkeit)[grau, None]
    fig, ax = plt.subplots(figsize=(7, 7.2), constrained_layout=True)
    ax.imshow(rgb, extent=_extent(meta, rgb.shape[:2]), interpolation='nearest')
    ax.set(title='Phase als Farbe · Magnitude als Helligkeit',
           xlabel='x in Schichtebene [mm]', ylabel='y in Schichtebene [mm]')
    ax.legend(handles=[Patch(color='red', label='Phasendifferenz nahe ±π'),
                       Patch(color='blue', label='Phasendifferenz nahe 0'),
                       Patch(color='.6', label='Phase nicht auswertbar')],
              loc='upper center', bbox_to_anchor=(.5, -.11), ncol=2, frameon=False)
    fig.supxlabel('Farbe: gemessene Phasenlage · Helligkeit: IP-Magnitude\n'
                  'Rot und Blau haben keine feste Wasser-/Öl-Bedeutung', fontsize=9)
    plt.show()
    return rgb


def signalanteile_anzeigen(anteil_a, anteil_b, b_prozent, maske, meta):
    """Berechnete Modellanteile und pixelweise Prozentkarte zeigen; keine Trennung."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5), constrained_layout=True)
    lim = fenster(anteil_a[maske], anteil_b[maske])[1]
    for ax, data, title, cmap, vmax in zip(
            axes, [anteil_a, anteil_b, b_prozent],
            ['Größerer Modellanteil A', 'Kleinerer Modellanteil B', 'Signalanteil B [%]'],
            ['Blues', 'Reds', 'viridis'], [lim, lim, 50]):
        ax.set_facecolor('#e8edf2')
        im = ax.imshow(np.ma.masked_where(~maske, data), cmap=cmap, vmin=0, vmax=vmax,
                       extent=_extent(meta, data.shape))
        prozentkarte = ax is axes[2]
        kritisch = maske & ((data < 0) | (data > 50)) if prozentkarte else maske & (data < 0)
        ax.imshow(np.ma.masked_where(~kritisch, np.ones_like(data)),
                  cmap=ListedColormap(['#f4a340']), vmin=0, vmax=1,
                  extent=_extent(meta, data.shape))
        ax.set(title=title, xlabel='x [mm]', ylabel='y [mm]')
        fig.colorbar(im, ax=ax, shrink=.75, label='%' if prozentkarte else 'Signal [a.u.]')
    fig.legend(handles=[Patch(color='#f4a340', label='Orange: Modellgrenze verletzt'),
                        Patch(color='#e8edf2', label='Hellgrau: nicht ausgewertet')],
               loc='outside lower center', ncol=2, frameon=False)
    fig.suptitle('Modellanteile A und B · Wasser-/Fett-Zuordnung offen', fontsize=13)
    plt.show()
    return fig


def b0_anzeigen(b0_hz, delta_te_s, meta):
    """B0-Frequenzkarte ohne Maske im eindeutigen Bereich ±1/(2 ΔTE) zeigen."""
    grenze = 1 / (2 * delta_te_s)
    return bild(b0_hz, 'B₀: Frequenzabweichung [Hz] · ohne Maske / ohne Entfalten',
                meta, (-grenze, grenze), 'RdBu_r')
