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
freqIn = 1000  # Hz
targetFreq = freqIn  # Hz

# Choose input file
sample_period, data = raspi_import(
    "ELSYSS6/Sensor/Labber/Labb1/ADCMedUtenFilter/31250Samples1_65VOffset1_65V1000HzUtenFilter",
    channels
)

# Window functions: 'none', 'hann', 'hamming', 'blackman', 'bartlett'
windowFunction = "hann"

# Zero padding choice
nfftChooser = True  # True: nfft = next power of 2 above N, False: nfft = N

# Plot range mode
# 0: 0..3000 Hz
# 1: 0..fs/2
# 2: zoom near targetFreq
plotWholeSpectrum = 0

# -----------------------------
# Prepare signal
# -----------------------------
x = data.astype(np.float64)
x = x - np.mean(x, axis=0, keepdims=True)

N = x.shape[0]
fs = 1.0 / sample_period

# Window
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

xw = x * w

# nfft
if nfftChooser:
    nfft = 2 ** int(np.ceil(np.log2(N)))
else:
    nfft = N

# FFT
X = np.fft.rfft(xw, n=nfft, axis=0)
freq = np.fft.rfftfreq(nfft, d=sample_period)

mag = np.abs(X) / N
if nfft > 1:
    mag[1:-1, :] *= 2.0

eps = 1e-12
mag_db = 20.0 * np.log10(mag + eps)

# -----------------------------
# Pretty plotting
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

for ch in range(mag_db.shape[1]):
    ax.plot(freq, mag_db[:, ch], label=f"ADC {ch+1}", color=colors[ch % len(colors)])

# Target frequency marker
ax.axvline(targetFreq, linestyle="--", color=colors[3], linewidth=1.6, alpha=0.8,)
ax.text(
    targetFreq + 50, 0.04,
    f"Analog frekvens: {targetFreq} Hz",
    transform=ax.get_xaxis_transform(),
    ha="left",
    va="top",
    fontsize=10,
    color=colors[3]
)

textPos = (1500, 60)  # common start point in data coords
start = (textPos[0], textPos[1] - 2)  # tweak the -2 to taste
arrowPoints = [(1251, -4.8), (1500, -15), (1751, -6), (2000, 44)]

# 1) Place the text (centered exactly at textPos)
ax.text(
    textPos[0], textPos[1],
    "Støy og overtone",
    ha="center", va="center"
)

# 2) Draw all arrows from the exact same start point
for tip in arrowPoints:
    arrow = FancyArrowPatch(
        posA=(start[0], start[1] - 0.6 if tip[1] > 22 else start[1]),  # Start of the arrow, with optional offset
        posB=tip,  # Tip of the arrow
        arrowstyle="->",
        mutation_scale=15,     # arrow head size
        linewidth=1.6,
        color="black"
    )
    arrow.set_clip_on(False)
    ax.add_patch(arrow)



# X limits
if plotWholeSpectrum == 0:
    ax.set_xlim(400, 2300)
elif plotWholeSpectrum == 1:
    ax.set_xlim(0, fs / 2.0)
else:
    ax.set_xlim(targetFreq - 20, targetFreq + 20)

ax.set_xlabel("Frekvens [Hz]")
ax.set_ylabel("Magnitude [dB]")
ax.set_title("FFT analyse av ADC data")

ax.grid(True, which="both")
ax.legend(loc="upper left")

# # Helpful info box
# df = fs / nfft
# info = (
#     f"N = {N}\n"
#     f"fs = {fs:.1f} Hz\n"
#     f"nfft = {nfft}\n"
#     f"Δf = {df:.3f} Hz\n"
#     f"Window = {windowFunction}"
# )
# ax.text(
#     0.01, 0.99, info,
#     transform=ax.transAxes,
#     ha="left", va="top",
#     bbox=dict(boxstyle="round,pad=0.35", alpha=0.10, linewidth=0.8)
# )

fig.tight_layout()
plt.show()
