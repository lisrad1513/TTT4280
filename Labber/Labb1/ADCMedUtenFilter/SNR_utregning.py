import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

#Function that calculates SNR
def SNR(signal, noise):
    """
    Beregn Signal-to-Noise Ratio (SNR) i desibel (dB).
    
    Parametre:
        signal: numpy array med signalverdier
        noise: numpy array med støyverdier
    
    Returnerer:
        SNR i dB
    """
    power_signal = np.mean(signal**2)
    power_noise = np.mean(noise**2)
    
    if power_noise == 0:
        raise ValueError("Støyens effekt er null, kan ikke beregne SNR")
    
    snr = 10 * np.log10(power_signal / power_noise)
    return snr

# Example usage
if __name__ == "__main__":
    # Eksempeldata
    fs, data = raspi_import('adc_data.bin', channels=3)
    signal = data[:, 0]  # Anta at signalet er i kanal 0
    noise = data[:, 1]   # Anta at støyen er i kanal 1
    
    snr_value = SNR(signal, noise)
    print(f"SNR: {snr_value:.2f} dB")