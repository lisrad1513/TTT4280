import numpy as np                      
import matplotlib.pyplot as plt         
from raspi_import import raspi_import   

channels = 3
#freqIn = 50    #50 Hz
freqIn = 1000   #1 kHz

#sample_period, data = raspi_import(f'ELSYSS6/Sensor/Labber/Labb1/{freqIn}Hz/31250Samples1_65VOffset1_65V{freqIn}Hz', channels)
sample_period, data = raspi_import("ELSYSS6/Sensor/Labber/Labb1/ADCMedUtenFilter/31250Samples1_65VOffset1_65V1000HzUtenFilter", channels)

targetFreq = freqIn  #Hz

#Convert ADC data to float so FFT and mean subtraction behave as expected.
x = data.astype(np.float64)

#Remove DC offset (mean value) from each channel separately.
x = x - np.mean(x, axis=0, keepdims=True)

#Number of time samples
N = x.shape[0]

#Sampling frequency fs in Hz (samples per second)
fs = 1.0 / sample_period

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
xw = x * w

#Zero padding / nfft choice (nfft > N adds zero padding)
nfftChooser = True  # True: nfft = next power of 2 above N, False: nfft = N
if nfftChooser:
    nfft = 2**int(np.ceil(np.log2(N)))  
else:
    nfft = N

#Compute one sided FFT for real signals along the time axis (axis=0).
X = np.fft.rfft(xw, n=nfft, axis=0)

#Frequency axis for rfft, in Hz, using the real sample period Ts
freq = np.fft.rfftfreq(nfft, d=sample_period)

#Magnitude spectrum (absolute value of complex FFT).
mag = np.abs(X) / N

#For a one sided spectrum, energy that was split between positive and negative frequencies is folded into the positive side, so we multiply interior bins by 2.
if nfft > 1:
    mag[1:-1, :] *= 2.0

#Convert magnitude to decibels.
eps = 1e-12
mag_db = 20.0 * np.log10(mag + eps) #eps prevents log10(0)

plt.figure()
for ch in range(mag_db.shape[1]):
    plt.plot(freq, mag_db[:, ch], label=f"ADC {ch}")

#Control what frequency range is shown
#0: show 0 to 2000 Hz
#1: show full available one sided range 0 to fs/2
#2: zoom near targetFreq
plotWholeSpectrum = 1 #Change this value to 0, 1, or 2
if plotWholeSpectrum == 0:
    plt.xlim(0, 3000)
elif plotWholeSpectrum == 1:
    plt.xlim(0, fs / 2)
else:
    plt.xlim(targetFreq - 20, targetFreq + 20)


plt.xlabel("Frekvens [Hz]")
plt.ylabel("Magnitude [dB]")
plt.title("FFT Analyse av ADC Data")
plt.axvline(x=targetFreq, linestyle='--', label=f"Målfrekvens, {targetFreq}Hz", color='red')
plt.axvline(x=50, linestyle='--', label=f"50Hz mains", color='red', alpha=0.25)
plt.grid(True)
plt.legend()
plt.show()