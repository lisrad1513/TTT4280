import numpy as np 
#Plotting
import matplotlib.pyplot as plt
#Lese CSV
import csv

header = []
data1 = []
data2 = []
filename1 = 'ELSYSS6/Sensor/Labber/Labb4/pre-work/filter-test/filterIFItoADC1.csv'
filename2 = 'ELSYSS6/Sensor/Labber/Labb4/pre-work/filter-test/filterIFQtoADC2.csv'
#Henter data fra csvfil
with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    #Leser første linje i csv-fila (den med navn til kanalene)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

with open(filename2, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    #Leser første linje i csv-fila (den med navn til kanalene)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data2.append(values)
        

#Legger inn data fra hver kanal i hver sin liste
freq1 = [(p[0]) for p in data1]
filt1 = [(p[1]) for p in data1]

freq2 = [(p[0]) for p in data2]
filt2 = [(p[1]) for p in data2]

#Kryssningspunkt for -3dB er der hvor filteret har en dB-verdi som er 3 mindre enn den maksimale dB-verdien.
threshold1 = max(filt1) - 3
threshold2 = max(filt2) - 3

freq1_low = None
freq1_high = None

for i in range(1, len(filt1)):
    if freq1_low is None and filt1[i-1] < threshold1 and filt1[i] >= threshold1:
        freq1_low = freq1[i]
    if filt1[i-1] >= threshold1 and filt1[i] < threshold1:
        freq1_high = freq1[i]

freq2_low = None
freq2_high = None

for i in range(1, len(filt2)):
    if freq2_low is None and filt2[i-1] < threshold2 and filt2[i] >= threshold2:
        freq2_low = freq2[i]
    if filt2[i-1] >= threshold2 and filt2[i] < threshold2:
        freq2_high = freq2[i]

print(f"Knekkfrekvens for I-kanalen: {round(freq1_low, 2)} Hz (nedre), {round(freq1_high, 2)} kHz (øvre)")
print(f"Knekkfrekvens for Q-kanalen: {round(freq2_low, 2)} Hz (nedre), {round(freq2_high, 2)} kHz (øvre)")

plt.xlabel("Frekvens [Hz]")
plt.ylabel("dB")
plt.title("Frekevensrespons til Forsterkeren")
plt.xlim(1, 10000)
plt.xscale('log')
plt.ylim(15,28)
#plt.axhline(y=0, label='Input spenning')
plt.plot(freq1, filt1, label='Filteret på I-kanalen')
plt.plot(freq2, filt2, label='Filteret på Q-kanalen')

plt.axhline(y=threshold1, color='r', linestyle='--', label='Knekkfrekvens-terskel')
plt.axvline(x=freq1_low, color='r', linestyle='--', label=f'Frekvensen: {round(freq1_low, 2)} Hz') #Nedre
plt.axvline(x=freq1_high, color='r', linestyle='--', label=f'Frekvensen: {round(freq1_high, 2)} kHz') #Øvre

plt.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

plt.legend()
plt.show()