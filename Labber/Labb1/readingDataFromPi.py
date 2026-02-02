import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


from raspi_import import raspi_import

channels = 3
#freqIn = 50    #50 Hz
freqIn = 1000   #1 kHz

periodsCount = 10 #How many periods you want to display
periodTime = 1/freqIn  #seconds
rangePeriod = periodsCount * periodTime 

#sample_period, data = raspi_import(f'ELSYSS6/Sensor/Labber/Labb1/{freqIn}Hz/31250Samples1_65VOffset1_65V{freqIn}Hz', channels)
sample_period, data = raspi_import(f'ELSYSS6/Sensor/Labber/Labb1/demoForStudass', channels)

print(data.shape)

time_axis = np.arange(data.shape[0]) * sample_period

print(data)

C = 3.3  # volts per count for MCP3201 with Vref = 3.3V

def converter(data): #Convert from counts to volts
    resulution = (2**12) - 1  #12 bit ADC
    Vconv = (data / resulution) * C
    return Vconv

#colorArray
colorArray = ['royalblue', 'orange', 'green']

#Plot each channel in its own subplot
fig, axs = plt.subplots(channels, 1, sharex=True, figsize=(6, 6))
if channels == 1:
    axs = [axs]
for i in range(channels):
    axs[i].plot(time_axis, converter(data[:, i]), color=colorArray[i], label=f'Digital data fra ADC {i+1}')
    axs[i].axhline(y=C, linestyle='--', label="Maks spenning, 3.3V", color='gray', alpha=0.6)
    axs[i].axhline(y=C/2, linestyle='--', label="DC offset, 1.65V", color='red', alpha=0.6)
    axs[i].axhline(y=0, linestyle='--', label="Min spenning, 0V", color='gray', alpha=0.6)
    axs[i].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x*1e3:g}"))
    axs[i].set_xlim(0, 0.005)
    axs[i].set_ylim(-0.5, 3.7)
    axs[i].set_ylabel("Voltage [V]")
    axs[i].set_title(f"Data fra ADC {i+1}")
    axs[i].legend()
    axs[i].grid(True)
    if i == channels - 1:
        axs[i].set_xlabel("Time [ms]")
plt.tight_layout()
plt.show() 