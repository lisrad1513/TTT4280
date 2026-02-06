import numpy as np
import matplotlib.pyplot as plt
import csv

# -----------------------------
# Data loading
# -----------------------------
header = []
data1 = []
data2 = []

filename1 = 'ELSYSS6/Sensor/Labber/Labb1/Filter/Filter0Ohm501Steps.csv'
filename2 = 'ELSYSS6/Sensor/Labber/Labb1/Filter/Filter15Ohm501Steps.csv'

with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

with open(filename2, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data2.append(values)

freq1 = np.array([p[0] for p in data1], dtype=float)
db1   = np.array([p[2] for p in data1], dtype=float)

freq2 = np.array([p[0] for p in data2], dtype=float)
db2   = np.array([p[2] for p in data2], dtype=float)

# -----------------------------
# Plot parameters
# -----------------------------
upperLimit = 300  # Hz

fc_0  = 30.90
fc_15 = 24.55
db_cut = -3.0

title_khz = np.round(upperLimit / 1000.0, 1)

# -----------------------------
# Prettier plot
# -----------------------------
plt.close("all")

plt.rcParams.update({
    "figure.figsize": (10, 5.6),
    "figure.dpi": 120,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "axes.grid": True,
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

# Curves
ax.plot(freq1, db1, label=r"Filter ved $R_F = 0 \Omega$")
ax.plot(freq2, db2, label=r"Filter ved $R_F = 15 \Omega$")

# Cutoff lines (keep them subtle)
ax.axhline(db_cut, linestyle="--", linewidth=1.6, alpha=0.8, label="Knekkfrekvens")
ax.axvline(fc_0,  linestyle="--", linewidth=1.6, alpha=0.8)
ax.axvline(fc_15, linestyle="--", linewidth=1.6, alpha=0.8)

# Annotations instead of huge legend text
# ax.annotate(r"$-3$ dB",
#             xy=(1.1, db_cut), xycoords=("data", "data"),
#             xytext=(10, 6), textcoords="offset points",
#             va="bottom", ha="left")

ax.annotate(r"$f_{c_0} \approx 30.90$ Hz (0 $\Omega$)",
            xy=(fc_0, np.interp(fc_0, freq1, db1)),
            xytext=(40, 50), textcoords="offset points",
            arrowprops=dict(arrowstyle="->", lw=1.0),
            ha="left", va="top")

ax.annotate(r"$f_{c_{15}} \approx 24.55$ Hz (15 $\Omega$)",
            xy=(fc_15, np.interp(fc_15, freq2, db2)),
            xytext=(-120, -50), textcoords="offset points",
            arrowprops=dict(arrowstyle="->", lw=1.0),
            ha="left", va="bottom")

# Axes formatting
ax.set_xscale("log")
ax.set_xlim(1, upperLimit)
ax.set_ylim(-45, 12)

ax.set_xlabel("Frekvens [Hz]")
ax.set_ylabel("Demping [dB]")
ax.set_title(f"Amplituderespons til filteret mellom 1 Hz og {title_khz} kHz")

# Minor grid looks great on log axis
ax.grid(True, which="major")
ax.grid(True, which="minor", alpha=0.38)

# Legend placed outside so it never hides data
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0)

fig.tight_layout()
plt.show()
