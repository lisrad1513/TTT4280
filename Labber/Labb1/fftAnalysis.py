import numpy as np
import matplotlib.pyplot as plt
from raspi_import import raspi_import

sample_period, data = raspi_import(
    'ELSYSS6/Sensor/Labber/Labb1/31250Samples1_65VOffset1_65V', 3
)

x = data.astype(np.float64)
x = x - np.mean(x, axis=0, keepdims=True)

N = x.shape[0]
fs = 1.0 / sample_period

w = np.hanning(N)[:, None]
xw = x * w

nfft = N  # set > N for zero padding if you want
X = np.fft.rfft(xw, n=nfft, axis=0)
freq = np.fft.rfftfreq(nfft, d=sample_period)

mag = np.abs(X) / N
if nfft > 1:
    mag[1:-1, :] *= 2.0

# Convert to dB
eps = 1e-12
mag_db = 20.0 * np.log10(mag + eps)

plt.figure()
for ch in range(mag_db.shape[1]):
    plt.plot(freq, mag_db[:, ch], label=f"Channel {ch}")

plotWholeSpectrum = False
if not plotWholeSpectrum:
    plt.xlim(0, 2000)
else:  
    plt.xlim(0, fs / 2)

plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True)
plt.legend()
plt.show()