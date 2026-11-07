# Quiz zum MRT-Praktikum

Dreizehn Multiple-Choice-Fragen zur Selbstkontrolle: Fragen 1–5 beziehen sich auf das [Versuchsskript](../Versuchsskript/Versuchsskript.pdf), Fragen 6–10 auf die Python-Rechenschritte im [Jupyter-Notebook](../../notebook/experiment.ipynb), Frage 11 auf die B₀-Karte aus der Triple-Echo-Aufnahme und Fragen 12–13 auf die Bedienung des Scanners nach der [Versuchsdurchführung](../Versuchsdurchfuehrung/Versuchsdurchfuehrung.pdf). Pro Frage ist genau eine Antwort richtig.

## Teil 1: Physikalische Grundlagen und Dixon-Methode

### Frage 1: Larmorfrequenz

**Frage:** Welche Larmorfrequenz haben Wasserstoffkerne im 1,5-T-Scanner des Praktikums? (γ ≈ 42,58 MHz/T)

**Optionen:**

- A) 42,6 MHz
- B) 63,9 MHz
- C) 127,7 MHz
- D) 1,5 GHz

**Antwort:** B. ω₀ = γ · B₀ = 42,58 MHz/T · 1,5 T ≈ 63,9 MHz (Versuchsskript, Abschnitt 2.1).

### Frage 2: Chemische Verschiebung

**Frage:** Fett und Wasser haben eine chemische Verschiebung von etwa 3,5 ppm. Wie groß ist der Frequenzunterschied bei 1,5 T ungefähr?

**Optionen:**

- A) 22 Hz
- B) 220 Hz
- C) 440 Hz
- D) 3,5 kHz

**Antwort:** B. 3,5 · 10⁻⁶ · 63,9 MHz ≈ 224 Hz, also ≈ 220 Hz (Abschnitt 3.1).

### Frage 3: In-Phase und Out-of-Phase

**Frage:** Welche Aussage über die Magnitudenbilder im vereinfachten Dixon-Modell stimmt?

**Optionen:**

- A) Das In-Phase-Bild zeigt nur das Wassersignal.
- B) Im Out-of-Phase-Bild addieren sich Wasser und Fett zu W + F.
- C) Das In-Phase-Bild zeigt W + F, das Out-of-Phase-Bild |W − F|.
- D) Das Out-of-Phase-Signal ist immer größer als das In-Phase-Signal.

**Antwort:** C. Bei In-Phase addieren sich die Zeiger, bei Out-of-Phase zeigen sie in entgegengesetzte Richtungen (Abschnitt 3.2).

### Frage 4: 3-Punkt-Dixon

**Frage:** Warum trennt die 3-Punkt-Dixon-Methode Wasser und Fett robuster als die 2-Punkt-Methode?

**Optionen:**

- A) Mit drei Echos ist das Signal-Rausch-Verhältnis dreimal so hoch.
- B) Aus den zwei In-Phase-Bildern lässt sich die Hintergrundphase durch Feldinhomogenitäten berechnen und herausrechnen.
- C) Das dritte Echo unterdrückt das Fettsignal schon während der Aufnahme.
- D) Mit drei Echos kann es kein Phase Wrapping mehr geben.

**Antwort:** B. Δφ = ½ · arg(S₃ · S₁*). Phase Wrapping bleibt trotzdem ein Problem (Abschnitt 3.5).

### Frage 5: CSE-MRT und spektrale Fettsuppression

**Frage:** Welchen Vorteil hat die CSE-MRT (Dixon) gegenüber der spektralen Fettsuppression?

**Optionen:**

- A) Sie braucht nur eine einzige Echozeit.
- B) Sie unterdrückt das Fettsignal schon während der Aufnahme.
- C) Sie ist robuster gegenüber Magnetfeldinhomogenitäten, zum Beispiel in der Nähe von Metall.
- D) Sie kommt ohne Phaseninformation aus.

**Antwort:** C. Die spektrale Fettsuppression versagt bei starken Feldinhomogenitäten oft. Die CSE-MRT trennt Wasser und Fett erst bei der Nachverarbeitung (Abschnitt 1.2).

## Teil 2: Python im Notebook

### Frage 6: Rechnen mit Arrays

**Frage:** `ip` und `op` sind NumPy-Arrays mit je 512 × 512 Pixeln. Was berechnet `anteil_a = (ip + op) / 2`?

**Optionen:**

- A) Eine einzelne Zahl: den Mittelwert aller Pixel beider Bilder
- B) Ein neues 512 × 512-Array mit dem Mittelwert für jedes Pixel einzeln
- C) Einen Fehler, weil man Arrays nicht addieren kann
- D) Eine Liste mit 1024 Einträgen, weil beide Arrays aneinandergehängt werden

**Antwort:** B. NumPy rechnet elementweise: Jedes Pixel wird mit dem Pixel an derselben Stelle verrechnet, die Bildform bleibt erhalten.

### Frage 7: Phasendifferenz

**Frage:** Welcher Ausdruck führt eine Phasendifferenz zuverlässig auf den Bereich −π bis π zurück?

**Optionen:**

- A) `phase_op - phase_ip`
- B) `np.abs(phase_op - phase_ip)`
- C) `np.angle(np.exp(1j * (phase_op - phase_ip)))`
- D) `np.clip(phase_op - phase_ip, -np.pi, np.pi)`

**Antwort:** C. `exp(i·Δφ)` stellt den Winkel als Punkt auf dem Einheitskreis dar, dabei fallen volle Runden weg. `np.angle` liefert dann den Winkel zwischen −π und π. Variante D schneidet die Werte nur ab und verfälscht sie dadurch.

### Frage 8: Werte begrenzen

**Frage:** Was ergibt `np.clip(np.array([-0.2, 0.5, 1.7]), 0, 1)`?

