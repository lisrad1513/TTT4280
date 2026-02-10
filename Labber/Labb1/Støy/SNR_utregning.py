import csv
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

header = []
data1 = []
data2 = []
filename1 = 'ELSYSS6/Sensor/Labber/Labb1/Støy/ADC-1-2.csv'
filename2 = 'ELSYSS6/Sensor/Labber/Labb1/Støy/ADC-3.csv'

with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

with open(filename2, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data2.append(values)

time1 = [p[0] for p in data1]
channel1 = [p[1] for p in data1]
channel2 = [p[2] for p in data1]
time2 = [p[0] for p in data2]
channel3 = [p[1] for p in data2]


channels = [np.array(channel1), np.array(channel2), np.array(channel3)]


sample_period, data = raspi_import(f'ELSYSS6/Sensor/Labber/Labb1/1000Hz/31250Samples1_65VOffset1_65V1000Hz', 3)

#Function that calculates SNR
def SNR(signal, noise):
    """
    Beregn Signal-to-Noise Ratio (SNR) i desibel (dB).
    
    Parametre:
        signal: numpy array med signalverdier (volts)
        noise: numpy array med støyverdier (volts)
    
    Returnerer:
        SNR i dB
    
    Merk: Effekt er proporsjonal med V², og siden vi tar forholdet mellom
    signaleffekt og støyeffekt, kansellerer resistansen (R) ut.
    """
    # Beregn gjennomsnittlig effekt (normalisert til R=1Ω)
    power_signal = np.mean(signal)  # Fjern DC-offset
    power_noise = np.mean(noise)  # Fjern DC-offset
    
    if power_noise == 0:
        raise ValueError("Støyens effekt er null, kan ikke beregne SNR")
    
    snr = 10 * np.log10(power_signal / power_noise)
    return snr

signal1 = data[:, 0]  # Anta at signalet er i kanal 0
noise1 = channels[0]
signal2 = data[:, 1]  # Anta at signalet er i kanal 1
noise2 = channels[1]
signal3 = data[:, 2]  # Anta at signalet er i kanal 2
noise3 = channels[2]
    
snr_value1 = SNR(signal1, noise1)
snr_value2 = SNR(signal2, noise2)
snr_value3 = SNR(signal3, noise3)
print(f"SNR channel 1: {snr_value1:.2f} dB")
print(f"SNR channel 2: {snr_value2:.2f} dB")
print(f"SNR channel 3: {snr_value3:.2f} dB")