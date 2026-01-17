import numpy as np
import matplotlib.pyplot as plt

from raspi_import import raspi_import

channels = 3
#sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/31250Samples1VOffset0V', 3)
#sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/31250Samples2VOffset1V', 3)
#sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/31250Samples2_15VOffset1V', 3)
#sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/31250Samples1_5VOffset1_5V', 3)
sample_period, data = raspi_import('ELSYSS6/Sensor/Labber/Labb1/31250Samples1_65VOffset1_65V', channels)

print(data.shape)

time_axis = np.arange(data.shape[0]) * sample_period

print(data)

C = 3.3  # volts per count for MCP3201 with Vref = 3.3V
periodTime = 20e-3  # seconds

def converter(data): #Convert from counts to volts
    resulution = 2**12
    Vconv = (C/resulution * data)
    return Vconv

for i in range(channels):
    plt.plot(time_axis, converter(data[:, i]) + i*C, label=f'Channel {i+1}')

# plt.axhline(y=C, linestyle='--', label="Max voltage, 3.3V")
# plt.axhline(y=C/2, linestyle='--', label="Mid voltage, 1.65V", color='red')
# plt.axhline(y=0, linestyle='--', label="Min voltage, 0V")
#plt.plot(time_axis, data[:, 0], label='Channel 1')
plt.xlim(0, 10 * periodTime)
#plt.plot(time_axis, data[:, 1], label='Channel 2')
#plt.plot(time_axis, data[:, 2], label='Channel 3')
plt.legend()
plt.show()