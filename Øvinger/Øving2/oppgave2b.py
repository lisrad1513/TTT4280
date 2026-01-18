import numpy as np
import matplotlib.pyplot as plt

#Given
A = 1.0             #Amplitude [V]
f0 = 100.0          #Frequency [Hz]
deltaT = 0.2e-3     #Sampling time [s]
fs = 1 / deltaT
N = 900             #Number of samples

#Time signal
t = np.arange(N) * deltaT
x = A * np.sin(2 * np.pi * f0 * t)

def periodogram_full(x, sample_period):
    x = x.astype(np.float64)

    #Remove DC
    x = x - np.mean(x)

    fs = 1.0 / sample_period
    NFFT = len(x)

    #Full FFT length NFFT
    X = np.fft.fft(x)

    #Frequency axis 0 to fs (NFFT points)
    freq = np.arange(NFFT) * fs / NFFT

    #Periodogram Sxx = |X|^2 (simple normalized version)
    Sxx = (np.abs(X) ** 2) / (NFFT ** 2)

    #Power in dB
    Sxx_db = 10 * np.log10(Sxx + 1e-20)

    return freq, Sxx_db, NFFT

freq, Sxx_db, NFFT = periodogram_full(x, deltaT)

delta_f = fs / NFFT
print(f"NFFT = {NFFT}")
print(f"fs = {fs} Hz")
print(f"Δf = {delta_f} Hz")
print(f"Mirror frequency = {fs - f0} Hz")

plt.plot(freq, Sxx_db, label='Periodogram')
plt.title("Periodogram $S_{XX}(f) = |X(f)|^2$")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Power [dB]")
plt.xlim(0, fs)
plt.legend()
plt.grid(True)
plt.show()