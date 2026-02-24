from extractColorChannels import run_video_roi_extraction
from plotValues import plot_values
from fft import plot_fft

video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/fingerLisa2.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/testopptak.mp4"
output_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/outputFiler/colorChannels.txt"
defineNewROI = True

if defineNewROI:
    run_video_roi_extraction(video_file, output_file)

plot_values(output_file)

peak_red, peak_green, peak_blue = plot_fft(output_file, 30, .5, 6, True)

print(f'Puls i bpm for rød kanal: {peak_red:.2f} Hz, {peak_red * 60:.2f} bpm')
print(f'Puls i bpm for grønn kanal: {peak_green:.2f} Hz, {peak_green * 60:.2f} bpm')
print(f'Puls i bpm for blå kanal: {peak_blue:.2f} Hz, {peak_blue * 60:.2f} bpm')
