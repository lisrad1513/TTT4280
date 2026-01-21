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

NFFT = 1024  #Number of points in FFT (next power of 2 above N)

x_padding = np.zeros(NFFT)  #Zero padded signal
x_padding[:N] = x            #Copy original signal into padded array

X = np.fft.fft(x_padding, n=NFFT)  #FFT computation

df = fs / NFFT          #Frequency resolution
f = np.arange(NFFT) * df  #Frequency vector

print(rf"Interval $d_f$ = {df} Hz")