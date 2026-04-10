"""
Forberedelsesoppgave 1
======================
Beskriv med Python-kode hvordan krysskorrelasjon kan brukes for å finne
effektiv forsinkelse mellom to lydsignaler samplet med frekvens fs.

Fremgangsmåte:
  1. Fjern DC-komponent (trekk fra middelverdi).
  2. Beregn krysskorrelasjonsfunksjonen r_xy(m) = sum_n x[n] * y[n+m].
  3. Finn m der |r_xy(m)| er størst – det er den effektive forsinkelsen i sampler.
  4. Forsinkelsen i tid: delta_t = m / fs.
"""

import numpy as np
import matplotlib.pyplot as plt


def finn_effektiv_forsinkelse(x, y, fs):
    """
    Finn effektiv forsinkelse mellom to signaler x og y.

    Krysskorrelasjonsdefinisjon (jf. lign. 1 i lab-oppgaven):
        r_xy(m) = sum_n  x[n] * y[n+m]

    numpy.correlate(a, v) beregner sum_n a[n+k] * v[n], som er r_xy(-k)
    når a=x og v=y. For å få r_xy(m) direkte bruker vi a=y og v=x slik
    at numpy.correlate(y, x)[k] = sum_n y[n+k]*x[n] = r_xy(k).

    Parametre:
        x  : referansesignal (1D numpy array), DC fjernes internt
        y  : mulig forsinket signal (1D numpy array), DC fjernes internt
        fs : samplingsfrekvens [Hz]

    Returnerer:
        lag_samples : forsinkelse i sampler (heltall m der |r_xy(m)| er størst)
        lag_tid_s   : forsinkelse i sekunder
        r_xy        : krysskorrelasjonsfunksjonsverdiene
        lags        : m-verdier som hører til r_xy
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # Steg 1: Fjern DC-komponent
    x = x - np.mean(x)
    y = y - np.mean(y)

    # Steg 2: Beregn r_xy(m)
    # numpy.correlate(y, x)[k] = sum_n y[n+k]*x[n] = r_xy(k)
    r_xy = np.correlate(y, x, mode='full')
    lags = np.arange(-(len(x) - 1), len(y))

    # Steg 3: Finn m der |r_xy(m)| er størst
    lag_samples = int(lags[np.argmax(np.abs(r_xy))])

    # Steg 4: Omregn til tid
    lag_tid_s = lag_samples / fs

    return lag_samples, lag_tid_s, r_xy, lags


# ---------------------------------------------------------------------------
# Demonstrasjon
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    fs = 4000          # Samplingsfrekvens [Hz] – som i teorieksempelet
    varighet = 0.5     # Signalvarighet [s]
    frekvens = 200     # Sinusfrekvens [Hz]

    t = np.arange(0, varighet, 1 / fs)
    x_ren = np.sin(2 * np.pi * frekvens * t)

    # -----------------------------------------------------------------------
    # Eksempel 1: Eksakt 3 samplers forsinkelse
    # -----------------------------------------------------------------------
    forsinkelse_1 = 3   # sampler
    y1 = np.sin(2 * np.pi * frekvens * (t - forsinkelse_1 / fs))

    lag1, tid1, r1, lags1 = finn_effektiv_forsinkelse(x_ren, y1, fs)
    print("Eksempel 1: Eksakt forsinkelse")
    print(f"  Forventet: {forsinkelse_1} sampler ({forsinkelse_1/fs*1e3:.3f} ms)")
    print(f"  Funnet:    {lag1} sampler ({tid1*1e3:.3f} ms)")

    # -----------------------------------------------------------------------
    # Eksempel 2: Sub-sample forsinkelse (0.25 sampler) – begrenset nøyaktighet
    # -----------------------------------------------------------------------
    forsinkelse_2 = 0.25   # sampler
    y2 = np.sin(2 * np.pi * frekvens * (t - forsinkelse_2 / fs))

    lag2, tid2, r2, lags2 = finn_effektiv_forsinkelse(x_ren, y2, fs)
    print("\nEksempel 2: Sub-sample forsinkelse (0.25 sampler)")
    print(f"  Forventet: {forsinkelse_2} sampler ({forsinkelse_2/fs*1e3:.4f} ms)")
    print(f"  Funnet:    {lag2} sampler ({tid2*1e3:.4f} ms)")
    print(f"  Feil: ±0.5 sampel = ±{0.5/fs*1e3:.4f} ms (uten oppsampling)")

    # -----------------------------------------------------------------------
    # Eksempel 3: Signal med støy
    # -----------------------------------------------------------------------
    forsinkelse_3 = 3   # sampler
    snr_db = 5          # Signal-til-støy [dB]
    snr = 10 ** (snr_db / 20)
    y3 = np.sin(2 * np.pi * frekvens * (t - forsinkelse_3 / fs))
    noise_x = np.random.normal(0, 1 / snr, len(t))
    noise_y = np.random.normal(0, 1 / snr, len(t))
    x_støy = x_ren + noise_x
    y3_støy = y3 + noise_y

    lag3, tid3, r3, lags3 = finn_effektiv_forsinkelse(x_støy, y3_støy, fs)
    print("\nEksempel 3: Eksakt forsinkelse med gaussisk støy (SNR ≈ 5 dB)")
    print(f"  Forventet: {forsinkelse_3} sampler ({forsinkelse_3/fs*1e3:.3f} ms)")
    print(f"  Funnet:    {lag3} sampler ({tid3*1e3:.3f} ms)")

    # -----------------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------------
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    zoom = 20   # Vis kun ±zoom sampler rundt toppen

    # Eks. 1 – signaler
    n_vis = 80
    axes[0, 0].plot(t[:n_vis] * 1e3, x_ren[:n_vis], label='x')
    axes[0, 0].plot(t[:n_vis] * 1e3, y1[:n_vis], '--', label=f'y (forsinket {forsinkelse_1} samp.)')
    axes[0, 0].set(xlabel='Tid [ms]', ylabel='Amplitude',
                   title='Eks. 1 – Signaler')
    axes[0, 0].legend(); axes[0, 0].grid(True)

    # Eks. 1 – krysskorrelasjon
    mask1 = np.abs(lags1) <= zoom
    axes[0, 1].plot(lags1[mask1], r1[mask1])
    axes[0, 1].axvline(lag1, color='r', linestyle='--', label=f'Funnet: {lag1} samp.')
    axes[0, 1].axvline(forsinkelse_1, color='g', linestyle=':', label=f'Forventet: {forsinkelse_1} samp.')
    axes[0, 1].set(xlabel='Lag m [sampler]', ylabel='r_xy(m)',
                   title='Eks. 1 – Krysskorrelasjon')
    axes[0, 1].legend(); axes[0, 1].grid(True)

    # Eks. 2 – signaler
    axes[1, 0].plot(t[:n_vis] * 1e3, x_ren[:n_vis], label='x')
    axes[1, 0].plot(t[:n_vis] * 1e3, y2[:n_vis], '--', label=f'y (forsinket {forsinkelse_2} samp.)')
    axes[1, 0].set(xlabel='Tid [ms]', ylabel='Amplitude',
                   title='Eks. 2 – Sub-sample forsinkelse')
    axes[1, 0].legend(); axes[1, 0].grid(True)

    # Eks. 2 – krysskorrelasjon
    mask2 = np.abs(lags2) <= zoom
    axes[1, 1].plot(lags2[mask2], r2[mask2])
    axes[1, 1].axvline(lag2, color='r', linestyle='--', label=f'Funnet: {lag2} samp.')
    axes[1, 1].axvline(forsinkelse_2, color='g', linestyle=':', label=f'Forventet: {forsinkelse_2} samp.')
    axes[1, 1].set(xlabel='Lag m [sampler]', ylabel='r_xy(m)',
                   title='Eks. 2 – Krysskorrelasjon (sub-sample)')
    axes[1, 1].legend(); axes[1, 1].grid(True)

    # Eks. 3 – signaler med støy
    axes[2, 0].plot(t[:n_vis] * 1e3, x_støy[:n_vis], label='x (med støy)')
    axes[2, 0].plot(t[:n_vis] * 1e3, y3_støy[:n_vis], '--', label='y (forsinket + støy)')
    axes[2, 0].set(xlabel='Tid [ms]', ylabel='Amplitude',
                   title=f'Eks. 3 – Støy (SNR ≈ {snr_db} dB)')
    axes[2, 0].legend(); axes[2, 0].grid(True)

    # Eks. 3 – krysskorrelasjon
    mask3 = np.abs(lags3) <= zoom
    axes[2, 1].plot(lags3[mask3], r3[mask3])
    axes[2, 1].axvline(lag3, color='r', linestyle='--', label=f'Funnet: {lag3} samp.')
    axes[2, 1].axvline(forsinkelse_3, color='g', linestyle=':', label=f'Forventet: {forsinkelse_3} samp.')
    axes[2, 1].set(xlabel='Lag m [sampler]', ylabel='r_xy(m)',
                   title='Eks. 3 – Krysskorrelasjon (støy)')
    axes[2, 1].legend(); axes[2, 1].grid(True)

    plt.suptitle('Forberedelsesoppgave 1: Krysskorrelasjon for å finne effektiv forsinkelse',
                 fontsize=13)
    plt.tight_layout()
    plt.show()
