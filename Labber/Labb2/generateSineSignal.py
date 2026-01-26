import numpy as np

def generer_signaler(frekvens, fs, varighet, forsinkelse_samples):
    """
    Genererer to sinussignaler der y er en forsinket versjon av x med et helt antall sampler.

    Viktig:
    Her lages y ved å forskyve signalet i tid: y(t) = sin(2*pi*f*(t - delay/fs)).
    Det betyr at y "kommer senere" enn x når delay > 0.
    """
    t = np.arange(0, varighet, 1 / fs)

    x = np.sin(2 * np.pi * frekvens * t)

    delay_s = forsinkelse_samples / fs
    y = np.sin(2 * np.pi * frekvens * (t - delay_s))

    return t, x, y, forsinkelse_samples

def generer_sinus(t, frekvens, delay_samples, fs):
    delay_s = delay_samples / fs
    return np.sin(2 * np.pi * frekvens * (t - delay_s))

def sinus_med_pakke(t, frekvens, fs, delay_samples=0, t0=None, sigma=0.01, A=1.0):
    """
    Lager en sinus som er multiplisert med en gaussisk "pakke" (envelope),
    slik at signalet blir tidsbegrenset og gir en tydeligere, mer unik topp i krysskorrelasjon.

    Parametre:
    t             : tidsvektor [s]
    frekvens      : sinusfrekvens [Hz]
    fs            : samplingsfrekvens [Hz]
    delay_samples : forsinkelse i samples (y kommer senere når delay_samples > 0)
    t0            : sentrum for pakken [s]. Hvis None, brukes midten av t.
    sigma         : bredde (standardavvik) til gauss [s]. Mindre sigma gir smalere pakke.
    A             : amplitude

    Returnerer:
    x : signalet
    """

    if t0 is None:
        t0 = 0.5 * (t[0] + t[-1])

    delay_s = delay_samples / fs
    t_shift = t - delay_s

    envelope = np.exp(-0.5 * ((t_shift - t0) / sigma) ** 2)
    sinus = np.sin(2 * np.pi * frekvens * t_shift)

    x = A * envelope * sinus
    return x