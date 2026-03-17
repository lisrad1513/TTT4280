import numpy as np 
import matplotlib.pyplot as plt
import csv

from complexFourierTransform import complex_fourier_transform
from speedConversion import convert_doppler_shift_to_speed

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

channels = 3

#sample_period, data = raspi_import("ELSYSS6/Sensor/Labber/Labb4/speed_test/minimum/bilLow4", channels)
#sample_period, data = raspi_import("ELSYSS6/Sensor/Labber/Labb4/speed_test/high/bilHigh4", channels)
sample_period, data = raspi_import("ELSYSS6/Sensor/Labber/Labb4/speed_test/reverse_max/bilReverse4", channels)


sr = 31250  # Samplingsfrekvens i Hz
f_0 = 24.13e9  # Radarens frekvens i Hz
c = 299792458  # Lysets hastighet i m/s
waveLength = c / f_0  # Radarens bølgelengde i meter

cut_upper = 0.5
cut_lower = 1
cut_samples_upper = int(cut_upper * sr)  # Antall samples som tilsvarer cut-tiden
cut_samples_lower = len(data) - int(cut_lower * sr)  # Antall samples som tilsvarer cut-tiden
print(f"Total samples: {len(data)}")
print(f"Cut samples upper: {cut_samples_upper}")
print(f"Cut samples lower: {cut_samples_lower}")


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


ch1 = data[cut_samples_upper:cut_samples_lower, 2]  # I-kanal
ch2 = data[cut_samples_upper:cut_samples_lower, 1]  # Q-kanal

plt.xlabel("Tid [s]")
plt.ylabel("Spenning [V]")
plt.title("Rå radar-feed")
plt.plot(ch1, label='I-kanal')
plt.plot(ch2, label='Q-kanal')
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.legend()
plt.show()

frequencies_shifted, spectrum, db_spectrum, doppler = complex_fourier_transform(ch1, ch2, sample_period, True, True, True, "highpass",30, 0, 4)

f_D = np.max(frequencies_shifted[np.where(spectrum == np.max(spectrum))])  # Doppler-frekvens i Hz

print(f"Doppler-frekvens: {f_D:.2f} Hz")
speed = convert_doppler_shift_to_speed(f_D, f_0)
print(f"Estimert hastighet: {speed:.2f} m/s")

plt.xlabel("Frekvens [Hz]")
plt.ylabel("Magnitude [dB]")
plt.title("Doppler-spektrum")
plt.plot(frequencies_shifted, spectrum, label='Doppler-spektrum')
#plt.plot(frequencies_shifted, db_spectrum, label='Doppler-spektrum')
#plt.plot(frequencies_shifted, 10 * np.log10(spectrum), label='Doppler-spektrum')
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xlim(-np.abs(f_D*1.5), np.abs(f_D*1.5))  # Juster x-aksen for å fokusere på relevante frekvensområder
#plt.ylim(0, np.max(spectrum) * 1.1)  # Juster y-aksen for å vise hele spekteret
plt.show()
