from extractColorChannels import run_video_roi_extraction
from plotValues import plot_values
from fft import plot_fft
from snr import snr_from_file_all

#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/fingerLisa2.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/fingerEven1.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/robusthetstest/hvilepulsVsHøypuls/fingerEven70bpm.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/robusthetstest/hvilepulsVsHøypuls/fingerEven114bpm.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/robusthetstest/temperatur/fingerEven76bpmVarm.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/robusthetstest/temperatur/fingerEven74bpmKald.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/robusthetstest/andreKroppsdeler/oyreflippEven77bpm.mp4"
video_file = "ELSYSS6/Sensor/Labber/Labb3/videofiler/robusthetstest/lys/fingerEven70bpmMoerkt.mp4"
#video_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/videofiler/robusthetstest/andreKroppsdeler/handleddEven73bpmIphone.mp4"
output_file = "/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/outputFiler/colorChannels.txt"
defineNewROI = True

removeFirstNSeconds = 5 # Remove first N seconds of signal
removeLastNSeconds = 5  # Remove last N seconds of signal

if defineNewROI:
    run_video_roi_extraction(video_file, output_file, removeFirstNSeconds, removeLastNSeconds)

plot_values(output_file)

peak_red, peak_green, peak_blue = plot_fft(output_file, 30, .5, 6, True)

print("-----------------------------------")
print("Puls i Hz og bpm for hver kanal:")
print(f'\t Rød kanal: {peak_red:.2f} Hz, {peak_red * 60:.2f} bpm')
print(f'\t Grønn kanal: {peak_green:.2f} Hz, {peak_green * 60:.2f} bpm')
print(f'\t Blå kanal: {peak_blue:.2f} Hz, {peak_blue * 60:.2f} bpm')


print("-----------------------------------")
result = snr_from_file_all(output_file, skip_header=0)
print("SNR for hver kanal:")
print(f'\t Rød kanal: {result[0]:.2f} dB')
print(f'\t Grønn kanal: {result[1]:.2f} dB')
print(f'\t Blå kanal: {result[2]:.2f} dB')