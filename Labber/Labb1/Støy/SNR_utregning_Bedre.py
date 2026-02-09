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

# Function that calculates SNR
def SNR_from_signal_with_noise(signal_with_noise, noise_only):
    """
    Beregn Signal-to-Noise Ratio (SNR) fra en måling med signal+støy og en måling med bare støy.
    
    Parametre:
        signal_with_noise: numpy array med signal + støy (volts)
        noise_only: numpy array med bare støy (volts)
    
    Returnerer:
        SNR i dB
    """
    # Fjern DC-offset
    signal_ac = signal_with_noise - np.mean(signal_with_noise)
    noise_ac = noise_only - np.mean(noise_only)
    
    # Total effekt i signalet (signal + støy)
    power_total = np.mean(signal_ac ** 2)
    
    # Støyeffekt
    power_noise = np.mean(noise_ac ** 2)
    
    # Signaleffekt = total effekt - støyeffekt
    power_signal = power_total - power_noise
    
    if power_signal <= 0:
        raise ValueError("Signaleffekt er negativ eller null - sjekk målingene")
    if power_noise == 0:
        raise ValueError("Støyeffekt er null")
    
    snr = 10 * np.log10(power_signal / power_noise)
    return snr

def SNR_from_single_measurement(signal_with_noise):
    """
    Beregn SNR fra én måling ved å estimere signal fra RMS og støy fra residual.
    Antar sinusformet signal.
    
    Parametre:
        signal_with_noise: numpy array med signal + støy (volts)
    
    Returnerer:
        SNR i dB
    """
    # Fjern DC-offset
    signal_ac = signal_with_noise - np.mean(signal_with_noise)
    
    # Peak-to-peak amplitude (estimat av sinus amplitude)
    amplitude = (np.max(signal_ac) - np.min(signal_ac)) / 2
    
    # Signaleffekt for sinus: A²/2
    power_signal = (amplitude ** 2) / 2
    
    # Total effekt
    power_total = np.mean(signal_ac ** 2)
    
    # Støyeffekt = total - signal
    power_noise = power_total - power_signal
    
    if power_noise <= 0:
        raise ValueError("Estimert støyeffekt er negativ - prøv en annen metode")
    
    snr = 10 * np.log10(power_signal / power_noise)
    return snr

# Beregn SNR med begge metoder
print("=== Metode 1: Sammenligning med støymåling ===")
signal1 = data[:, 0]
noise1 = channels[0]
signal2 = data[:, 1]
noise2 = channels[1]
signal3 = data[:, 2]
noise3 = channels[2]
    
snr_value1 = SNR_from_signal_with_noise(signal1, noise1)
snr_value2 = SNR_from_signal_with_noise(signal2, noise2)
snr_value3 = SNR_from_signal_with_noise(signal3, noise3)
print(f"SNR channel 1: {snr_value1:.2f} dB")
print(f"SNR channel 2: {snr_value2:.2f} dB")
print(f"SNR channel 3: {snr_value3:.2f} dB")

print("\n=== Metode 2: Fra enkeltmåling ===")
snr_single1 = SNR_from_single_measurement(signal1)
snr_single2 = SNR_from_single_measurement(signal2)
snr_single3 = SNR_from_single_measurement(signal3)
print(f"SNR channel 1: {snr_single1:.2f} dB")
print(f"SNR channel 2: {snr_single2:.2f} dB")
print(f"SNR channel 3: {snr_single3:.2f} dB")