import numpy as np

def finn_forsinkelse(x, y, fs):
    """
    Finner tidsforsinkelse mellom to signaler x og y
    ved hjelp av krysskorrelasjon.
    
    Returnerer:
    n_delay : forsinkelse i antall sampler
    tau     : forsinkelse i sekunder
    rxy     : krysskorrelasjonsfunksjonen
    lags    : lag-akse (sampler)
    """

    # Fjern DC-komponent
    x = x - np.mean(x)
    y = y - np.mean(y)

    # Krysskorrelasjon
    rxy = np.correlate(x, y, mode='full')

    # Lag-akse
    lags = np.arange(-len(x) + 1, len(x))

    # Finn maksimum av absoluttverdi
    n_delay = lags[np.argmax(np.abs(rxy))]
    tau = n_delay / fs

    return n_delay, tau, rxy, lags