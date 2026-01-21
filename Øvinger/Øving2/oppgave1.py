import numpy as np
import matplotlib.pyplot as plt

#Given
A = 1.0          #Amplitude [V]
f = 100.0        #Frequency [Hz]
deltaT = 0.2e-3  #Sampling time [s]
N = 900          #Number of samples

#Time vector with N points, spaced by deltaT
t = np.arange(N) * deltaT

#Sine signal
x = A * np.sin(2 * np.pi * f * t)

#Plotting the first 200 points 
plt.plot(t[:200] * 1e3, x[:200])
plt.title("Sine signal: A = 1 V, f = 100 Hz")
plt.xlabel("Time [ms]")
plt.ylabel("Voltage [V]")
plt.grid(True)
plt.show()

#Finding sampling frequency and Nyquist
fs = 1 / deltaT
fN = fs / 2
print(rf"Sampling frequency $f_s$ = {fs} Hz")
print(rf"Nyquist frequency $f_N$ = {fN} Hz")
