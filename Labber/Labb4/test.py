import numpy as np 
import matplotlib.pyplot as plt
import csv

from complexFourierTransform import complex_fourier_transform

header = []
data1 = []
filename1 = 'ELSYSS6/Sensor/Labber/Labb4/pre-work/raw-radar-feed/digilent92c_radar.csv'
#Henter data fra csvfil
with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    #Leser første linje i csv-fila (den med navn til kanalene)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)  

#Legger inn data fra hver kanal i hver sin liste
time = [(p[0]) for p in data1]
ch1 = [(p[1]) for p in data1]
ch2 = [(p[2]) for p in data1]

frequencies, spectrum, doppler_shift = complex_fourier_transform(ch1, ch2)

plt.xlabel("Frekvens [Hz]")
plt.ylabel("Magnitude")
plt.title("Doppler-spektrum")
plt.plot(frequencies, spectrum)
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xlim(-0.2, 0.2)  # Juster x-aksen for å fokusere på relevante frekvensområder
plt.ylim(0, np.max(spectrum) * 1.1)  # Juster y-aksen for å vise hele spekteret
plt.show()
