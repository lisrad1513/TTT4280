import numpy as np 
import matplotlib.pyplot as plt
import csv

from complexFourierTransform import complex_fourier_transform
from speedConversion import convert_doppler_shift_to_speed, convert_distance_and_time_to_speed
from snr_comp import estimate_snr_from_spectrum
from resolution import estimate_doppler_resolution

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
db_spectrum = []
frequencies_shifted = []
for i in range(speeds_tested):
    measure_speed_doppler = []
    measure_speed_timer = []
    measure_snr = []
    measure_resolution = []
    for j in range(readings):
        current_measurement = (i * readings) + j

        sample_period, data = raspi_import(f"{filePath[current_measurement]}", channels)
        cutSamples_start = int(timeCutFirst[current_measurement] * sr)
        cutSamples_end = int(len(data) - (timeCutLast[current_measurement] * sr))

        ch1 = data[cutSamples_start:cutSamples_end, 2]  # I-kanal
        ch2 = data[cutSamples_start:cutSamples_end, 1]  # Q-kanal

        frequencies_shifted, spectrum, db_spectrum, doppler = complex_fourier_transform(ch1, 
                                                                                        ch2, 
                                                                                        sample_period,
                                                                                        True, # apply_window
                                                                                        True, # remove dc
                                                                                        True, # shift_frequencies
                                                                                        "highpass", # filter_type
                                                                                        filterLower[current_measurement], # filter_lower
                                                                                        None, # filter_upper
                                                                                        4) # filter_order
        f_D = np.max(frequencies_shifted[np.where(spectrum == np.max(spectrum))])  # Doppler-frekvens i Hz
        speed_doppler = convert_doppler_shift_to_speed(f_D, f_0)  # Radarens frekvens i Hz
        speed_timer = convert_distance_and_time_to_speed(length[current_measurement], time[current_measurement])  # Radarens frekvens i Hz

        measure_speed_doppler.append(speed_doppler)
        measure_speed_timer.append(speed_timer)

        result_snr = estimate_snr_from_spectrum(
            frequencies = frequencies_shifted,
            spectrum = spectrum,
            spectrum_unit = "linear",   # use this if your plotted y-axis is truly power in dB
            dc_exclusion_hz = 20,
            guard_hz = 15,
            search_band = (-600, 600),
            use_peak_power = True,
        )
        measure_snr.append(result_snr['snr_db'])

        result_resolution = estimate_doppler_resolution(
            frequencies = frequencies_shifted,
            spectrum = db_spectrum,
            sample_period = sample_period,
            spectrum_unit = "db_magnitude",
            dc_exclusion_hz = 20,
            search_band = (-600, 600),
        )
        measure_resolution.append(result_resolution['bandwidth_3db_hz'])


    doppler_avg = np.mean(measure_speed_doppler) # Gjennomsnittlig Doppler-hastighet
    doppler_std = np.std(measure_speed_doppler)  # Standardavvik for Doppler-målingene
    timer_avg = np.mean(measure_speed_timer) # Gjennomsnittlig Timer-hastighet
    timer_std = np.std(measure_speed_timer)  # Standardavvik for Timer-målingene
    snr_avg = np.mean(measure_snr)  # Gjennomsnittlig SNR
    snr_std = np.std(measure_snr)  # Standardavvik for SNR-målingene
    resolution_avg = np.mean(measure_resolution)  # Gjennomsnittlig Doppler-oppløsning
    resolution_std = np.std(measure_resolution)  # Standardavvik for Doppler-oppløsning

    measurements.append((doppler_avg, timer_avg, doppler_std, timer_std, snr_avg, snr_std, resolution_avg, resolution_std))

plt.xlabel("Frekvens [Hz]")
plt.ylabel("Magnitude [dB]")
plt.title("Doppler-spektrum")
plt.plot(frequencies_shifted, db_spectrum, label='Doppler-spektrum')
#plt.plot(frequencies_shifted, db_spectrum, label='Doppler-spektrum')
#plt.plot(frequencies_shifted, 10 * np.log10(spectrum), label='Doppler-spektrum')
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xlim(-np.abs(f_D*1.5), np.abs(f_D*1.5))  # Juster x-aksen for å fokusere på relevante frekvensområder
#plt.ylim(0, np.max(spectrum) * 1.1)  # Juster y-aksen for å vise hele spekteret
plt.show()

print("Målte hastigheter:")
for i in range(speeds_tested):
    print(f"{name[i * readings]}:")
    print(f"  Doppler-hastighet: {measurements[i][0]:.{decimals}f} m/s (std: {measurements[i][2]:.2f} m/s)")
    print(f"  Timer-hastighet: {measurements[i][1]:.{decimals}f} m/s (std: {measurements[i][3]:.2f} m/s)")
    print(f"  SNR: {measurements[i][4]:.{decimals}f} dB (std: {measurements[i][5]:.2f} dB)")
    print(f"  Doppler-oppløsning: {measurements[i][6]:.{decimals}f} Hz (std: {measurements[i][7]:.2f} Hz)")
    print()