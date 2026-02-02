#A script that displays 5 values for zeta, and the corresponding filter response plots
import numpy as np
import matplotlib.pyplot as plt 

zeta_values = [0.1, 0.45, 0.5, 0.55, 1.0]
f0 = 1000  # Natural frequency in Hz
frequencies = np.logspace(1, 5, 1000)  # Frequencies from 10 Hz to 100 kHz  

def findRfromZeta(zeta, L=100e-3, C=470e-6):
    """Calculate resistance R for a given damping ratio zeta, inductance L, and capacitance C."""
    R = 2 * zeta * L * (1 / np.sqrt(L * C))
    return R

for zeta in zeta_values:
    # Calculate the magnitude response |H(f)|
    H_f = 1 / np.sqrt((1 - (frequencies / f0)**2)**2 + (2 * zeta * (frequencies / f0))**2)
    H_f_db = 20 * np.log10(H_f)  # Convert to dB

    plt.plot(frequencies, H_f_db, label=f'ζ = {zeta}')
    print(f'For zeta = {zeta}, R = {findRfromZeta(zeta):.2f} Ohms')


plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude |H(f)| (dB)')
plt.title('Filter Response for Different Damping Ratios')
plt.axhline(y=-3, color='red', linestyle='--', label='-3 dB Line')
plt.xlim(100, 10000)
plt.ylim(-30, 15)
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()