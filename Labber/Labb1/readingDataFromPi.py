import numpy as np
import matplotlib.pyplot as plt

from raspi_import import raspi_import

#sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/ACD31250SamplesTest')
sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/ADCPiOutputReal1', 3)
#sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/ADCPiOutputReal1SquareTest', 3)

print(data.shape)

time_axis = np.arange(data.shape[0]) * sample_period

print(data)

#C = 0.805664062e-3  # volts per count for MCP3201 with Vref = 3.3V
C = 3.3  # volts per count for MCP3201 with Vref = 3.3V

def converter(data):
    resulution = 2**12
    Vconv = (C/resulution * data)
    return Vconv


plt.plot(time_axis, converter(data[:, 0]), label='Channel 1 Converted')
plt.plot(time_axis, converter(data[:, 1]), label='Channel 2 Converted')
plt.plot(time_axis, converter(data[:, 2]), label='Channel 3 Converted')
plt.axhline(y=3.3, linestyle='--')
#plt.plot(time_axis, data[:, 0], label='Channel 1')
plt.xlim(0, 1)
#plt.plot(time_axis, data[:, 1], label='Channel 2')
#plt.plot(time_axis, data[:, 2], label='Channel 3')
plt.legend()
plt.show()