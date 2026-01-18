import numpy as np
import matplotlib.pyplot as plt

# Given
A = 1.0
f0 = 100.0
deltaT = 0.2e-3
fs = 1 / deltaT
N = 900

# Time signal
t = np.arange(N) * deltaT
x = A * np.sin(2 * np.pi * f0 * t)

def spectrum_2d(x, sample_period):
    x = x.astype(np.float64)

    # Remove DC
    x = x - np.mean(x)

    fs = 1.0 / sample_period
    NFFT = len(x)

    # Full FFT (length NFFT)
    X = np.fft.fft(x)

    # Frequency axis 0 to fs (NFFT points)
    freq = np.arange(NFFT) * fs / NFFT

    # 2d wants: 20*log10(|X(f)|)
    mag_db = 20 * np.log10(np.abs(X) + 1e-20)

    # Normalize so max becomes 0 dB
    rel_db = mag_db - np.max(mag_db)

    return freq, rel_db, NFFT

freq, rel_db, NFFT = spectrum_2d(x, deltaT)

delta_f = fs / NFFT
print(f"NFFT = {NFFT}")
print(f"fs = {fs} Hz")
print(f"Δf = {delta_f} Hz")
print(f"Mirror frequency = {fs - f0} Hz")

plt.plot(freq, rel_db)
plt.title("Normalized spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Relativ effekt, [dB]")
plt.xlim(0, fs)          # 0 to 5 kHz
plt.ylim(-80, 10)        # suggested range in task
plt.grid(True)
plt.show()