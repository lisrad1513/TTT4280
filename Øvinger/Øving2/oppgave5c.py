import numpy as np
import matplotlib.pyplot as plt

dt = 0.2e-3   # Sampling interval [s]
fs = 1 / dt    # Sampling frequency [Hz]
f0 = 100.0    # Signal frequency [Hz]
w0 = 2 * np.pi * f0  # Angular frequency [rad/s]
N = 900       # Number of samples

t = np.arange(N) * dt  # Time vector [s]
NFFT = 4096  # Number of points in FFT (next power of 2 above N)
df = fs / NFFT          # Frequency resolution
f = np.arange(NFFT) * df  # Frequency vector

x = np.exp(1j * w0 * t)  # Complex exponential signal
X = np.fft.fft(x, n=NFFT)  # FFT computation
X_mag = np.abs(X)
X_mag[X_mag == 0] = np.finfo(float).eps  # Avoid log(0) issues

plt.plot(f, X_mag)
plt.axvline(x=f0, color='r', linestyle='--', label=f'Frequency {f0} Hz')
plt.legend()
#plt.xlim(0, 200)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.title('Magnitude Spectrum of the Complex Exponential Signal')
plt.grid(True)
plt.show()

