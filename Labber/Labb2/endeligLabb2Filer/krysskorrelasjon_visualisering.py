"""
Krysskorrelasjonsfunksjonen – Visuell illustrasjon av lag-estimering
=====================================================================
Bruker ekte målinger for å vise hvordan krysskorrelasjon avdekker
forsinkelsen (lag) mellom to mikrofonsignaler.

Figur:
  (a) To mikrofonsignaler (sensor 1 og 2) i tidsdomenet.
  (b) Krysskorrelasjonsfunksjonen r_21(m) over alle lag.
  (c) Forstørret versjon rundt toppen – tydelig lagvisning.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

# ---------------------------------------------------------------------------
# Konfigurasjon
# ---------------------------------------------------------------------------
MAALEFIL = Path(__file__).parent.parent / 'endeligLabb2Maalinger' / 'test' / 'testChannels1'

ADC_BITS   = 12
VREF       = 3.3
RESOLUTION = (2 ** ADC_BITS) - 1

c  = 343.0
a  = 0.05
d  = np.sqrt(3) * a

N_VIS_PERIODER = 10    # Antall perioder å vise i signalplot (f ≈ 1000 Hz)
FREQ_IN        = 1000  # Hz – frekvensen brukt under opptak
ZOOM_LAG       = 15    # Vis ±ZOOM_LAG sampler i forstørret korrelasjonsplot

# ---------------------------------------------------------------------------
# Last inn data
# ---------------------------------------------------------------------------
sample_period, data_counts = raspi_import(str(MAALEFIL), channels=3)
fs    = 1.0 / sample_period
n_max = int(np.floor(d * fs / c))

data_V = (data_counts / RESOLUTION) * VREF

m1 = data_V[:, 0] - np.mean(data_V[:, 0])   # Sensor 1 – referanse (DC fjernet)
m2 = data_V[:, 1] - np.mean(data_V[:, 1])   # Sensor 2 – forsinket (DC fjernet)

t_ms = np.arange(len(m1)) * sample_period * 1e3   # Tid i ms

print(f"Fil:               {MAALEFIL.name}")
print(f"Samplingsfrekvens: {fs:.0f} Hz")
print(f"n_max (±{d*100:.1f} cm): {n_max} sampler")

# ---------------------------------------------------------------------------
# Beregn krysskorrelasjon r_21(m)
# numpy.correlate(m2, m1)[k] = sum_n m2[n+k]*m1[n]
# Topp ved k = n_21 når m2 er forsinket n_21 sampler ift. m1
# ---------------------------------------------------------------------------
r_xy        = np.correlate(m2, m1, mode='full')
lags        = np.arange(-(len(m1) - 1), len(m2))
lag_samples = int(lags[np.argmax(np.abs(r_xy))])
lag_ms      = lag_samples / fs * 1e3

print(f"Estimert lag n_21 = {lag_samples:+d} sampler  ({lag_ms:+.3f} ms)")

# ===========================================================================
# Plotting
# ===========================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# -----------------------------------------------------------------------
# (a) Signaler i tidsdomenet
# -----------------------------------------------------------------------
idx_vis = int(N_VIS_PERIODER / FREQ_IN / sample_period)
axes[0].plot(t_ms[:idx_vis], m1[:idx_vis],
             label='Sensor 1 (ref)', linewidth=1.0)
axes[0].plot(t_ms[:idx_vis], m2[:idx_vis],
             label='Sensor 2', linewidth=1.0, alpha=0.85)
axes[0].set(xlabel='Tid [ms]', ylabel='Spenning [V]',
            title='Mikrofonsignaler')
axes[0].legend(fontsize=9)
axes[0].grid(True)

# -----------------------------------------------------------------------
# (b) Full krysskorrelasjonsfunksjon
# -----------------------------------------------------------------------
lags_ms = lags / fs * 1e3
nmax_ms = n_max / fs * 1e3

axes[1].plot(lags_ms, r_xy, linewidth=0.7)
axes[1].axvline(lag_ms, color='r', linestyle='--', linewidth=1.5,
                label=f'Topp: n_21 = {lag_samples} samp. ({lag_ms:.2f} ms)')
axes[1].axvline( nmax_ms, color='grey', linestyle=':', alpha=0.7,
                label=f'+n_max = {n_max}')
axes[1].axvline(-nmax_ms, color='grey', linestyle=':', alpha=0.7,
                label=f'-n_max = {-n_max}')
axes[1].set(xlabel='Lag [ms]', ylabel=r'Krysskorrelasjon $r_{21}$ [-]',
            title='Krysskorrelasjonsfunksjon')
axes[1].legend(fontsize=8)
axes[1].grid(True)

# -----------------------------------------------------------------------
# (c) Forstørret krysskorrelasjon rundt toppen
# -----------------------------------------------------------------------
mask         = np.abs(lags) <= ZOOM_LAG
lags_zoom_ms = lags[mask] / fs * 1e3
r_zoom       = r_xy[mask]

axes[2].plot(lags_zoom_ms, r_zoom, 'o-', markersize=4, linewidth=1.2)
axes[2].axvline(lag_ms, color='r', linestyle='--', linewidth=1.5,
                label=f'Topp: n_21 = {lag_samples} samp.')
axes[2].axvline( nmax_ms, color='grey', linestyle=':', alpha=0.7,
                label=f'+n_max = {n_max}')
axes[2].axvline(-nmax_ms, color='grey', linestyle=':', alpha=0.7,
                label=f'-n_max = {-n_max}')

# Annotasjon av toppen
peak_idx = np.argmax(np.abs(r_zoom))
peak_val = r_zoom[peak_idx]
offset_x = ZOOM_LAG * 0.25 / fs * 1e3
axes[2].annotate(
    f'n$_{{21}}$ = {lag_samples} samp.',
    xy=(lag_ms, peak_val),
    xytext=(lag_ms + offset_x, peak_val * 0.80),
    arrowprops=dict(arrowstyle='->', color='red', lw=1.2),
    fontsize=9, color='red'
)

axes[2].set(xlabel='Lag [ms]', ylabel=r'Krysskorrelasjon $r_{21}$ [-]',
            title='Krysskorrelasjon – forstørret')
axes[2].legend(fontsize=8)
axes[2].grid(True)

# -----------------------------------------------------------------------
# Subplot-etiketter (a), (b), (c)
# -----------------------------------------------------------------------
for ax, label in zip(axes, ['(a)', '(b)', '(c)']):
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')

fig.suptitle(
    'Krysskorrelasjonsfunksjonen – forsinkelsesestimering mellom sensor 1 og 2',
    fontsize=13
)
plt.tight_layout()
plt.show()
