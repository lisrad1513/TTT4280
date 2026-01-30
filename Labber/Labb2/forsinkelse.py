import numpy as np

def finn_forsinkelse(x, y, fs, bruk_abs=True, dc_fjern=True):
    """
    Finner tidsforsinkelse mellom to signaler x og y ved hjelp av krysskorrelasjon.

    Denne funksjonen er laget slik at fortegnet på forsinkelsen følger kompendiets definisjon:
        r_xy(m) = sum_n x(n) * y(n + m)

    Tolkning:
    Hvis y er x forskjøvet til høyre (y kommer senere), får du typisk en positiv forsinkelse (m > 0).

    Parametre:
    x, y      : 1D arrays (samme eller ulik lengde)
    fs        : samplingsfrekvens [Hz]
    bruk_abs  : hvis True finner maksimum av |rxy|, hvis False finner maksimum av rxy
    dc_fjern  : hvis True fjernes DC (middelverdi) fra begge signaler

    Returnerer:
    m_delay : forsinkelse i antall sampler (kompendiets m)
    tau     : forsinkelse i sekunder
    rxy     : krysskorrelasjonsfunksjonen (full)
    lags_m  : lag-akse i sampler, uttrykt som kompendiets m
    """

    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x og y må være 1D-arrays")

    if fs <= 0:
        raise ValueError("fs må være > 0")

    if dc_fjern:
        x = x - np.mean(x)
        y = y - np.mean(y)

    # NumPy sin korrelasjon har motsatt fortegnkonvensjon i forhold til kompendiet.
    # Derfor bruker vi xcorr = correlate(x, y), og konverterer k-lags til kompendiets m ved m = -k.
    rxy = np.correlate(x, y, mode="full")

    # Lags for numpy-correlate(x,y): k går fra -(len(y)-1) til (len(x)-1)
    lags_k = np.arange(-len(y) + 1, len(x))

    # Konverter til kompendiets m
    lags_m = -lags_k

    # Finn indeks for topp
    if bruk_abs:
        idx = int(np.argmax(np.abs(rxy)))
    else:
        idx = int(np.argmax(rxy))

    m_delay = int(lags_m[idx])
    tau = m_delay / fs

    return m_delay, tau, rxy, lags_m


def finn_forsinkelse_med_oppampling(x, y, fs, L=16, vindu=20, bruk_abs=True, dc_fjern=True):
    """
    Som finn_forsinkelse, men forbedrer oppløsningen rundt toppen ved å oppsample rxy lokalt.

    Idé:
    1) Finn grov topp (heltalls-lag)
    2) Ta et lite vindu rundt toppen
    3) Oppsample dette vinduet med lineær interpolasjon med faktor L
    4) Finn topp i oppsamplet versjon for brøkdels-lag

    Parametre:
    L      : oppsamlingsfaktor (for eksempel 16)
    vindu  : antall heltalls-samples på hver side av toppen som tas med

    Returnerer:
    m_delay_frac : forsinkelse i sampler (kan være brøk)
    tau_frac     : forsinkelse i sekunder
    rxy          : original rxy (full)
    lags_m       : original lags-akse (kompendiets m)
    """

    m_delay_int, tau_int, rxy, lags_m = finn_forsinkelse(
        x, y, fs, bruk_abs=bruk_abs, dc_fjern=dc_fjern
    )

    # Finn hvor toppen ligger i rxy-indekser
    if bruk_abs:
        idx0 = int(np.argmax(np.abs(rxy)))
    else:
        idx0 = int(np.argmax(rxy))

    # Velg vindu rundt toppen (i indeksdomene)
    i0 = max(0, idx0 - vindu)
    i1 = min(len(rxy) - 1, idx0 + vindu)

    r_seg = rxy[i0:i1 + 1]
    m_seg = lags_m[i0:i1 + 1].astype(np.float64)

    # Oppsample med lineær interpolasjon
    n_fine = (len(r_seg) - 1) * L + 1
    m_fine = np.linspace(m_seg[0], m_seg[-1], n_fine)
    r_fine = np.interp(m_fine, m_seg, r_seg)

    # Finn topp i oppsamplet segment
    if bruk_abs:
        j = int(np.argmax(np.abs(r_fine)))
    else:
        j = int(np.argmax(r_fine))

    m_delay_frac = float(m_fine[j])
    tau_frac = m_delay_frac / fs

    return m_delay_frac, tau_frac, rxy, lags_m

def finn_forsinkelse_test(x, y, fs, min_samples = 10, max_samples = 10):
    r_xy = []
    for delay in range(-min_samples, max_samples + 1):
        if delay < 0:
            shifted_y = np.concatenate((y[-delay:], np.zeros(-delay)))
        elif delay > 0:
            shifted_y = np.concatenate((np.zeros(delay), y[:-delay]))
        else:
            shifted_y = y

        r = np.sum(x * shifted_y)
        r_xy.append(r)

        m_delay = np.max(r_xy)
    return np.array(r_xy), m_delay, m_delay/fs 



if __name__ == "__main__":
    # Mini-demo for å sanity-sjekke fortegn og verdi
    fs = 4000.0
    N = 200
    t = np.arange(N) / fs

    # Et "pulsaktig" signal
    x = np.exp(-((t - 0.02) / 0.003) ** 2)

    # Lag y som en forsinket versjon av x med 3 samples (0.75 ms)
    d = 3
    y = np.zeros_like(x)
    y[d:] = x[:-d]

    m, tau, rxy, lags_m = finn_forsinkelse(x, y, fs)
    print("Hele samples")
    print("m_delay =", m, "samples")
    print("tau     =", tau, "s")

    m_frac, tau_frac, _, _ = finn_forsinkelse_med_oppampling(x, y, fs, L=16, vindu=20)
    print("\nMed oppsampling")
    print("m_delay_frac =", m_frac, "samples")
    print("tau_frac     =", tau_frac, "s")
