import numpy as np
import matplotlib.pyplot as plt
import csv

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

header = []
data1 = []
csvFile = 'ELSYSS6/Sensor/Labber/Labb1/FoerOgEtterADC/Analog-signalAD3.csv' #Noke e rart med dinne fila :/

binaryFile = 'ELSYSS6/Sensor/Labber/Labb1/FoerOgEtterADC/ADCsignal'
channels = 3

sample_period, data = raspi_import(binaryFile, channels)

def converter(data): #Convert from counts to volts
    C = 3.3  # volts per count for MCP3201 with Vref = 3.3V
    resulution = (2**12) - 1  #12 bit ADC
    Vconv = (data / resulution) * C
    return Vconv


with open(csvFile, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

timeCSV = [p[0] for p in data1]
readingADC = [p[1] for p in data1]

plt.xlabel("Tid [s]")
plt.ylabel("ADC-verdi")

time_axis = np.arange(data.shape[0]) * sample_period

#Function that moves the sine from the ADC reading forwards in time to align with the CSV data
# It takes in the fuction data, sample period and time shift in seconds
def timeShift(data, sample_period, time_shift):
    samples_shift = int(time_shift / sample_period)
    shifted_data = np.roll(data, -samples_shift)
    return shifted_data


data[:, 1] = timeShift(data[:, 1], sample_period, 736.0E-6)  #Shift by 


plt.plot(timeCSV, readingADC, label=r'ADC Reading', alpha=1)
plt.plot(time_axis, converter(data[:, 1]), label=r'ADC Input', alpha=1)
plt.xlim(0, 0.003)



plt.legend()
plt.grid(True, which="both")
plt.show()