"""
Laboppgave – Oppgave 2, 3 og 4
================================
Bruker målefilen  endeligLabb2Maalinger/test/testChannels1  (1 kHz sinussignal).

Oppgave 2: Vis at de tre mikrofonsignalene ser ut som forventet.
           – Amplituden skal variere rundt 0 (DC-komponent fjernes).
           – Alle tre skal se ut som sinustoner.

Oppgave 3: Implementer krysskorrelasjon for de tre mikrofonsignalene.
           – Finn forsinkelse (i sampler) fra toppen av krysskorrelasjonene.
           – Vis de tre krysskorrelasjonssignalene.
           – Vis ett autokorrelasjonssignal; sjekk topp ved lag = 0.
           – Sjekk at toppene er innenfor ±n_max.

Oppgave 4: Beregn innfallsvinkelen fra de tre tidsforsinkelsene.
           – Bruk formel (29) fra teoridelen.
           – Demonstrer at vinkler fra -180 til +180 grader kan estimeres.

Array-geometri (fra figur 4 i lab-oppgaven, likesidet triangel med sidelengde d = sqrt(3)*a):
    Sensor 1:  [0,         +a]
    Sensor 2:  [-sqrt(3)/2 * a, -a/2]
    Sensor 3:  [+sqrt(3)/2 * a, -a/2]

    x_21 = sensor2 - sensor1 = [-sqrt(3)/2, -3/2] * a
    x_31 = sensor3 - sensor1 = [+sqrt(3)/2, -3/2] * a
    x_32 = sensor3 - sensor2 = [+sqrt(3),      0] * a

Vinkelformel (lign. 28/29):
    theta = arctan2( sqrt(3)*(n_21 + n_31),  n_21 - n_31 - 2*n_32 )
    Resultat ligger i (-pi, pi], dvs. -180° til +180°.

Kanal-til-sensor-mapping (samme som ekteSignalRegning.py):
    m1 = data[:, 0]  (sensor 1)
    m2 = data[:, 1]  (sensor 2)
    m3 = data[:, 2]  (sensor 3)
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Legg til rotmappen (Labb2/) i Python-path for raspi_import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

# ---------------------------------------------------------------------------
# Konfigurasjon
# ---------------------------------------------------------------------------
MAALEFIL = Path(__file__).parent.parent / 'endeligLabb2Maalinger' / 'test' / 'testChannels1'

ADC_BITS  = 12
VREF      = 3.3       # Volt
RESOLUTION = (2 ** ADC_BITS) - 1

c   = 343.0           # Lydhastighet [m/s]
a   = 0.05            # Array-parameter [m]  (d = sqrt(3)*a ≈ 8.66 cm)
d   = np.sqrt(3) * a  # Sidelengde [m]

ZOOM_LAG       = 15   # Vis ±ZOOM_LAG sampler i korrelasjonsplottene
N_VIS_PERIODER = 50    # Antall perioder å vise i signalplot (f ≈ 1000 Hz)
FORSKYVNING_MS = 500   # Startpunkt i ms (sett til 0 for å starte fra begynnelsen)


# ---------------------------------------------------------------------------
# Hjelpefunksjoner
# ---------------------------------------------------------------------------
def counts_til_volt(data):
    return (data / RESOLUTION) * VREF


def finn_forsinkelse(ref, sig):
    """
    Finn forsinkelse n slik at sig[n] ≈ ref[n-n_lag] (sig er forsinket n_lag sampler).
    Returnerer: n_lag, r_xy, lags
    """
    ref = ref - np.mean(ref)
    sig = sig - np.mean(sig)
    # numpy.correlate(sig, ref)[k] = sum_n sig[n+k]*ref[n]
    # Topp ved k = n_lag når sig er forsinket n_lag sampler ift. ref
    r_xy = np.correlate(sig, ref, mode='full')
    lags = np.arange(-(len(ref) - 1), len(sig))
    n_lag = int(lags[np.argmax(np.abs(r_xy))])
    return n_lag, r_xy, lags


def beregn_vinkel(n_21, n_31, n_32):
    """
    Beregn innfallsvinkel theta fra tidsforsinkelsene n_21, n_31, n_32.

    Basert på lign. (29) i lab-oppgaven:
        theta = arctan2( sqrt(3)*(n_21 + n_31),  n_21 - n_31 - 2*n_32 )

    Returnerer vinkel i radianer og grader, i intervallet (-180°, 180°].
    """
    teller = np.sqrt(3) * (n_21 + n_31)
    nevner = n_21 - n_31 - 2 * n_32
    theta_rad = np.arctan2(teller, nevner)
    return theta_rad, np.degrees(theta_rad)


# ===========================================================================
# Last inn data
# ===========================================================================
sample_period, data_counts = raspi_import(str(MAALEFIL), channels=3)
fs = 1.0 / sample_period
n_max = int(np.floor(d * fs / c))

print(f"Fil:               {MAALEFIL.name}")
print(f"Samplingsfrekvens: {fs:.0f} Hz  (sample_period = {sample_period*1e6:.1f} µs)")
print(f"Antall sampler:    {data_counts.shape[0]}")
print(f"n_max (±{d*100:.1f} cm, c={c} m/s): {n_max} sampler")

# Konverter til volt
data_V = counts_til_volt(data_counts)
m1_raw = data_V[:, 0]
m2_raw = data_V[:, 1]
m3_raw = data_V[:, 2]

t = np.arange(data_V.shape[0]) * sample_period


# ===========================================================================
# OPPGAVE 2 – Vis signalene (med DC-fjerning)
# ===========================================================================
m1 = m1_raw - np.mean(m1_raw)
m2 = m2_raw - np.mean(m2_raw)
m3 = m3_raw - np.mean(m3_raw)

freq_in    = 1000    # Hz – frekvensen brukt under opptak
idx_start  = int(FORSKYVNING_MS * 1e-3 / sample_period)
idx_vis    = idx_start + int(N_VIS_PERIODER / freq_in / sample_period)

fig2, ax2 = plt.subplots(figsize=(10, 4))
for signal, label, color in zip(
        [m1, m2, m3],
        ['Sensor 1 (kanal 0)', 'Sensor 2 (kanal 1)', 'Sensor 3 (kanal 2)'],
        ['tab:blue', 'tab:orange', 'tab:green']):
    ax2.plot(t[idx_start:idx_vis] * 1e3, signal[idx_start:idx_vis],
             color=color, linewidth=0.8, label=label)
ax2.axhline(0, linestyle='--', color='k', linewidth=0.6, alpha=0.5)
ax2.set(xlabel='Tid [ms]', ylabel='Spenning [V]')
ax2.legend(fontsize=9)
ax2.grid(True)

fig2.suptitle('Oppgave 2 – Tre mikrofonsignaler (DC fjernet)', fontsize=13)
plt.tight_layout()

print("\nOppgave 2: DC-nivåer (counts):")
for i, ch in enumerate([data_counts[:, 0], data_counts[:, 1], data_counts[:, 2]]):
    print(f"  Kanal {i}: mean = {ch.mean():.1f}, std = {ch.std():.1f}")


# ===========================================================================
# OPPGAVE 3 – Krysskorrelasjon og autokorrelasjon
# ===========================================================================
n_31, r_31, lags31 = finn_forsinkelse(m1, m3)   # forsinkelse sensor 1→3
n_21, r_21, lags21 = finn_forsinkelse(m1, m2)   # forsinkelse sensor 1→2
n_32, r_32, lags32 = finn_forsinkelse(m2, m3)   # forsinkelse sensor 2→3

# Autokorrelasjon av sensor 1 (skal ha topp ved lag=0)
r_auto = np.correlate(m1, m1, mode='full')
lags_auto = np.arange(-(len(m1) - 1), len(m1))
n_auto = int(lags_auto[np.argmax(np.abs(r_auto))])

print("\nOppgave 3:")
print(f"  n_31 = {n_31:+d} sampler  (topp innenfor ±{n_max}? {abs(n_31) <= n_max})")
print(f"  n_21 = {n_21:+d} sampler  (topp innenfor ±{n_max}? {abs(n_21) <= n_max})")
print(f"  n_32 = {n_32:+d} sampler  (topp innenfor ±{n_max}? {abs(n_32) <= n_max})")
print(f"  Autokorrelasjon sensor 1: topp ved lag = {n_auto} (forventet 0)")

fig3, axes3 = plt.subplots(2, 2, figsize=(12, 8))

# Krysskorrelasjoner
for ax, r, lags, n_lag, tittel in [
        (axes3[0, 0], r_31, lags31, n_31, f'r_31: sensor 3 vs. sensor 1  (n_31 = {n_31})'),
        (axes3[0, 1], r_21, lags21, n_21, f'r_21: sensor 2 vs. sensor 1  (n_21 = {n_21})'),
        (axes3[1, 0], r_32, lags32, n_32, f'r_32: sensor 3 vs. sensor 2  (n_32 = {n_32})')]:
    mask = np.abs(lags) <= ZOOM_LAG
    ax.plot(lags[mask], r[mask])
    ax.axvline(n_lag, color='r', linestyle='--', linewidth=1.5,
               label=f'Topp: {n_lag} samp.')
    ax.axvline(n_max,  color='grey', linestyle=':', alpha=0.7, label=f'+n_max = {n_max}')
    ax.axvline(-n_max, color='grey', linestyle=':', alpha=0.7, label=f'-n_max = {-n_max}')
    ax.set(xlabel='Lag m [sampler]', ylabel='r(m)', title=tittel)
    ax.legend(fontsize=8); ax.grid(True)

# Autokorrelasjon
mask_auto = np.abs(lags_auto) <= ZOOM_LAG
axes3[1, 1].plot(lags_auto[mask_auto], r_auto[mask_auto])
axes3[1, 1].axvline(n_auto, color='r', linestyle='--', linewidth=1.5,
                    label=f'Topp: {n_auto} samp. (forventet 0)')
axes3[1, 1].set(xlabel='Lag m [sampler]', ylabel='r(m)',
                title='Autokorrelasjon – sensor 1')
axes3[1, 1].legend(fontsize=8); axes3[1, 1].grid(True)

# Subplot-etiketter
for ax, label in zip(axes3.flat, ['(a)', '(b)', '(c)', '(d)']):
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')

fig3.suptitle('Oppgave 3 – Krysskorrelasjoner og autokorrelasjon', fontsize=13)
plt.tight_layout()


# ===========================================================================
# OPPGAVE 4 – Beregn innfallsvinkel og demonstrer -180° til +180°
# ===========================================================================
theta_rad, theta_deg = beregn_vinkel(n_21, n_31, n_32)

print(f"\nOppgave 4:")
print(f"  n_21={n_21}, n_31={n_31}, n_32={n_32}")
print(f"  Estimert vinkel: {theta_deg:.1f}°  ({theta_rad:.4f} rad)")

# ---
# Demonstrer at formelen gir vinkler over hele [-180°, 180°) ved å beregne
# forventede forsinkelser for alle vinkler og kjøre tilbake.
# ---
theta_test = np.linspace(-np.pi, np.pi, 361)

# Sensor-posisjoner (fra lign. 15–17)
s1 = np.array([0.0,              a])
s2 = np.array([-np.sqrt(3)/2*a, -a/2])
s3 = np.array([ np.sqrt(3)/2*a, -a/2])

theta_est = []
for th in theta_test:
    # Innfallsretning som enhetsvektor
    x_hat = np.array([np.cos(th), np.sin(th)])
    # Tidsforsinkelse tau_ji = - (x_ji . x_hat) / c   (fra lign. 6)
    x_21 = s2 - s1; tau_21 = -np.dot(x_21, x_hat) / c
    x_31 = s3 - s1; tau_31 = -np.dot(x_31, x_hat) / c
    x_32 = s3 - s2; tau_32 = -np.dot(x_32, x_hat) / c
    # Konverter til heltalls-sampler (avrunding simulerer ADC-diskretisering)
    n21 = int(round(tau_21 * fs))
    n31 = int(round(tau_31 * fs))
    n32 = int(round(tau_32 * fs))
    _, th_est = beregn_vinkel(n21, n31, n32)
    theta_est.append(th_est)

theta_est = np.array(theta_est)
theta_test_deg = np.degrees(theta_test)

fig4, axes4 = plt.subplots(1, 2, figsize=(12, 5))

# Venstre: estimert vs. faktisk vinkel
axes4[0].plot(theta_test_deg, theta_est, linewidth=1.2)
axes4[0].plot([-180, 180], [-180, 180], 'k--', linewidth=0.8, label='Ideal (y=x)')
axes4[0].axvline(theta_deg, color='r', linestyle='--',
                 label=f'Målt vinkel: {theta_deg:.1f}°')
axes4[0].set(xlabel='Faktisk vinkel [grader]', ylabel='Estimert vinkel [grader]',
             title='Estimert vs. faktisk innfallsvinkel',
             xlim=[-180, 180], ylim=[-180, 180])
axes4[0].legend(fontsize=9); axes4[0].grid(True)

# Høyre: feil (diskretiseringsfeil fra heltalls-sampler)
feil = theta_est - theta_test_deg
# Normaliser til (-180, 180]
feil = (feil + 180) % 360 - 180
axes4[1].plot(theta_test_deg, feil, linewidth=1.0)
axes4[1].set(xlabel='Faktisk vinkel [grader]', ylabel='Feil [grader]',
             title='Estimeringsfel grunnet heltalls-avrunding av forsinkelse',
             xlim=[-180, 180])
axes4[1].axhline(0, color='k', linewidth=0.6)
axes4[1].grid(True)

# Subplot-etiketter
for ax, label in zip(axes4, ['(a)', '(b)']):
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')

fig4.suptitle('Oppgave 4 – Innfallsvinkelestimering over [-180°, +180°]', fontsize=13)
plt.tight_layout()

print(f"\n  Demonstrasjon (oppgave 4): Formelen dekker alle vinkler [-180°, +180°].")
print(f"  Maks diskretiseringsfeil (heltalls-sampler): "
      f"{np.max(np.abs(feil)):.1f}°")

plt.show()
