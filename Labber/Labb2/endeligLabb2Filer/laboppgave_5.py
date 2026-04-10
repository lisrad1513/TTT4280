"""
Laboppgave – Oppgave 5
=======================
Systematisk variasjon av estimert innfallsvinkel for flere innfallsvinkler.

Datamapper (fra endeligLabb2Maalinger/konsekventTesting/):
    pos1_degMin120_{1..4}  – Nominell innfallsvinkel  -120°
    pos1_degMin60_{1..4}   – Nominell innfallsvinkel   -60°
    pos1_degPos60_{1..4}   – Nominell innfallsvinkel   +60°

For hver vinkel:
  – Gjør ≥ 5 (her 4) gjentatte målinger.
  – Beregn estimert theta for hver måling.
  – Beregn gjennomsnitt, standardavvik og varians.

Vinkelformel (lign. 29):
    theta = arctan2( sqrt(3)*(n_21 + n_31),  n_21 - n_31 - 2*n_32 )

Kanal-til-sensor-mapping:
    m1 = data[:, 0]  (sensor 1)
    m2 = data[:, 1]  (sensor 2)
    m3 = data[:, 2]  (sensor 3)
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
BASE = Path(__file__).parent.parent / 'endeligLabb2Maalinger' / 'konsekventTesting'

ADC_BITS   = 12
VREF       = 3.3
RESOLUTION = (2 ** ADC_BITS) - 1

c = 343.0    # Lydhastighet [m/s]
a = 0.05     # Array-parameter [m]
d = np.sqrt(3) * a

# Nominelle vinkler og tilhørende filnavn-prefiks
VINKLER = [
    (-120, 'pos1_degMin120'),
    ( -60, 'pos1_degMin60'),
    (  60, 'pos1_degPos60'),
]
N_MAALINGER = 4   # Antall gjentatte målinger per vinkel


# ---------------------------------------------------------------------------
# Hjelpefunksjoner
# ---------------------------------------------------------------------------
def counts_til_volt(data):
    return (data / RESOLUTION) * VREF


def finn_forsinkelse(ref, sig):
    """Returnerer n_lag (sampler) fra krysskorrelasjon."""
    ref = ref - np.mean(ref)
    sig = sig - np.mean(sig)
    r_xy = np.correlate(sig, ref, mode='full')
    lags = np.arange(-(len(ref) - 1), len(sig))
    return int(lags[np.argmax(np.abs(r_xy))])


def beregn_vinkel_deg(n_21, n_31, n_32):
    """Beregn innfallsvinkel i grader via lign. (29)."""
    teller = np.sqrt(3) * (n_21 + n_31)
    nevner = n_21 - n_31 - 2 * n_32
    return float(np.degrees(np.arctan2(teller, nevner)))


def estimer_fra_fil(path):
    """Last inn én måling og returner estimert vinkel i grader."""
    sp, data_counts = raspi_import(str(path), channels=3)
    data_V = counts_til_volt(data_counts)
    m1, m2, m3 = data_V[:, 0], data_V[:, 1], data_V[:, 2]
    n_31 = finn_forsinkelse(m1, m3)
    n_21 = finn_forsinkelse(m1, m2)
    n_32 = finn_forsinkelse(m2, m3)
    theta = beregn_vinkel_deg(n_21, n_31, n_32)
    return theta, n_21, n_31, n_32, 1.0 / sp


# ===========================================================================
# Kjør analyse for alle vinkler
# ===========================================================================
resultater = {}   # nominell_vinkel -> {'thetas', 'mean', 'std', 'var'}

print("=" * 65)
print(f"{'Nominell':>10}  {'Maaling':>8}  {'n_21':>5}  {'n_31':>5}  "
      f"{'n_32':>5}  {'Estimert [deg]':>15}")
print("=" * 65)

for nom_deg, prefiks in VINKLER:
    thetas = []
    for i in range(1, N_MAALINGER + 1):
        filsti = BASE / f'{prefiks}_{i}'
        theta, n21, n31, n32, fs = estimer_fra_fil(filsti)
        thetas.append(theta)
        print(f"  {nom_deg:>8}°  {i:>8d}  {n21:>5d}  {n31:>5d}  {n32:>5d}  {theta:>14.1f}°")

    mean_t = float(np.mean(thetas))
    std_t  = float(np.std(thetas, ddof=1)) if len(thetas) > 1 else 0.0
    var_t  = std_t ** 2

    resultater[nom_deg] = {
        'thetas': thetas,
        'mean':   mean_t,
        'std':    std_t,
        'var':    var_t,
    }

    print(f"  {nom_deg:>8}°  {'STAT':>8}  {'':>5}  {'':>5}  {'':>5}  "
          f"mean={mean_t:.1f}°  std={std_t:.2f}°  var={var_t:.2f}°²")
    print("-" * 65)

print()

# ===========================================================================
# Sammendragstabell
# ===========================================================================
print("Sammendrag")
print(f"{'Nominell [deg]':>16}  {'Gjennomsnitt [deg]':>20}  "
      f"{'Std.avvik [deg]':>17}  {'Varians [deg²]':>16}")
print("-" * 74)
for nom_deg, res in resultater.items():
    print(f"  {nom_deg:>14}°  {res['mean']:>19.2f}°  "
          f"{res['std']:>16.3f}°  {res['var']:>15.3f}°²")


# ===========================================================================
# Plotting
# ===========================================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 6))

nom_vals  = list(resultater.keys())
means     = [resultater[n]['mean'] for n in nom_vals]
stds      = [resultater[n]['std']  for n in nom_vals]
colors    = ['tab:blue', 'tab:orange', 'tab:green']

# Venstre: alle enkeltmålinger + gjennomsnitt
for idx, (nom_deg, res) in enumerate(resultater.items()):
    x_vals = [nom_deg] * len(res['thetas'])
    axes[0].scatter(x_vals, res['thetas'], color=colors[idx], zorder=5,
                    s=60, label=f'{nom_deg}° (n={len(res["thetas"])})')
    axes[0].errorbar(nom_deg, res['mean'], yerr=res['std'],
                     fmt='D', color=colors[idx], capsize=6,
                     markersize=8, linewidth=2)

# Ideal linje
rng = np.array([min(nom_vals) - 20, max(nom_vals) + 20])
axes[0].plot(rng, rng, 'k--', linewidth=0.8, label='Ideal (y=x)')
axes[0].set(xlabel='Nominell innfallsvinkel [grader]',
            ylabel='Estimert innfallsvinkel [grader]',
            title='Oppgave 5 – Estimerte vinkler per måling\n'
                  '(diamant = gjennomsnitt ± std.avvik)',
            xticks=nom_vals)
axes[0].legend(fontsize=9)
axes[0].grid(True)

# Høyre: standardavvik og varians per vinkel
ax2 = axes[1].twinx()
bars = axes[1].bar([str(n) + '°' for n in nom_vals], stds,
                   color=colors, alpha=0.7, label='Std.avvik [deg]')
ax2.plot([str(n) + '°' for n in nom_vals], [resultater[n]['var'] for n in nom_vals],
         'ko--', markersize=7, linewidth=1.5, label='Varians [deg²]')

axes[1].set(xlabel='Nominell innfallsvinkel',
            ylabel='Standardavvik [grader]',
            title='Oppgave 5 – Usikkerhet per innfallsvinkel')
ax2.set_ylabel('Varians [grader²]')

lines1, labels1 = axes[1].get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
axes[1].legend(lines1 + lines2, labels1 + labels2, fontsize=9)
axes[1].grid(True, axis='y')

plt.suptitle('Laboppgave 5 – Systematisk variasjon av innfallsvinkel', fontsize=13)
plt.tight_layout()
plt.show()
