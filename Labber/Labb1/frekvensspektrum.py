import numpy as np
import matplotlib.pyplot as plt

#Generate random array
fs = 1000  # Sampling frequency
t = np.arange(0, 1.0, 1.0/fs)
f1 = 50  # Frequency of the first sine wave
f2 = 120  # Frequency of the second sine wave
signal = 0.7 * np.sin(2 * np.pi * f1 * t) + 0.3 * np.sin(2 * np.pi * f2 * t) + 0.5 * np.random.normal(size=t.shape)  # Add some noise

#Compute FFT
n = len(signal)
fft_values = np.fft.fft(signal)
fft_freq = np.fft.fftfreq(n, 1/fs) 

#Compute magnitude spectrum
magnitude = np.abs(fft_values) / n  

#Plot frequency spectrum
#plt.figure(figsize=(10, 6))
plt.plot(fft_freq[:n//2], magnitude[:n//2])  # Plot only the positive frequencies
plt.title('Frequency Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid()
plt.show()