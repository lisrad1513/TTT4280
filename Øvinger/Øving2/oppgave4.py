import numpy as np
import matplotlib.pyplot as plt

#Given
A = 1.0             #Amplitude [V]
f0 = 100.0          #Frequency [Hz]
deltaT = 0.2e-3     #Sampling time [s]
N = 900             #Number of samples

fs = 1 / deltaT     #Sampling frequency
fN = fs / 2         #Nyquist frequency

#Time vector (900 samples)
t = np.arange(N) * deltaT

#Sine signal
x = A * np.sin(2 * np.pi * f0 * t)

NFFT = 4096  #Number of points in FFT (next power of 2 above N)

x_padding = np.zeros(NFFT)      #Zero padded signal
x_padding[:N] = x               #Copy original signal into padded array

X = np.fft.fft(x_padding, n=NFFT)  #FFT computation

df = fs / NFFT              #Frequency resolution
f = np.arange(NFFT) * df    #Frequency vector

print(rf"Sampling frequency $f_s$ = {fs} Hz")
print(rf"Nyquist frequency $f_N$ = {fN} Hz")

S_xx = np.abs(X)**2 / NFFT  #Power spectral density

x_mag = np.abs(X)
x_mag[x_mag == 0] = np.finfo(float).eps  #Avoid log(0) issues
Sxx_bb = 20 * np.log10(x_mag) #Magnitude in dB
Sxx_bb = Sxx_bb - np.max(Sxx_bb)  #Normalize to 0 dB max

w = np.hanning(len(x))  #Hanning window
w_win = x * w  #Windowed signal

X_rect = np.fft.fft(w_win, n=NFFT)  #FFT computation of windowed signal
S_rect = 20 * np.log10(np.abs(X_rect))
S_rect = S_rect - np.max(S_rect)  #Normalize to 0 dB max

X_hanning = np.fft.fft(w_win, n=NFFT)  #FFT computation of windowed signal
S_hanning = 20 * np.log10(np.abs(X_hanning))
S_hanning = S_hanning - np.max(S_hanning)  #Normalize to 0 dB max

plt.plot(f, Sxx_bb, label='Rectangular Window (No Window)')
plt.plot(f, S_hanning, label='Hanning Window')
plt.axvline(x=f0, color='r', linestyle='--', label=f'Frequency {f0} Hz')
plt.legend()
plt.xlim(0, 200)
plt.ylim(-80, 25)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Relative Power [dB]')
plt.title('Power Spectral Density of the Sine Signal')
plt.grid(True)
plt.show()

