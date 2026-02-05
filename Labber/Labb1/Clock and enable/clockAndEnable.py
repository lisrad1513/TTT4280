import numpy as np
import matplotlib.pyplot as plt
import csv

header = []
data1 = []
filename1 = 'ELSYSS6/Sensor/Labber/Labb1/Clock and enable/ClockAndEnableSignal.csv'

with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

time = [p[0] for p in data1]
v1 = [p[1] for p in data1]
v2 = [p[2] for p in data1]

#Format tiime to microseconds
time = [t * 1e6 for t in time]

plt.xlabel("Time [µs]")
plt.ylabel("Voltage [V]")
plt.title(r"Clock and Enable Signal")

plt.plot(time, v1, label=r'Clock', alpha=1)
plt.plot(time, v2, label=r'Enable', alpha=1)

padding = 0.4  #Microseconds

startCycle = (1.963044748695652) * 1e6 #Microseconds
endCycle = (1.963046708695652) * 1e6 #Microseconds

oneCycle = endCycle - startCycle  #Microseconds
oneFullCycle = 16 #One full cycle of clock and enable (according to datasheet)
amountOfCycles = 16 #Number of clock cycles to show

start = startCycle - padding
#end = (startCycle + amountOfCycles * oneCycle) + padding
end = (startCycle + oneFullCycle * oneCycle) + padding

plt.xlim(start, end)
plt.legend()
plt.grid(True, which="both")
plt.show()