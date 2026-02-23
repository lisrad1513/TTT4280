import numpy as np
import matplotlib.pyplot as plt
import os

def plot_values(data_path):
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

    time = np.arange(len(data)) / 30.  # Assuming each row corresponds to a frame at 30 fps
    red_channel = data[:, 0]
    green_channel = data[:, 1]
    blue_channel = data[:, 2]   

    plt.figure(figsize=(10, 6))
    plt.plot(time, red_channel, label='Red Channel', color='red')
    plt.plot(time, green_channel, label='Green Channel', color='green')
    plt.plot(time, blue_channel, label='Blue Channel', color='blue')   
    plt.title('Color Channel Intensities Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Mean Intensity')
    plt.legend()
    plt.grid()
    plt.show()