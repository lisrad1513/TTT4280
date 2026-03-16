import numpy as np 
import matplotlib.pyplot as plt
import csv

from complexFourierTransform import complex_fourier_transform

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import


channels = 3
#freqIn = 50    #50 Hz
freqIn = 1000   #1 kHz

#sample_period, data = raspi_import("ELSYSS6/Sensor/Labber/Labb4/speed_test/minimum/bilLow2", channels)
sample_period, data = raspi_import("ELSYSS6/Sensor/Labber/Labb4/speed_test/high/bilHigh3", channels)
#sample_period, data = raspi_import("ELSYSS6/Sensor/Labber/Labb4/speed_test/reverse_max/bilReverse3", channels)

# header = []
# data1 = []
# filename1 = 'ELSYSS6/Sensor/Labber/Labb4/pre-work/raw-radar-feed/digilent92c_radar.csv'
# #Henter data fra csvfil
# with open(filename1, mode='r') as csvfile:
#     csvreader = csv.reader(csvfile)
#     #Leser første linje i csv-fila (den med navn til kanalene)
#     header = next(csvreader)
#     for datapoint in csvreader:
#         values = [float(value) for value in datapoint]
#         data1.append(values)  

# #Legger inn data fra hver kanal i hver sin liste
# time = [(p[0]) for p in data1]
# ch1 = [(p[1]) for p in data1]
# ch2 = [(p[2]) for p in data1]


ch1 = data[:, 2]  # I-kanal
ch2 = data[:, 1]  # Q-kanal

plt.xlabel("Tid [s]")
plt.ylabel("Spenning [V]")
plt.title("Rå radar-feed")
plt.plot(ch1, label='I-kanal')
plt.plot(ch2, label='Q-kanal')
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.legend()
plt.show()

frequencies_shifted, spectrum, doppler_shift = complex_fourier_transform(ch1, ch2, sample_period)

plt.xlabel("Frekvens [Hz]")
plt.ylabel("Magnitude")
plt.title("Doppler-spektrum")
plt.plot(frequencies_shifted, spectrum)
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xlim(-200, 200)  # Juster x-aksen for å fokusere på relevante frekvensområder
plt.ylim(0, np.max(spectrum) * 1.1)  # Juster y-aksen for å vise hele spekteret
plt.show()
