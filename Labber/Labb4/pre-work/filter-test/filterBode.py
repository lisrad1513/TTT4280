import numpy as np
import matplotlib.pyplot as plt
import csv

# -----------------------------
# Read CSV data
# -----------------------------
header = []
data1 = []
data2 = []

filename1 = 'ELSYSS6/Sensor/Labber/Labb4/pre-work/filter-test/filterIFItoADC1.csv'
filename2 = 'ELSYSS6/Sensor/Labber/Labb4/pre-work/filter-test/filterIFQtoADC2.csv'

with open(filename1, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data1.append(values)

with open(filename2, mode='r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data2.append(values)

# -----------------------------
# Extract columns
# -----------------------------
freq1 = np.array([p[0] for p in data1])
filt1 = np.array([p[1] for p in data1])

freq2 = np.array([p[0] for p in data2])
filt2 = np.array([p[1] for p in data2])

# -----------------------------
# Find -3 dB thresholds
# -----------------------------
threshold1 = np.max(filt1) - 3
threshold2 = np.max(filt2) - 3

freq1_low = None
freq1_high = None

for i in range(1, len(filt1)):
    if freq1_low is None and filt1[i - 1] < threshold1 and filt1[i] >= threshold1:
        freq1_low = freq1[i]
    if filt1[i - 1] >= threshold1 and filt1[i] < threshold1:
        freq1_high = freq1[i]

freq2_low = None
freq2_high = None

for i in range(1, len(filt2)):
    if freq2_low is None and filt2[i - 1] < threshold2 and filt2[i] >= threshold2:
        freq2_low = freq2[i]
    if filt2[i - 1] >= threshold2 and filt2[i] < threshold2:
        freq2_high = freq2[i]

# -----------------------------
# Print results
# -----------------------------
print(f"I-kanal: nedre knekkfrekvens = {freq1_low:.2f} Hz, øvre knekkfrekvens = {freq1_high:.2f} Hz")
print(f"Q-kanal: nedre knekkfrekvens = {freq2_low:.2f} Hz, øvre knekkfrekvens = {freq2_high:.2f} Hz")

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(11, 6))

# Main curves
plt.plot(freq1, filt1, linewidth=2.5, label='I-kanal')
plt.plot(freq2, filt2, linewidth=2.5, label='Q-kanal')

# Threshold lines
plt.axhline(threshold1, linestyle='--', linewidth=1.5, alpha=0.8, label='-3 dB nivå')
#plt.axhline(threshold2, linestyle='--', linewidth=1.5, alpha=0.8, label='Q-kanal, -3 dB nivå')

# Vertical cutoff lines for I channel
if freq1_low is not None:
    plt.axvline(freq1_low, linestyle='--', linewidth=1.2, alpha=0.8)
    plt.text(freq1_low, 15.4, f'{freq1_low:.1f} Hz', rotation=90,
             va='bottom', ha='right', fontsize=9)

# if freq1_high is not None:
#     plt.axvline(freq1_high, linestyle='--', linewidth=1.2, alpha=0.8)
#     plt.text(freq1_high, 15.4, f'{freq1_high:.1f} Hz', rotation=90,
#              va='bottom', ha='right', fontsize=9)

# # Vertical cutoff lines for Q channel
# if freq2_low is not None:
#     plt.axvline(freq2_low, linestyle=':', linewidth=1.2, alpha=0.8)
#     plt.text(freq2_low, 16.2, f'{freq2_low:.1f} Hz', rotation=90,
#              va='bottom', ha='left', fontsize=9)

if freq2_high is not None:
    plt.axvline(freq2_high, linestyle='--', linewidth=1.2, alpha=0.8)
    plt.text(freq2_high, 16.2, f'{freq2_high:.1f} Hz', rotation=90,
             va='bottom', ha='left', fontsize=9)

# Labels and styling
plt.xscale('log')
plt.xlim(1, 10000)
plt.ylim(15, 28)

plt.xlabel("Frekvens [Hz]", fontsize=12)
plt.ylabel("Forsterkning [dB]", fontsize=12)
plt.title("Frekvensrespons til forsterkeren", fontsize=14, pad=12)

plt.grid(which='both', linestyle=':', linewidth=0.7, alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()

plt.show()