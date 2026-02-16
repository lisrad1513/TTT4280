import numpy as np
import matplotlib.pyplot as plt

from generateSineSignal import generer_sinus, sinus_med_pakke
from finnForsinkelse import krysskorrelasjon, krysskorrelasjon_upscaled

# Function below

def find_theta(n_31, n_21, n_32):
    """
    Beregn vinkelen theta fra korrelasjonsverdier.
    
    Basert på formel (II.29):
        theta = atan(sqrt(3) * (n_31 + n_21) / (n_31 - n_21 + 2*n_32))
    
    Parametre:
        n_31, n_21, n_32: korrelasjonsverdier (integers i samples)
    
    Returnerer:
        theta: vinkelen i radianer
    """

    #print(f"n_31: {n_31}, n_21: {n_21}, n_32: {n_32}")

    denominator = n_31 - n_21 + 2 * n_32
    numeratror = np.sqrt(3) * (n_31 + n_21)

    if denominator == 0:
        #return 0, 0
        raise ValueError("Denominator i theta-formelen er 0, kan ikke beregne theta.")
    
    theta_rad = np.arctan2(denominator, numeratror)
    # arctan2 tar seg av kvadrantproblematikken, så ingen ekstra justering er nødvendig.
    # if denominator < 0:
    #     theta_rad += np.pi  # Juster for riktig kvadrant

    theta_deg = np.degrees(theta_rad)

    return theta_rad, theta_deg


# Example usage
if __name__ == "__main__":
    fs = 10000  # Sampling frequency in Hz
    varighet = 1.0  # Duration in seconds
    frekvens = 1000  # Frequency of the sine wave in Hz

    t = np.arange(0, varighet, 1 / fs)
    m1 = sinus_med_pakke(t, frekvens, fs, delay_samples=0)
    m2 = sinus_med_pakke(t, frekvens, fs, delay_samples=0)
    m3 = sinus_med_pakke(t, frekvens, fs, delay_samples=4)

    # n_31 = krysskorrelasjon_upscaled(m1, m3, fs, True)[0]
    # n_21 = krysskorrelasjon_upscaled(m1, m2, fs, True)[0]
    # n_32 = krysskorrelasjon_upscaled(m3, m2, fs, True)[0]

    n_31 = krysskorrelasjon(m1, m3, fs, True)[0]
    n_21 = krysskorrelasjon(m1, m2, fs, True)[0]
    n_32 = krysskorrelasjon(m3, m2, fs, True)[0]

    theta_rad, theta_deg = find_theta(n_31, n_21, n_32)
    print(f"Vinkel theta: {theta_rad:.4f} radianer, {theta_deg:.2f} grader")