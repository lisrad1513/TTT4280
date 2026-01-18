import numpy as np
import matplotlib.pyplot as plt

#Given
A = 1.0          #Amplitude [V]
f0 = 100.0        #Frequency [Hz]
deltaT = 0.2e-3  #Sampling time [s]
N = 900          #Number of samples

#Time vector (900 samples)
t = np.arange(N) * deltaT

#Sine signal
x = A * np.sin(2 * np.pi * f0 * t)

#Sampling frequency and Nyquist
fs = 1 / deltaT
fN = fs / 2

def FFT_analysis(x, sample_period):
    x = x.astype(np.float64)

    #Remove DC offset
    x = x - np.mean(x)

    NFFT = len(x)
    fs = 1.0 / sample_period #Sampling frequency

    #Full FFT length NFFT
    X = np.fft.fft(x)

    #Frequency axis 0 to fs (NFFT points)
    freq = np.arange(NFFT) * fs / NFFT

    #Magnitude in dB (amplitude spectrum style)
    magnitude = 20 * np.log10(np.abs(X) / NFFT + 1e-12)

    return freq, magnitude, NFFT

#FFT analysis without zero padding
freq, magnitude, NFFT = FFT_analysis(x, deltaT)

#Frequency step
delta_f = fs / NFFT
print(f"NFFT = {NFFT}")
print(f"fs = {fs} Hz")
print(f"Nyquist = {fN} Hz")
print(f"Δf = {delta_f} Hz")

#Plot 0 to 5 kHz (fs)
plt.plot(freq, magnitude, label='FFT Magnitude')
plt.title("FFT of sine signal")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")
plt.xlim(0, fs)
plt.legend()
plt.grid(True)
plt.show()