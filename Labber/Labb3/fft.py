import numpy as np
import matplotlib.pyplot as plt
import os

#FFT analysis of each color channel, to find the dominant frequencies in the signal
def plot_fft(data_path, normalizeChannelsSeparately=True):

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path relative to the script location
    data_path = os.path.join(script_dir, data_path)

    # Check if file exists
    if not os.path.exists(data_path):
        print(f"Error: File not found at {data_path}")
        exit()

    try:
        data = np.genfromtxt(data_path, delimiter=" ", skip_header=1)
    except Exception as e:
        print(f"Error loading data: {e}")
        exit()

    print(data)  # Print the loaded data to verify its structure

    # Verify data has correct shape
    if data.ndim != 2 or data.shape[1] < 3:
        print(f"Error: Data shape is incorrect. Expected (n, 3), got {data.shape}")
        exit()

    red_channel = data[:, 0]
    green_channel = data[:, 1]
    blue_channel = data[:, 2]

    # Stack channels for processing
    x = np.column_stack([red_channel, green_channel, blue_channel])

    # Remove DC offset (mean value) from each channel separately
    x = x - np.mean(x, axis=0, keepdims=True)

    # Number of time samples
    N = x.shape[0]

    # Sampling frequency fs in Hz (assuming 30 fps)
    fs = 30.0
    sample_period = 1.0 / fs

    # Window function
    windowFunction = 'hamming'  # Options: 'none', 'hann', 'hamming', 'blackman', 'bartlett'
    if windowFunction == 'none':
        w = np.ones((N, 1))
    elif windowFunction == 'hann':
        w = np.hanning(N)[:, None]
    elif windowFunction == 'hamming':
        w = np.hamming(N)[:, None]
    elif windowFunction == 'blackman':
        w = np.blackman(N)[:, None]
    elif windowFunction == 'bartlett':
        w = np.bartlett(N)[:, None]
    else:
        print("Unknown window function, defaulting to none.")
        w = np.ones((N, 1))

    # Apply the window to each channel
    xw = x * w

    # Zero padding / nfft choice (nfft > N adds zero padding)
    nfftChooser = True  # True: nfft = next power of 2 above N, False: nfft = N
    if nfftChooser:
        nfft = 2**int(np.ceil(np.log2(N)))
    else:
        nfft = N

    # Compute one sided FFT for real signals along the time axis (axis=0)
    X = np.fft.rfft(xw, n=nfft, axis=0)

    # Frequency axis for rfft, in Hz, using the real sample period
    freq = np.fft.rfftfreq(nfft, d=sample_period)

    # Magnitude spectrum (absolute value of complex FFT)
    mag = np.abs(X) / N

    # For a one sided spectrum, energy that was split between positive and negative frequencies is folded into the positive side
    if nfft > 1:
        mag[1:-1, :] *= 2.0

    # Convert magnitude to decibels
    eps = 1e-12
    if normalizeChannelsSeparately:
        mag_norm = np.zeros_like(mag)
        for i in range(mag.shape[1]):
            mag_norm[:, i] = mag[:, i] / (np.max(mag[:, i]) + eps)  # Normalize to max of mag for each channel separately
            mag_db = 10.0 * np.log10(mag_norm + eps)
    else:
        mag_db = 10.0 * np.log10(mag / (np.max(mag[:, 0]) + eps) + eps)  # Normalize all channels together based on the max of the first channel

    plt.figure(figsize=(10, 6))
    plt.plot(freq, mag_db[:, 0], label='Red Channel', color='red')
    plt.plot(freq, mag_db[:, 1], label='Green Channel', color='green')
    plt.plot(freq, mag_db[:, 2], label='Blue Channel', color='blue')

    # Show 0 to 15 Hz range to focus on relevant frequencies
    plt.xlim(0, 15)    
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('FFT Analysis of Color Channels')
    plt.grid(True)
    plt.legend()
    plt.show()


#example usage:
if __name__ == "__main__":
    plot_fft("/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/outputFiler/colorChannels.txt")