"""
Krysskorrelasjon – generisk illustrasjon
========================================
Viser hvordan krysskorrelasjon avdekker tidsforskyvningen mellom to signaler.

Figur:
  (a) To identiske signaler – signal y er forskyvet nøyaktig 3 sampler.
  (b) Krysskorrelasjonen r_xy(m) for hele signallengden.
  (c) Forstørret versjon av (b) rundt toppen.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Syntesiser to signaler
# ---------------------------------------------------------------------------
fs     = 4000          # Hz – samplingsfrekvens
f0     = 150           # Hz – frekvens for sinusen (lavt nok til å gi ~6 synlige sykluser)
T      = 0.04          # s  – signallengde
t      = np.arange(0, T, 1 / fs)   # tidvektor

N_SHIFT = 3            # eksakt forsinkelse i antall sampler  (= 0.75 ms ved fs=4000)

# Gaussisk-modulert sinusoid (bølgepakke)
sigma  = T / 5
env    = np.exp(-((t - T / 2) ** 2) / (2 * sigma ** 2))
x      = env * np.sin(2 * np.pi * f0 * t)

# y er identisk med x, men forskyvet N_SHIFT sampler
y      = np.roll(x, N_SHIFT)
y[:N_SHIFT] = 0        # unngå wrap-around

t_ms   = t * 1e3       # tid i ms

# ---------------------------------------------------------------------------
# Krysskorrelasjonen
# ---------------------------------------------------------------------------
r_xy  = np.correlate(x, y, mode='full')
lags  = np.arange(-(len(y) - 1), len(x))   # lag i antall sampler
lags_ms = lags / fs * 1e3                  # lag i ms

peak_lag_ms = lags_ms[np.argmax(r_xy)]

ZOOM = 10   # vis ±ZOOM sampler rundt null i forstørret plot
zoom_mask = np.abs(lags) <= ZOOM

# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
ax_sig, ax_full, ax_zoom = axes

# --- (a) Signaler ---
ax_sig.plot(t_ms, x, 'b.-', markersize=4, linewidth=1.2, label='Signal x')
ax_sig.plot(t_ms, y, 'r.-', markersize=4, linewidth=1.2, label='Signal y', alpha=0.85)
ax_sig.set(xlabel='Time [ms]', ylabel='Signal amplitude [-]',
           title='Signaler')
ax_sig.legend(fontsize=9)
ax_sig.grid(True)

# --- (b) Full krysskorrelasjon ---
ax_full.plot(lags_ms, r_xy, 'b-', linewidth=1.2)
ax_full.set(xlabel='Time [ms]', ylabel=r'Cross correlation $r_{xy}$',
            title='Krysskorrelasjonsfunksjonen')
ax_full.grid(True)

# --- (c) Forstørret rundt toppen ---
ax_zoom.plot(lags_ms[zoom_mask], r_xy[zoom_mask], 'b.-', markersize=5, linewidth=1.2)
ax_zoom.axvline(peak_lag_ms, color='red', linestyle='--', linewidth=1.0,
                label=f'Topp ved {peak_lag_ms:.3f} ms')
ax_zoom.set(xlabel='Time [ms]', ylabel=r'Cross correlation $r_{xy}$',
            title='Forstørret – rundt toppen')
ax_zoom.legend(fontsize=9)
ax_zoom.grid(True)

# --- Subplot-etiketter ---
for ax, label in zip(axes, ['(a)', '(b)', '(c)']):
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')

fig.suptitle(
    'Krysskorrelasjon: toppen av $r_{xy}$ avdekker tidsforskyvningen mellom x og y',
    fontsize=12
)
plt.tight_layout()
plt.show()
