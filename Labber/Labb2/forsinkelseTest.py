import numpy as np
import matplotlib.pyplot as plt

from forsinkelse import finn_forsinkelse, finn_forsinkelse_med_oppampling


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


# Parametere
frekvens = 50
fs = 4000
varighet = 1.0
forsinkelse_samples = 3

# Generer signalene
t, x, y, forventet_delay_samples = generer_signaler(frekvens, fs, varighet, forsinkelse_samples)

oppsamplet = False
oppsamplingsfaktor = 16

# Finn forsinkelsen (heltalls-samples)
print(f"Forventet forsinkelse: {forventet_delay_samples} samples ({forventet_delay_samples/fs} sekunder)")

if not oppsamplet:
    m_delay, tau, rxy, lags_m = finn_forsinkelse(x, y, fs)
    print(f"Funnet forsinkelse:     {m_delay} samples ({tau} sekunder)")
else:
    m_delay, tau, rxy, lags_m = finn_forsinkelse_med_oppampling(x, y, fs, oppsamplingsfaktor, vindu=40)
    print(f"Funnet (oppsamplet):    {m_delay} samples ({tau} sekunder)")

# Plot signalene (som i kompendiet)
plt.figure()
plt.plot(t, x, label="Signal x(t)")
plt.plot(t, y, label="Signal y(t)", alpha=0.7)
plt.xlim(0, 0.1)
plt.title("Originale signaler")
plt.xlabel("Tid [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.show()

# Plot krysskorrelasjon (full, med lag-akse i kompendiets m)
plt.figure()
plt.plot(lags_m / fs, rxy)
plt.title("Krysskorrelasjon r_xy(m)")
plt.xlabel("Tid [s]")
plt.ylabel("r_xy")
plt.grid(True)
plt.show()

# Zoom inn rundt toppen
plt.figure()
plt.plot(lags_m / fs, rxy)
plt.xlim((m_delay - 50) / fs, (m_delay + 50) / fs)
plt.title("Krysskorrelasjon zoom rundt topp")
plt.xlabel("Tid [s]")
plt.ylabel("r_xy")
plt.grid(True)
plt.show()
