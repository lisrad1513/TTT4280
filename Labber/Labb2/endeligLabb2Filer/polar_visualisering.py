"""
Polar visualisering
====================
Illustrerer estimerte innfallsvinkler i polare koordinater.

Viser:
  1. Alle enkeltmålinger som punkter på enhetssirkelen.
  2. Gjennomsnittlig estimert vinkel som pil.
  3. Nominell (sann) innfallsvinkel som stiplet pil.
  4. Usikkerhet (±1 std.avvik) som en bue rundt gjennomsnittspilen.
  5. Array-geometri: mikrofonposisjonene i eget polarplott.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

# ---------------------------------------------------------------------------
# Konfigurasjon
# ---------------------------------------------------------------------------
BASE = Path(__file__).parent.parent / 'endeligLabb2Maalinger' / 'konsekventTesting'

ADC_BITS   = 12
VREF       = 3.3
RESOLUTION = (2 ** ADC_BITS) - 1
c          = 343.0
a          = 0.05
d          = np.sqrt(3) * a

VINKLER = [
    (-120, 'pos1_degMin120', 'tab:blue'),
    ( -60, 'pos1_degMin60',  'tab:orange'),
    (  60, 'pos1_degPos60',  'tab:green'),
]
N_MAALINGER = 4


# ---------------------------------------------------------------------------
# Hjelpefunksjoner
# ---------------------------------------------------------------------------
def counts_til_volt(data):
    return (data / RESOLUTION) * VREF

def finn_forsinkelse(ref, sig):
    ref = ref - np.mean(ref)
    sig = sig - np.mean(sig)
    r   = np.correlate(sig, ref, mode='full')
    lags = np.arange(-(len(ref) - 1), len(sig))
    return int(lags[np.argmax(np.abs(r))])

def beregn_vinkel_rad(n_21, n_31, n_32):
    return np.arctan2(np.sqrt(3) * (n_21 + n_31), n_21 - n_31 - 2 * n_32)

def estimer_fra_fil(path):
    sp, data_counts = raspi_import(str(path), channels=3)
    V  = counts_til_volt(data_counts)
    m1, m2, m3 = V[:, 0], V[:, 1], V[:, 2]
    n_31 = finn_forsinkelse(m1, m3)
    n_21 = finn_forsinkelse(m1, m2)
    n_32 = finn_forsinkelse(m2, m3)
    return beregn_vinkel_rad(n_21, n_31, n_32)


# ---------------------------------------------------------------------------
# Samle målinger
# ---------------------------------------------------------------------------
resultater = {}
for nom_deg, prefiks, farge in VINKLER:
    thetas = [estimer_fra_fil(BASE / f'{prefiks}_{i}') for i in range(1, N_MAALINGER + 1)]
    thetas = np.array(thetas)
    resultater[nom_deg] = {
        'thetas': thetas,
        'mean':   float(np.mean(thetas)),
        'std':    float(np.std(thetas, ddof=1)) if len(thetas) > 1 else 0.0,
        'farge':  farge,
    }


# ===========================================================================
# Figur 1: Estimerte innfallsvinkler (polar)
# ===========================================================================
fig1 = plt.figure(figsize=(8, 8))
ax1  = fig1.add_subplot(111, projection='polar')

# Konvensjon: 0° = høyre (øst), positiv retning = mot klokken
# matplotlib polar: theta=0 peker til høyre, positiv = mot klokken – perfekt.

for nom_deg, res in resultater.items():
    nom_rad   = np.radians(nom_deg)
    mean_rad  = res['mean']
    std_rad   = res['std']
    farge     = res['farge']
    thetas    = res['thetas']

    # Enkeltmålinger som små prikker på r=1
    ax1.scatter(thetas, np.ones(len(thetas)), color=farge, s=60,
                zorder=5, alpha=0.85)

    # Gjennomsnittspil
    ax1.annotate('', xy=(mean_rad, 1.0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color=farge, lw=2.5))

    # Nominell pil (stiplet)
    ax1.annotate('', xy=(nom_rad, 1.0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color=farge, lw=1.5,
                                 linestyle='dashed', alpha=0.5))

    # ±1 std.avvik som bue på r = 0.95
    if std_rad > 0:
        bue_theta = np.linspace(mean_rad - std_rad, mean_rad + std_rad, 100)
        ax1.plot(bue_theta, np.full_like(bue_theta, 0.95),
                 color=farge, lw=3, alpha=0.4)

    # Etikett
    label_r = 1.17
    ax1.text(mean_rad, label_r,
             f'{np.degrees(mean_rad):.1f}°\n(nom. {nom_deg}°)',
             ha='center', va='center', fontsize=9, color=farge,
             fontweight='bold')

# Pynt
ax1.set_rmax(1.35)
ax1.set_rticks([])
ax1.set_theta_zero_location('E')   # 0° peker til høyre
ax1.set_theta_direction(1)          # positiv retning mot klokken
ax1.set_thetagrids(np.arange(0, 360, 30))
ax1.grid(True, alpha=0.3)
ax1.set_title('Estimerte innfallsvinkler\n(piler = gjennomsnitt, '
              'stiplet = nominell, bue = ±1 std.avvik)',
              pad=20, fontsize=12)

# Forklaring (manuell legend)
legend_elements = [
    mpatches.Patch(color=res['farge'],
                   label=f"Nominell {nom_deg}°: "
                         f"mean={np.degrees(res['mean']):.1f}°, "
                         f"std={np.degrees(res['std']):.1f}°")
    for nom_deg, res in resultater.items()
]
ax1.legend(handles=legend_elements, loc='lower center',
           bbox_to_anchor=(0.5, -0.12), fontsize=9)


# ===========================================================================
# Figur 2: Array-geometri i polar koordinater
# ===========================================================================
fig2 = plt.figure(figsize=(6, 6))
ax2  = fig2.add_subplot(111, projection='polar')

# Sensor-posisjoner (kartesisk -> polar)
sensorer = {
    'Sensor 1': np.array([0.0,              a]),
    'Sensor 2': np.array([-np.sqrt(3)/2*a, -a/2]),
    'Sensor 3': np.array([ np.sqrt(3)/2*a, -a/2]),
}
sensor_farger = ['tab:red', 'tab:purple', 'tab:brown']

for (navn, pos), farge in zip(sensorer.items(), sensor_farger):
    r_pos     = np.hypot(pos[0], pos[1])
    theta_pos = np.arctan2(pos[1], pos[0])
    ax2.scatter(theta_pos, r_pos * 100, color=farge, s=120, zorder=6)
    ax2.text(theta_pos, r_pos * 100 + 0.8, navn,
             ha='center', va='bottom', fontsize=10, color=farge, fontweight='bold')

# Tegn triangelet
pos_list  = list(sensorer.values()) + [list(sensorer.values())[0]]
for p1, p2 in zip(pos_list[:-1], pos_list[1:]):
    theta1, r1 = np.arctan2(p1[1], p1[0]), np.hypot(p1[0], p1[1]) * 100
    theta2, r2 = np.arctan2(p2[1], p2[0]), np.hypot(p2[0], p2[0]) * 100
    # Tegn som rett linje i kartesisk, konverter til mange polarpunkter
    t_vals = np.linspace(0, 1, 100)
    px = p1[0] + t_vals * (p2[0] - p1[0])
    py = p1[1] + t_vals * (p2[1] - p1[1])
    ax2.plot(np.arctan2(py, px), np.hypot(px, py) * 100,
             'k-', lw=1.2, alpha=0.4)

# Innfallsretninger
for nom_deg, res in resultater.items():
    nom_rad  = np.radians(nom_deg)
    mean_rad = res['mean']
    farge    = res['farge']
    # Pil fra utenfor arrayet inn mot sentrum (innfallsretning)
    r_start = 7.5
    ax2.annotate('', xy=(nom_rad + np.pi, 0.5), xytext=(nom_rad + np.pi, r_start),
                 arrowprops=dict(arrowstyle='->', color=farge, lw=1.5,
                                 linestyle='dashed', alpha=0.5))
    ax2.annotate('', xy=(mean_rad + np.pi, 0.5), xytext=(mean_rad + np.pi, r_start),
                 arrowprops=dict(arrowstyle='->', color=farge, lw=2.0))

ax2.set_rmax(9)
ax2.set_rticks([a * 100])
ax2.set_yticklabels([f'{a*100:.0f} cm'])
ax2.set_theta_zero_location('E')
ax2.set_theta_direction(1)
ax2.set_thetagrids(np.arange(0, 360, 30))
ax2.grid(True, alpha=0.3)
ax2.set_title('Array-geometri og innfallsretninger\n'
              '(stiplet = nominell, hel = estimert gjennomsnitt)',
              pad=20, fontsize=11)

legend2 = [
    mpatches.Patch(color=res['farge'], label=f'Nominell {nom_deg}°')
    for nom_deg, res in resultater.items()
]
ax2.legend(handles=legend2, loc='lower center',
           bbox_to_anchor=(0.5, -0.12), fontsize=9)

plt.show()