**Optionen:**

- A) `[0.0, 0.5, 1.0]`
- B) `[-0.2, 0.5, 1.0]`
- C) `[0.2, 0.5, 1.7]`
- D) `[0.0, 0.5, 0.7]`

**Antwort:** A. Werte unter 0 werden zu 0, Werte über 1 werden zu 1, alles dazwischen bleibt gleich.

### Frage 9: Signalmaske

**Frage:** `maske` ist ein Array aus `True`/`False`. Was bewirkt `ip_signal = np.where(maske, ip, np.nan)`?

**Optionen:**

- A) Alle Pixel werden auf `NaN` gesetzt.
- B) Nur die Pixel, an denen `maske` den Wert `True` hat, bleiben übrig; das Array wird dadurch kleiner.
- C) Wo `maske` den Wert `True` hat, steht der IP-Wert, sonst `NaN`; das Array behält seine Form.
- D) Die Maske wird mit dem IP-Bild multipliziert.

**Antwort:** C. `np.where(Bedingung, x, y)` wählt pixelweise zwischen `x` und `y`. `NaN` bedeutet „kein auswertbarer Wert“; das Array hat danach immer noch die volle Bildform.

### Frage 10: Einheiten

**Frage:** Die Echozeit steht in Millisekunden in `TE_ms`, der Frequenzabstand in Hertz in `chemie_hz`. Wie berechnet man die Phasenverschiebung von Fett gegenüber Wasser in Grad richtig?

**Optionen:**

- A) `360 * chemie_hz * TE_ms`
- B) `360 * chemie_hz * TE_ms / 1000`
- C) `360 * chemie_hz / TE_ms`
- D) `360 * chemie_hz * TE_ms * 1000`

**Antwort:** B. Hz entspricht 1/s, also vollen Runden pro Sekunde. Deshalb rechnet man die Millisekunden zuerst in Sekunden um (÷ 1000) und multipliziert mit 360° pro Runde. Beispiel: 360 · 223,6 Hz · 13,8 ms / 1000 ≈ 1111° = 3 volle Runden + 31°, also nahezu IP.

## Teil 3: B₀-Karte

### Frage 11: Frequenzabweichung aus der Phasendifferenz

**Frage:** Für die B₀-Karte vergleichen Sie die Phasen von Echo 1 (TE = 9,2 ms) und Echo 3 (TE = 23,0 ms) der Triple-Echo-Aufnahme. In einem Pixel beträgt die Phasendifferenz Δφ = φ₃ − φ₁ = π/2 rad. Wie groß ist dort die Frequenzabweichung Δf = Δφ / (2π · ΔTE)?

**Optionen:**

- A) 0,018 Hz
- B) 18 Hz
- C) 36 Hz
- D) 114 Hz

**Antwort:** B. ΔTE = 23,0 ms − 9,2 ms = 13,8 ms = 0,0138 s. Damit ist Δf = (π/2) / (2π · 0,0138 s) = 1 / (4 · 0,0138 s) ≈ 18 Hz. Die anderen Optionen entstehen durch typische Fehler: A, wenn ΔTE in Millisekunden statt Sekunden eingesetzt wird; C, wenn der Faktor 2 fehlt; D, wenn der Faktor 2π ganz fehlt. Echo 1 und Echo 3 werden verwendet, weil Wasser und Fett bei beiden Echozeiten gleich zueinander stehen (chemische Phasenverschiebung ≈ ein Vielfaches von 360°). Die verbleibende Phasendifferenz stammt dann von der lokalen Feldabweichung.

## Teil 4: Bedienung am Scanner

### Frage 12: Kontrast im Bildbetrachter

**Frage:** Sie möchten im Bildbetrachter den Kontrast (die Fensterbreite) eines Bildes ändern. Wie gehen Sie vor?

**Optionen:**

- A) Mausrad über dem Bild drehen
- B) Mit gedrückter mittlerer Maustaste im Bild nach links oder rechts ziehen
- C) Mit gedrückter mittlerer und linker Maustaste im Bild ziehen
- D) Pfeiltasten links und rechts drücken

**Antwort:** B. Mit der mittleren Maustaste ändert Ziehen nach links/rechts den Kontrast (Fensterbreite) und Ziehen nach oben/unten die Helligkeit (Fenstermitte). Mittlere + linke Taste verschiebt den Bildausschnitt, die Pfeiltasten blättern durch die Schichten (Versuchsdurchführung, Abschnitt 14 FAQ).

### Frage 13: Minimale Echozeiten des Systems

**Frage:** Bevor Sie Ihre Echozeiten eintragen, wollen Sie wissen, welche kleinste erste Echozeit und welchen kleinsten Echoabstand der Scanner bei der aktuellen Auflösung erlaubt. Wo lesen Sie das ab?

**Optionen:**

- A) Im Reiter **Contrast** in der Zeile **TE first**
- B) Im Reiter **Info** in der Zeile **Min. TR/TE1/delta TE**
- C) Im Reiter **Conflicts**
- D) In der Kopfzeile des Survey-Bildes

**Antwort:** B. Der Reiter **Info** zeigt unter **Act. TR/TE1/delta TE** die tatsächlich umgesetzten Werte und unter **Min. TR/TE1/delta TE** die kleinsten erreichbaren Werte, im Beispiel 26 / 3,7 / 3,2 ms. Diese Grenzen sind hardwarebedingt und hängen von Auflösung und Bandbreite ab. Jede gewählte Echozeit muss mindestens der minimalen TE1 entsprechen, der Echoabstand mindestens dem minimalen delta TE (Versuchsdurchführung, Abschnitte 06 und 10). **Conflicts** meldet erst nachträglich unzulässige Einstellungen.
