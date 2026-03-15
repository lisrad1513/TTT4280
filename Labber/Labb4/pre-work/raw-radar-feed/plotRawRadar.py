import numpy as np 
#Plotting
import matplotlib.pyplot as plt
#Lese CSV
import csv

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

plt.xlabel("Tid [s]")
plt.ylabel("Spenning [V]")
plt.title("Rå radar-feed")
plt.plot(time, ch1, label='Ch1')
plt.plot(time, ch2, label='Ch2')
plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.legend()
plt.show()