import numpy as np                      
import matplotlib.pyplot as plt         
from raspi_import import raspi_import   

channels = 3

sample_period1, data1 = raspi_import(f'ELSYSS6/Sensor/Labber/Labb1/1000Hz/31250Samples1_65VOffset1_65V1000Hz', channels)
sample_period2, data2 = raspi_import("ELSYSS6/Sensor/Labber/Labb1/ADCMedUtenFilter/31250Samples1_65VOffset1_65V1000HzUtenFilter", channels)

targetFreq = 1000  #Hz

#Convert ADC data to float so FFT and mean subtraction behave as expected.
x1 = data1.astype(np.float64)
x2 = data2.astype(np.float64)

#Remove DC offset (mean value) from each channel separately.
x1 = x1 - np.mean(x1, axis=0, keepdims=True)
x2 = x2 - np.mean(x2, axis=0, keepdims=True)

#Number of time samples
N1 = x1.shape[0]
N2 = x2.shape[0]
N = min(N1, N2)

#Sampling frequency fs in Hz (samples per second)
fs1 = 1.0 / sample_period1
fs2 = 1.0 / sample_period2

#Window functions
windowFunction = 'hann' # Options: 'none', 'hann', 'hamming', 'blackman', 'bartlett'
if windowFunction == 'none':
    w = np.ones((N, 1))

elif windowFunction == 'hann':
    w = np.hanning(N)[:, None]

elif windowFunction == 'hamming':
    w = np.hamming(N)[:, None]

elif windowFunction == 'blackman':
    w = np.blackman(N)[:, None]

elif windowFunction == 'bartlett':
    w = np.bartlett(N)[:, None]

else:
    print("Unknown window function, defaulting to none.")
    w = np.ones((N, 1))

#Apply the window to each channel
xw1 = x1 * w
xw2 = x2 * w

#Zero padding / nfft choice (nfft > N adds zero padding)
nfftChooser = True  # True: nfft = next power of 2 above N, False: nfft = N
if nfftChooser:
    nfft = 2**int(np.ceil(np.log2(N)))  
else:
    nfft = N

#Compute one sided FFT for real signals along the time axis (axis=0).
X1 = np.fft.rfft(xw1, n=nfft, axis=0)
X2 = np.fft.rfft(xw2, n=nfft, axis=0)

#Frequency axis for rfft, in Hz, using the real sample period Ts
freq1 = np.fft.rfftfreq(nfft, d=sample_period1)
freq2 = np.fft.rfftfreq(nfft, d=sample_period2)

#Magnitude spectrum (absolute value of complex FFT).
mag1 = np.abs(X1) / N
mag2 = np.abs(X2) / N

#For a one sided spectrum, energy that was split between positive and negative frequencies is folded into the positive side, so we multiply interior bins by 2.
if nfft > 1:
    mag1[1:-1, :] *= 2.0
    mag2[1:-1, :] *= 2.0
#Convert magnitude to decibels.
eps = 1e-12
mag_db1 = 20.0 * np.log10(mag1 + eps) #eps prevents log10(0)
mag_db2 = 20.0 * np.log10(mag2 + eps) #eps prevents log10(0)

plt.figure()
channel = 0
plt.plot(freq1, mag_db1[:, channel], label=f"ADC {channel + 1} med filter")
plt.plot(freq2, mag_db2[:, channel], label=f"ADC {channel + 1} uten filter", alpha=0.5)

#Control what frequency range is shown
#0: show 0 to 2000 Hz
#1: show full available one sided range 0 to fs/2
#2: zoom near targetFreq
plotWholeSpectrum = 0 #Change this value to 0, 1, or 2
if plotWholeSpectrum == 0:
    plt.xlim(0, 3000)
elif plotWholeSpectrum == 1:
    plt.xlim(0, fs1 / 2)
else:
    plt.xlim(targetFreq - 50, targetFreq + 50)


plt.xlabel("Frekvens [Hz]")
plt.ylabel("Magnitude [dB]")
plt.title("FFT Analyse av ADC Data")
plt.axvline(x=targetFreq, linestyle='--', label=f"Målfrekvens, {targetFreq}Hz", color='red')
plt.axvline(x=50, linestyle='--', label=f"50Hz mains", color='red', alpha=0.25)
plt.grid(True)
plt.legend()
plt.show()