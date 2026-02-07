import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

# -----------------------------
# Settings
# -----------------------------
channels = 3
channel = 0              # which ADC channel to compare
targetFreq = 1000        # Hz

windowFunction = "hann"  # 'none', 'hann', 'hamming', 'blackman', 'bartlett'
nfftChooser = True       # True: nfft = next pow2 above N

plotWholeSpectrum = 1    # 0: 600..2300, 1: 0..fs/2, 2: zoom around target

# Files
sample_period1, data1 = raspi_import(
    f"ELSYSS6/Sensor/Labber/Labb1/1000Hz/31250Samples1_65VOffset1_65V1000Hz",
    channels
)
sample_period2, data2 = raspi_import(
    "ELSYSS6/Sensor/Labber/Labb1/ADCMedUtenFilter/31250Samples1_65VOffset1_65V1000HzUtenFilter",
    channels
)

# -----------------------------
# Prepare signals (same length)
# -----------------------------
x1 = data1.astype(np.float64)
x2 = data2.astype(np.float64)

x1 = x1 - np.mean(x1, axis=0, keepdims=True)
x2 = x2 - np.mean(x2, axis=0, keepdims=True)

N1 = x1.shape[0]
N2 = x2.shape[0]
N = min(N1, N2)

x1 = x1[:N, :]
x2 = x2[:N, :]

fs1 = 1.0 / sample_period1
fs2 = 1.0 / sample_period2

# -----------------------------
# Window
# -----------------------------
if windowFunction == "none":
    w = np.ones((N, 1))
elif windowFunction == "hann":
    w = np.hanning(N)[:, None]
elif windowFunction == "hamming":
    w = np.hamming(N)[:, None]
elif windowFunction == "blackman":
    w = np.blackman(N)[:, None]
elif windowFunction == "bartlett":
    w = np.bartlett(N)[:, None]
else:
    print("Unknown window function, defaulting to none.")
    w = np.ones((N, 1))
    windowFunction = "none"

xw1 = x1 * w
xw2 = x2 * w

# -----------------------------
# nfft + FFT
# -----------------------------
if nfftChooser:
    nfft = 2 ** int(np.ceil(np.log2(N)))
else:
    nfft = N

X1 = np.fft.rfft(xw1, n=nfft, axis=0)
X2 = np.fft.rfft(xw2, n=nfft, axis=0)

freq1 = np.fft.rfftfreq(nfft, d=sample_period1)
freq2 = np.fft.rfftfreq(nfft, d=sample_period2)

mag1 = np.abs(X1) / N
mag2 = np.abs(X2) / N

if nfft > 1:
    mag1[1:-1, :] *= 2.0
    mag2[1:-1, :] *= 2.0

eps = 1e-12
mag_db1 = 20.0 * np.log10(mag1 + eps)
mag_db2 = 20.0 * np.log10(mag2 + eps)

# -----------------------------
# Pretty plotting (same style as your other figure)
# -----------------------------
plt.close("all")
plt.rcParams.update({
    "figure.figsize": (8, 6),
    "figure.dpi": 140,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "font.size": 11,
    "lines.linewidth": 2.0,
    "grid.alpha": 0.25,
    "grid.linestyle": ":",
    "grid.linewidth": 0.8,
    "legend.frameon": True,
    "legend.framealpha": 0.95,
    "legend.fancybox": True,
})

fig, ax = plt.subplots()

colors = ["royalblue", "darkorange", "seagreen", "crimson"]

# Plot: without filter (lighter) and with filter (solid)
ax.plot(
    freq2, mag_db2[:, channel],
    label=f"ADC {channel+1} uten filter",
    color=colors[2],
    alpha=1.0
)
ax.plot(
    freq1, mag_db1[:, channel],
    label=f"ADC {channel+1} med filter",
    color=colors[1],
    alpha=1.0
)

# Target frequency marker (same as before)
ax.axvline(targetFreq, linestyle="--", color=colors[3], linewidth=1.6, alpha=0.8)
ax.text(
    targetFreq + 50, 0.04,
    f"Analog frekvens: {targetFreq} Hz",
    transform=ax.get_xaxis_transform(),
    ha="left", va="top",
    fontsize=10,
    color=colors[3]
)

# Same arrows format
if plotWholeSpectrum == 0:
    textPos = (1500, 60)  # in data coords
    start = (textPos[0], textPos[1] - 2.0)

    arrowPoints = [(1251, -4.8), (1500, -15), (1751, -6), (2000, 44)]

    ax.text(
        textPos[0], textPos[1],
        "Støy og overtone",
        ha="center", va="center"
    )

    for tip in arrowPoints:
        arrow = FancyArrowPatch(
            posA=(start[0], start[1] - 0.6 if tip[1] > 22 else start[1]),  # Start of the arrow, with optional offset
            posB=tip,
            arrowstyle="->",
            mutation_scale=15,
            linewidth=1.6,
            color="black"
        )
        arrow.set_clip_on(False)
        ax.add_patch(arrow)


# X limits
if plotWholeSpectrum == 0:
    ax.set_xlim(400, 2300)
elif plotWholeSpectrum == 1:
    ax.set_xlim(0, fs1 / 2.0)
else:
    ax.set_xlim(targetFreq - 50, targetFreq + 50)

ax.set_xlabel("Frekvens [Hz]")
ax.set_ylabel("Magnitude [dB]")
ax.set_title("FFT analyse av ADC data: med og uten filter")

ax.grid(True, which="both")
#If plotWholeSpectrum = 0, loc = "upper left", while plotWholeSpectrum = 1 or 2, loc = "upper right" to avoid overlapping the target frequency marker
if plotWholeSpectrum == 0:
    ax.legend(loc="upper left")
else:
    ax.legend(loc="upper right")

fig.tight_layout()
plt.show()
