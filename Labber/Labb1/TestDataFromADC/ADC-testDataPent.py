import numpy as np
import matplotlib.pyplot as plt

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

# -----------------------------
# Settings
# -----------------------------
channels = 3
freqIn = 1000  # Hz

periodsCount = 10
periodTime = 1.0 / freqIn
rangePeriod = periodsCount * periodTime  # seconds

Vref = 3.3
resolution = (2**12) - 1  # 12-bit ADC
Voffset = Vref / 2.0

def counts_to_volts(counts):
    return (counts / resolution) * Vref

# -----------------------------
# Load data
# -----------------------------
sample_period, data = raspi_import(
    f"ELSYSS6/Sensor/Labber/Labb1/{freqIn}Hz/31250Samples1_65VOffset1_65V{freqIn}Hz",
    channels
)

N_total = data.shape[0]
fs = 1.0 / sample_period

time_s = np.arange(N_total) * sample_period
v = counts_to_volts(data)

# Show exactly the requested time window
mask = (time_s >= 0.0) & (time_s <= rangePeriod)
time_ms = time_s[mask] * 1e3
v_view = v[mask, :]

N_shown = v_view.shape[0]
t_start_ms = float(time_ms[0]) if N_shown > 0 else 0.0
t_end_ms = float(time_ms[-1]) if N_shown > 0 else rangePeriod * 1e3

# -----------------------------
# Styling
# -----------------------------
plt.close("all")
plt.rcParams.update({
    "figure.figsize": (8, 6),
    "figure.dpi": 140,
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "font.size": 11,
    "lines.linewidth": 2.2,
    "grid.alpha": 0.25,
    "grid.linestyle": ":",
    "grid.linewidth": 0.8,
    "legend.frameon": True,
    "legend.framealpha": 0.95,
    "legend.fancybox": True,
})

colors = ["royalblue", "darkorange", "seagreen"]

fig, axs = plt.subplots(channels, 1, sharex=True, sharey=True)

# Reference lines (same on all)
ref_levels = [
    (0.0, "0 V"),
    (Voffset, "1.65 V"),
    (Vref, "3.3 V"),
]

for i in range(channels):
    ax = axs[i]

    # Signal
    ax.plot(time_ms, v_view[:, i], color=colors[i], label=f"ADC {i+1}")

    # Reference lines
    for y, _ in ref_levels:
        ax.axhline(y=y, linestyle="--", linewidth=1.2, alpha=0.35)

    # Label the reference lines on the right side (cleaner than legend spam)
    x_text = t_end_ms
    x_pad = 0.01 * (t_end_ms - t_start_ms) if t_end_ms > t_start_ms else 0.1
    for y, lab in ref_levels:
        ax.text(
            x_text + x_pad,
            y,
            lab,
            va="center",
            ha="left",
            fontsize=10,
            alpha=0.75,
            clip_on=False
        )

    # Axis labels and titles
    ax.set_ylabel("Spenning [V]")
    ax.set_title(f"Dital Data fra ADC {i+1}")
    ax.grid(True, which="both")

    # Info box per subplot
    # info = (
    #     f"fs = {fs:.1f} Hz\n"
    #     f"dt = {sample_period*1e6:.2f} µs\n"
    #     f"N shown = {N_shown}\n"
    #     f"Vref = {Vref:.2f} V"
    # )
    # ax.text(
    #     0.01, 0.96,
    #     info,
    #     transform=ax.transAxes,
    #     va="top",
    #     ha="left",
    #     bbox=dict(boxstyle="round,pad=0.3", alpha=0.10, linewidth=0.8)
    #)

axs[-1].set_xlabel("Time [ms]")

# Limits
axs[0].set_xlim(t_start_ms, t_end_ms)
axs[0].set_ylim(-0.2, 3.5)

# One shared legend for the ADC traces only
# handles, labels = axs[0].get_legend_handles_labels()
# fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.98, 0.98))

fig.suptitle(
    f"Digital data fra alle {channels} ADC-ene, frekvens {freqIn} Hz",
    y=0.965
)

# Extra right margin so the right side reference labels fit
fig.tight_layout(rect=[0.0, 0.0, 0.92, 0.97])
plt.show()
