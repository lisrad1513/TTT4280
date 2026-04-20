"""
Krysskorrelasjonsfunksjonen – Visuell illustrasjon av lag-estimering
=====================================================================
Bruker ekte målinger for å vise hvordan krysskorrelasjon avdekker
forsinkelsen (lag) mellom mikrofonsignalpar.

Figur:
  (a) Alle tre mikrofonsignaler i tidsdomenet.
  (b) Krysskorrelasjon r_21(m) – forstørret rundt toppen.
  (c) Krysskorrelasjon r_31(m) – forstørret rundt toppen.
  (d) Krysskorrelasjon r_32(m) – forstørret rundt toppen.
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

N_VIS_PERIODER = 20    # Antall perioder å vise i signalplot (f ≈ 1000 Hz)
FORSKYVNING_MS = 500   # Startpunkt i ms (sett til 0 for å starte fra begynnelsen)
FREQ_IN        = 1000  # Hz – frekvensen brukt under opptak
ZOOM_LAG       = 15    # Vis ±ZOOM_LAG sampler i forstørret korrelasjonsplot

# ---------------------------------------------------------------------------
# Last inn data
# ---------------------------------------------------------------------------
sample_period, data_counts = raspi_import(str(MAALEFIL), channels=3)
fs    = 1.0 / sample_period
n_max = int(np.floor(d * fs / c))

data_V = (data_counts / RESOLUTION) * VREF

m1 = data_V[:, 0] - np.mean(data_V[:, 0])   # Sensor 1 – referanse
m2 = data_V[:, 1] - np.mean(data_V[:, 1])   # Sensor 2
m3 = data_V[:, 2] - np.mean(data_V[:, 2])   # Sensor 3

t_ms = np.arange(len(m1)) * sample_period * 1e3   # Tid i ms

print(f"Fil:               {MAALEFIL.name}")
print(f"Samplingsfrekvens: {fs:.0f} Hz")
print(f"n_max (±{d*100:.1f} cm): {n_max} sampler")

# ---------------------------------------------------------------------------
# Beregn krysskorrelasjon for alle tre par
# ---------------------------------------------------------------------------
def xcorr(x, y):
    """Returnerer (lags, korrelasjon) der lags er i antall sampler."""
    r    = np.correlate(x, y, mode='full')
    lags = np.arange(-(len(y) - 1), len(x))
    return lags, r

lags_21, r_21 = xcorr(m2, m1)
lags_31, r_31 = xcorr(m3, m1)
lags_32, r_32 = xcorr(m3, m2)

n_21 = int(lags_21[np.argmax(np.abs(r_21))])
n_31 = int(lags_31[np.argmax(np.abs(r_31))])
n_32 = int(lags_32[np.argmax(np.abs(r_32))])

print(f"Estimert lag n_21 = {n_21:+d} sampler")
print(f"Estimert lag n_31 = {n_31:+d} sampler")
print(f"Estimert lag n_32 = {n_32:+d} sampler")

# ===========================================================================
# Plotting
# ===========================================================================
fig, (ax_sig, ax_corr) = plt.subplots(1, 2, figsize=(14, 5))

# -----------------------------------------------------------------------
# (a) Signaler i tidsdomenet
# -----------------------------------------------------------------------
idx_start = int(FORSKYVNING_MS * 1e-3 / sample_period)
idx_vis   = idx_start + int(N_VIS_PERIODER / FREQ_IN / sample_period)
ax_sig.plot(t_ms[idx_start:idx_vis], m1[idx_start:idx_vis], label='Sensor 1', linewidth=1.0)
ax_sig.plot(t_ms[idx_start:idx_vis], m2[idx_start:idx_vis], label='Sensor 2', linewidth=1.0, alpha=0.85)
ax_sig.plot(t_ms[idx_start:idx_vis], m3[idx_start:idx_vis], label='Sensor 3', linewidth=1.0, alpha=0.85)
ax_sig.set(xlabel='Tid [ms]', ylabel='Spenning [V]', title='Mikrofonsignaler')
ax_sig.legend(fontsize=9)
ax_sig.grid(True)

# -----------------------------------------------------------------------
# (b) Alle tre krysskorrelasjoner overlappet (zoomed, lags i sampler)
# -----------------------------------------------------------------------
for lags, r_xy, n_peak, label in [
        (lags_21, r_21, n_21, rf'$r_{{21}}$ = {n_21:+d} lags'),
        (lags_31, r_31, n_31, rf'$r_{{31}}$ = {n_31:+d} lags'),
        (lags_32, r_32, n_32, rf'$r_{{32}}$ = {n_32:+d} lags')]:
    mask   = np.abs(lags) <= ZOOM_LAG
    l_zoom = lags[mask]
    r_zoom = r_xy[mask]
    # Normaliser til [-1, 1] så de er sammenlignbare
    r_norm = r_zoom / np.max(np.abs(r_zoom))
    line,  = ax_corr.plot(l_zoom, r_norm, 'o-', markersize=4, linewidth=1.2, label=label)
    ax_corr.axvline(n_peak, color=line.get_color(), linestyle='--', linewidth=1.0, alpha=0.7)

ax_corr.axvline( n_max, color='grey', linestyle=':', alpha=0.7, label=f'+n_max = {n_max}')
ax_corr.axvline(-n_max, color='grey', linestyle=':', alpha=0.7, label=f'-n_max = {-n_max}')
ax_corr.set(xlabel='Lag [sampler]', ylabel='Normalisert krysskorrelasjon [-]',
            title='Krysskorrelasjoner – forstørret')
ax_corr.legend(fontsize=9)
ax_corr.grid(True)

# -----------------------------------------------------------------------
# Subplot-etiketter (a)–(b)
# -----------------------------------------------------------------------
for ax, label in zip([ax_sig, ax_corr], ['(a)', '(b)']):
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')

fig.suptitle(
    'Krysskorrelasjonsfunksjonen – forsinkelsesestimering mellom mikrofonsignalpar',
    fontsize=13
)
plt.tight_layout()
plt.show()
