import numpy as np 
import matplotlib.pyplot as plt
import csv

from complexFourierTransform import complex_fourier_transform
from speedConversion import convert_doppler_shift_to_speed, convert_distance_and_time_to_speed

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

header = []
data_specifications = []
filename1 = 'ELSYSS6/Sensor/Labber/Labb4/speed_test/specifications.csv'
#Henter data fra csvfil
with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    #Leser første linje i csv-fila (den med navn til kanalene)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [value for value in datapoint]
        data_specifications.append(values)  


#Legger inn data fra hver kanal i hver sin liste
name = [(p[0]) for p in data_specifications]
filePath = [(p[1]) for p in data_specifications]
timeCutFirst = [(float(p[2])) for p in data_specifications]
timeCutLast = [(float(p[3])) for p in data_specifications]
filterLower = [(float(p[4])) for p in data_specifications]
filterUpper = [(float(p[5])) for p in data_specifications]
length = [(float(p[6])) for p in data_specifications]
time = [(float(p[7])) for p in data_specifications]

sr = 31250 # Samplingsfrekvens i Hz
f_0 = 24.13e9  # Radarens frekvens i Hz
channels = 3
speeds_tested = 3
readings = 4
decimals = 2

measurements = []
for i in range(speeds_tested):
    measurements_local = []
    for j in range(readings):
        current_measurement = (i * readings) + j
        sample_period, data = raspi_import(f"{filePath[current_measurement]}", channels)
        cutSamples_start = int(timeCutFirst[current_measurement] * sr)
        cutSamples_end = int(len(data) - (timeCutLast[current_measurement] * sr))

        ch1 = data[cutSamples_start:cutSamples_end, 2]  # I-kanal
        ch2 = data[cutSamples_start:cutSamples_end, 1]  # Q-kanal

        frequencies_shifted, spectrum, db_spectrum, doppler = complex_fourier_transform(ch1, ch2, sample_period, True, True, True, "highpass", filterLower[current_measurement], None, 4) 
        f_D = np.max(frequencies_shifted[np.where(spectrum == np.max(spectrum))])  # Doppler-frekvens i Hz
        speed_doppler = convert_doppler_shift_to_speed(f_D, f_0)  # Radarens frekvens i Hz
        speed_timer = convert_distance_and_time_to_speed(length[current_measurement], time[current_measurement])  # Radarens frekvens i Hz

        measurements_local.append(speed_doppler)
        measurements_local.append(speed_timer)


    avg_doppler = np.mean(measurements_local[::2]) # Gjennomsnittlig Doppler-hastighet
    doppler_std = np.std(measurements_local[::2])  # Standardavvik for Doppler-målingene
    avg_timer = np.mean(measurements_local[1::2]) # Gjennomsnittlig Timer-hastighet
    timer_std = np.std(measurements_local[1::2])  # Standardavvik for Timer-målingene

    measurements.append((avg_doppler, avg_timer, doppler_std, timer_std))

print("Målte hastigheter:")
for i in range(speeds_tested):
    print(f"{name[i * readings]}: Dop = {measurements[i][0]:.{decimals}f} m/s, Ti = {measurements[i][1]:.{decimals}f} m/s, Dop_std = {measurements[i][2]:.{decimals}f} m/s, Ti_std = {measurements[i][3]:.{decimals}f} m/s")