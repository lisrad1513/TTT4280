"""
Forberedelsesoppgave 2
======================

(a) Maksimalt antall sampler med forsinkelse for et triangelarray

    For to sensorer med avstand d og lydhastighet c, er maksimal gangveisforskjell
    lik d (når lyden treffer sensorene akkurat på rekke). Tilsvarende tidsforsinkelse:

        tau_max = d / c

    Omregnet til antall sampler:

        n_max = tau_max * fs = d * fs / c

    Eksempel: d = sqrt(3)*a med a = 5 cm  =>  d ≈ 8.66 cm
        n_max = 0.0866 * 31250 / 343 ≈ 7.9  =>  avrund ned til 7 sampler

(b) Unike innfallsvinkler med to mikrofoner – 2 vs. 4 sampler maks forsinkelse

    Med kun to mikrofoner og maks forsinkelse N sampler er de mulige
    heltallsverdiene for n_21:  {-N, -(N-1), ..., -1, 0, 1, ..., N-1, N}
    Det gir (2*N + 1) mulige forsinkelseverdier, og dermed (2*N + 1) unike vinkelbånd.

    For N = 2:  5 unike forsinkelseverdier  =>  5 unike vinkelbånd
    For N = 4:  9 unike forsinkelseverdier  =>  9 unike vinkelbånd

    Konklusjon: 4 sampler gir flere unike vinkler enn 2 sampler.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Systemparametere (juster etter din oppsett)
# ---------------------------------------------------------------------------
c  = 343.0     # Lydhastighet [m/s]
fs = 31250     # Samplingsfrekvens [Hz]
a  = 0.05      # Halvside av triangelet [m] (sensor 1 er i [0, a])
d  = np.sqrt(3) * a   # Sidelengde i det likesidede triangelet [m]


# ===========================================================================
# Del (a): Maks antall sampler med forsinkelse
# ===========================================================================
def maks_forsinkelse_sampler(d, fs, c=343.0):
    """
    Beregn maks antall sampler forsinkelse for to sensorer i avstand d.

    n_max = floor(d * fs / c)
    """
    n_max_eksakt = d * fs / c
    n_max = int(np.floor(n_max_eksakt))
    return n_max, n_max_eksakt


print("=" * 60)
print("Del (a): Maksimalt antall sampler med forsinkelse")
print("=" * 60)

n_max, n_max_eksakt = maks_forsinkelse_sampler(d, fs, c)
print(f"  Sidelengde d          = {d*100:.2f} cm  (a = {a*100:.1f} cm, d = sqrt(3)*a)")
print(f"  Samplingsfrekvens fs  = {fs} Hz")
print(f"  Lydhastighet c        = {c} m/s")
print(f"  n_max = d*fs/c        = {d:.4f} * {fs} / {c} = {n_max_eksakt:.2f}")
print(f"  Avrundet ned:  n_max  = {n_max} sampler")
print(f"\n  Forsinkelse kan altså ligge i [{-n_max}, ..., 0, ..., {n_max}] sampler.")

# Variasjon med forskjellige d-verdier
print("\n  Tabell over n_max for ulike sidelengder (fs = 31250 Hz):")
print(f"  {'d [cm]':>8}  {'n_max (eksakt)':>15}  {'n_max (floor)':>14}")
for d_cm in [3, 5, 8, 10, 15, 20]:
    d_m = d_cm / 100
    nm, nm_eks = maks_forsinkelse_sampler(d_m, fs, c)
    print(f"  {d_cm:>8.1f}  {nm_eks:>15.2f}  {nm:>14d}")


# ===========================================================================
# Del (b): Unike vinkler med 2 mikrofoner – sammenligning 2 vs. 4 sampler
# ===========================================================================
print("\n" + "=" * 60)
print("Del (b): Unike innfallsvinkler – maks 2 vs. 4 sampler forsinkelse")
print("=" * 60)

def unike_vinkler_to_mikrofoner(n_max, d_mic):
    """
    Beregn de unike estimerte innfallsvinklene for et to-mikrofonarray
    med maks forsinkelse n_max sampler og mikrofon-avstand d_mic.

    Vinkel fra n_21:  cos(alpha) = -c * tau_21 / d  =>  alpha = arccos(-c*n_21/(fs*d))
    Merk: alpha er vinkelen mellom x og x_21-vektoren, så innfallsvinkelen
    theta = +/- alpha (tvetydighet med bare to mikrofoner).
    Vi lister kun unike alpha-verdier.
    """
    vinkler = []
    for n in range(-n_max, n_max + 1):
        cos_alpha = -c * n / (fs * d_mic)
        if -1.0 <= cos_alpha <= 1.0:
            alpha_deg = np.degrees(np.arccos(cos_alpha))
            vinkler.append((n, alpha_deg))
    return vinkler

for n_max_b, label in [(2, "2 sampler"), (4, "4 sampler")]:
    vinkler = unike_vinkler_to_mikrofoner(n_max_b, d)
    unike_antall = len(set(round(v, 1) for _, v in vinkler))
    print(f"\n  Maks forsinkelse = {n_max_b} sampler:")
    print(f"  Mulige n_21-verdier: {list(range(-n_max_b, n_max_b + 1))}")
    print(f"  Antall unike vinkler (alpha): {unike_antall}")
    print(f"  {'n_21':>6}  {'alpha [deg]':>12}")
    for n, alpha in vinkler:
        print(f"  {n:>6d}  {alpha:>12.1f}")

print("\n  Konklusjon: Med 4 sampler maks forsinkelse kan man skille mellom")
print("  flere unike innfallsretninger enn med 2 sampler maks forsinkelse.")
print("  (9 mot 5 unike vinkelbånd for dette arrayoppsettet.)")


# ===========================================================================
# Plotting
# ===========================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Del a) – n_max som funksjon av d
d_vals = np.linspace(0.01, 0.25, 300)
n_max_vals = d_vals * fs / c

axes[0].plot(d_vals * 100, n_max_vals)
axes[0].axvline(d * 100, color='r', linestyle='--',
                label=f'Vår oppsett: d = {d*100:.1f} cm, n_max ≈ {n_max}')
axes[0].set(xlabel='Sidelengde d [cm]', ylabel='n_max [sampler]',
            title=f'(a) Maks forsinkelse i sampler\n(fs = {fs} Hz, c = {c} m/s)')
axes[0].legend(); axes[0].grid(True)

# Del b) – unike vinkler for N=2 og N=4
theta_kontinuerlig = np.linspace(0, 180, 1000)
for n_max_b, color, label in [(2, 'tab:blue', 'n_max = 2'), (4, 'tab:orange', 'n_max = 4')]:
    vinkler = unike_vinkler_to_mikrofoner(n_max_b, d)
    v_vals = [v for _, v in vinkler]
    axes[1].scatter(v_vals, [n_max_b] * len(v_vals), color=color, s=80,
                    zorder=5, label=f'{label}: {len(v_vals)} vinkler')

axes[1].set(xlabel='Estimert alpha [grader]', ylabel='n_max [sampler]',
            title='(b) Unike vinkler for 2 vs. 4 sampler maks forsinkelse',
            yticks=[2, 4])
axes[1].legend(); axes[1].grid(True)

# Subplot-etiketter
for ax, label in zip(axes, ['(a)', '(b)']):
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')

plt.suptitle('Forberedelsesoppgave 2', fontsize=13)
plt.tight_layout()
plt.show()
