import numpy as np
import matplotlib.pyplot as plt
import csv

header = []
data1 = []
filename1 = 'ELSYSS6/Sensor/Labber/Labb1/Clock and enable/ClockAndEnableSignal.csv'

with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

time = [p[0] for p in data1]
v1 = [p[1] for p in data1]
v2 = [p[2] for p in data1]

# Format time to microseconds
time = [t * 1e6 for t in time]  # [µs]

plt.close("all")
fig, ax = plt.subplots(figsize=(8, 6), dpi=120)

ax.set_xlabel("Tid [µs]")
ax.set_ylabel("Spenning [V]")
ax.set_title(r"Én klokkesyklus")

ax.axhline(y=0, color='black', linestyle='-', linewidth=1.0, alpha=0.6)
ax.plot(time, v1, label=r"Klokkesignal", linewidth=2.2)
#ax.plot(time, v2, label=r"Enable", linewidth=2.2)


startCycle = (1.963044748695652) * 1e6  # [µs]
endCycle   = (1.963052708695652) * 1e6  # [µs]

oneCycle = (endCycle - startCycle) / 4  # [µs]

start_display =(1.963043928695652) * 1e6
end_display = (1.963047438695652) * 1e6


start = start_display
end = end_display

ax.set_xlim(start, end)

ax.grid(True, which="both", alpha=0.25, linestyle=":", linewidth=0.8)



ax.legend()

# -----------------------------
# Add |---| marker for one cycle
# -----------------------------
# Choose a y-position slightly above the visible signals
y_min = min(min(v1), min(v2))
y_max = max(max(v1), max(v2))
y_span = y_max - y_min if y_max > y_min else 1.0

y_bracket = y_max - 0 * y_span  # put it above the waveforms

# Draw the bracket from startCycle to endCycle
ax.annotate(
    "",  # no text here, just the bracket line
    xy=(startCycle + oneCycle, y_bracket),
    xytext=(startCycle, y_bracket),
    arrowprops=dict(arrowstyle="|-|", lw=1.8)
)

# Put a label centered above the bracket
x_mid = 0.5 * (startCycle + (startCycle + oneCycle))
ax.text(
    x_mid,
    y_bracket + 0.04 * y_span,
    rf"1 syklus = {oneCycle:.3f} µs",
    ha="center",
    va="bottom"
)

#ax.axvline(startCycle, linewidth=1.0, alpha=0.25)
#ax.axvline(startCycle + oneCycle, linewidth=1.0, alpha=0.25)


# Make sure the bracket is inside the view
ax.set_ylim(y_min - 0.05 * y_span, y_max + 0.25 * y_span)

plt.show()
