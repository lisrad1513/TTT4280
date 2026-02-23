from extractColorChannels import run_video_roi_extraction
from plotValues import plot_values
from fft import plot_fft

video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/fingerLisa2.mp4"
output_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/outputFiler/colorChannels.txt"
run_video_roi_extraction(video_file, output_file)

plot_values(output_file)

plot_fft(output_file)