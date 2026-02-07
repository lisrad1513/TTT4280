import numpy as np
import matplotlib.pyplot as plt
import csv

# -----------------------------
# Load data
# -----------------------------
header = []
data1 = []
filename1 = "ELSYSS6/Sensor/Labber/Labb1/Clock and enable/ClockAndEnableSignal.csv"

with open(filename1, mode="r") as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

time = np.array([p[0] for p in data1], dtype=float) * 1e6  # [µs]
v1 = np.array([p[1] for p in data1], dtype=float)
v2 = np.array([p[2] for p in data1], dtype=float)

# -----------------------------
# Cycle settings
# -----------------------------
padding = 0.4  # [µs]

startCycle = (1.963044748695652) * 1e6  # [µs]
endCycle   = (1.963052708695652) * 1e6  # [µs]

oneCycle = (endCycle - startCycle) / 4    # [µs]
oneFullCycle = 16
amountOfCycles = 16

start = startCycle - padding
end = (startCycle + amountOfCycles * oneCycle)

# -----------------------------
# Prettier plot defaults
# -----------------------------
plt.close("all")
plt.rcParams.update({
    "figure.figsize": (10, 6),
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

ax.set_title("Klokke og 'Chip Select' over 16 klokkesykluser")
ax.set_xlabel("Time [µs]")
ax.set_ylabel("Voltage [V]")

ax.plot(time, v1, label="Klokke", linewidth=1.5)
ax.plot(time, v2, label="'Chip Select'", linewidth=1.5)

ax.set_xlim(start, end)
ax.grid(True, which="both")
ax.legend(loc="upper right")

# -----------------------------
# Add cycle numbers 1..16
# -----------------------------
y_min = float(min(v1.min(), v2.min()))
y_max = float(max(v1.max(), v2.max()))
y_span = (y_max - y_min) if y_max > y_min else 1.0

# Put the numbers a bit above the signals
y_numbers = y_max + 0 * y_span

# Draw a light vertical line at each cycle boundary and label the cycle number in the middle
for k in range(amountOfCycles):
    left = startCycle + k * oneCycle
    right = startCycle + (k + 1) * oneCycle
    mid = 0.5 * (left + right)

    # Boundary line at the start of each cycle
    ax.axvline(left, linewidth=1.0, alpha=0.25)

    # Number in the middle of each cycle
    ax.text(mid, y_numbers, f"{k+1}", ha="center", va="bottom")

# Also draw the final boundary
ax.axvline(startCycle + amountOfCycles * oneCycle, linewidth=1.0, alpha=0.25)

# Make sure labels fit inside the plot
ax.set_ylim(y_min - 0.05 * y_span, y_max + 0.42 * y_span)

# Optional: show a bracket for one cycle above the first cycle
y_bracket = y_max + 0.16 * y_span
ax.annotate(
    "",
    xy=(startCycle + oneCycle, y_bracket),
    xytext=(startCycle, y_bracket),
    arrowprops=dict(arrowstyle="|-|", lw=1.6, alpha=0.9),
)
ax.text(
    startCycle + 1.3 * oneCycle,
    y_bracket + 0.08 * y_span,
    f"1 sykel = {oneCycle:.3f} µs",
    ha="center",
    va="bottom"
)

fig.tight_layout()
plt.show()
