import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os

#FFT analysis of each color channel, to find the dominant frequencies in the signal
def plot_fft(data_path, fps = 40, lowerbound = 0, upperbound = 6, normalizeChannelsSeparately=True):
    data = np.genfromtxt(data_path, delimiter=" ", skip_header=1)
    print(data)  # Print the loaded data to verify its structure
    if data.ndim != 2 or data.shape[1] < 3:
        print(f"Error: Data shape is incorrect. Expected (n, 3), got {data.shape}")
        exit()

    time = np.arange(len(data)) / fps  # Assuming each row corresponds to a frame at fps frames per second
    red_channel = data[:, 0]
    green_channel = data[:, 1]
    blue_channel = data[:, 2]

    cut = 3*fps  #Cut the first 3 seconds of data, to remove artifacts from starting the recording
    red_channel = red_channel[cut:]
    green_channel = green_channel[cut:]
    blue_channel = blue_channel[cut:]

    #Remove DC offset (mean value) from each channel separately.
    red_channel = red_channel - np.mean(red_channel)
    green_channel = green_channel - np.mean(green_channel)
    blue_channel = blue_channel - np.mean(blue_channel)

    #Filtering the signal 
    lowCut = 0.5  #Hz
    highCut = 3   #Hz
    b, a = butter(3, [lowCut/(fps/2), highCut/(fps/2)], btype='band')
    red_channel = filtfilt(b, a, red_channel)
    green_channel = filtfilt(b, a, green_channel)
    blue_channel = filtfilt(b, a, blue_channel)

    # if normalizeChannelsSeparately:
    #     red_channel = red_channel / np.max(np.abs(red_channel))
    #     green_channel = green_channel / np.max(np.abs(green_channel))
    #     blue_channel = blue_channel / np.max(np.abs(blue_channel))
    
    #FFT analysis, with windowing and zero padding to get better frequency resolution. The FFT is computed for each color channel separately, and the magnitude spectrum is plotted. The dominant frequency in the area of interest (0.5-4 Hz) is identified for each channel and printed out.
    N = len(red_channel)
    zeroPaddingFactor = 16  #Increase this to get better frequency resolution, but it also increases computation time. A value of 4 means that the FFT will be computed on a signal that is 4 times longer than the original, with zero padding.
    nfft = zeroPaddingFactor * N
    red_channel = np.concatenate((red_channel, np.zeros(nfft - N)))
    green_channel = np.concatenate((green_channel, np.zeros(nfft - N)))
    blue_channel = np.concatenate((blue_channel, np.zeros(nfft - N)))

    #window = np.hanning(N)  #Hanning window to reduce spectral leakage
    red_fft = np.fft.rfft(red_channel)
    green_fft = np.fft.rfft(green_channel)
    blue_fft = np.fft.rfft(blue_channel)
    freqs = np.fft.rfftfreq(nfft, d=1/fps)

    areaOfInterest = (freqs >= lowerbound) & (freqs <= upperbound)
    freqs = freqs[areaOfInterest]
    red_magnitude = red_fft[areaOfInterest]
    green_magnitude = green_fft[areaOfInterest]
    blue_magnitude = blue_fft[areaOfInterest]

    peak_freq_red = freqs[np.argmax(red_magnitude)]
    peak_freq_green = freqs[np.argmax(green_magnitude)]
    peak_freq_blue = freqs[np.argmax(blue_magnitude)]

    #Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, red_magnitude, label='Red Channel', color='red', alpha=0.5)
    plt.plot(freqs, green_magnitude, label='Green Channel', color='green')
    plt.plot(freqs, blue_magnitude, label='Blue Channel', color='blue', alpha=0.5)
    plt.title('Magnitude Spectrum of Color Channels')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(lowerbound, upperbound) #Focus on frequencies up to 6 Hz, which is relevant for heart rate analysis
    plt.legend()
    plt.grid()
    plt.show()


    return peak_freq_red, peak_freq_green, peak_freq_blue


#example usage:
if __name__ == "__main__":
    plot_fft("/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/outputFiler/colorChannels.txt")