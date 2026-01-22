import numpy as np
import matplotlib.pyplot as plt
import csv

header = []
data1 = []
data2 = []
filename1 = 'ELSYSS6/Sensor/Labber/Labb1/Filter/Filter0Ohm501Steps.csv'
filename2 = 'ELSYSS6/Sensor/Labber/Labb1/Filter/Filter15Ohm501Steps.csv'

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

freq1 = [p[0] for p in data1]
db1 = [p[2] for p in data1]
freq2 = [p[0] for p in data2]
db2 = [p[2] for p in data2]

plt.xlabel("Frekvens [Hz]")
plt.ylabel("Demping [dB]")

plt.title(r"Amplituderespons til filter [1Hz - 100kHz]")

plt.plot(freq1, db1, label=r'0 $\Omega$ motstand', alpha=1)
plt.plot(freq2, db2, label=r'15 $\Omega$ motstand', alpha=1)

plt.axhline(y=-3, linestyle='--', label=r'Knekkfrekvens, -3 dB', color='red', alpha=0.6)
plt.axvline(x=24.5471, linestyle='--', label=r'Knekkfrekvens, 24.55 Hz', alpha=0.6)
plt.axvline(x=31.0, linestyle='--', label=r'Knekkfrekvens, 30.90 Hz', alpha=0.6)

plt.xscale("log")  #Logarithmic x-axis

#Finding limits for x-axis
xmin = min(f for f in freq1 if f > 0)
#plt.xlim(xmin, max(freq1))
plt.xlim(1, 1000)

plt.legend()
plt.grid(True, which="both")
plt.show()