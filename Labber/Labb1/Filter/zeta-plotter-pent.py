# A script that displays 5 values for zeta, and the corresponding filter response plots
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
zeta_values = [0.1, 0.45, 0.5, 0.55, 1.0]
f0 = 1000.0  # Natural frequency [Hz]
frequencies = np.logspace(1, 5, 2000)  # 10 Hz to 100 kHz

L = 100e-3
C = 470e-6

def findRfromZeta(zeta, L=L, C=C):
    """
    Calculate resistance R for a given damping ratio zeta,
    inductance L, and capacitance C.

    For a 2nd order RLC: zeta = (R/2)*sqrt(C/L)
    => R = 2*zeta*sqrt(L/C)
    """
    return 2.0 * zeta * np.sqrt(L / C)

# -----------------------------
# Prettier plotting defaults
# -----------------------------
plt.close("all")
plt.rcParams.update({
    "figure.figsize": (10, 5.6),
    "figure.dpi": 120,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "grid.alpha": 0.25,
    "grid.linestyle": ":",
    "grid.linewidth": 0.8,
    "lines.linewidth": 2.2,
    "legend.frameon": True,
    "legend.framealpha": 0.9,
    "legend.fancybox": True,
    "font.size": 11,
})

fig, ax = plt.subplots()

# -----------------------------
# Plot responses
# -----------------------------
for zeta in zeta_values:
    x = frequencies / f0
    H = 1.0 / np.sqrt((1.0 - x**2)**2 + (2.0 * zeta * x)**2)
    H_db = 20.0 * np.log10(H)

    ax.plot(frequencies, H_db, label=rf"$\zeta = {zeta}$")

    R = findRfromZeta(zeta)
    print(f"For zeta = {zeta}, R = {R:.2f} Ohms")

# Reference lines
ax.axhline(-3.0, linestyle="--", linewidth=1.6, alpha=0.8, label="Knekkfrekvens, -3 dB")
# ax.annotate(r"$-3$ dB", xy=(frequencies[0], -3.0), xytext=(10, 6),
#             textcoords="offset points", ha="left", va="bottom")

# Axes formatting
ax.set_xscale("log")
ax.set_xlim(10, 10000)
ax.set_ylim(-30, 15)

ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel(r"Magnitude [dB]")
ax.set_title("Filterrespons for ulike dempningsfaktorer")

# Grid: major + minor looks great on log axes
ax.grid(True, which="major")
ax.grid(True, which="minor", alpha=0.38)

# Legend outside so it never blocks curves
ax.legend(title="Dempningsfaktorer", loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0)

fig.tight_layout()
plt.show()
