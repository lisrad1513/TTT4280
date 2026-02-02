import numpy as np
import matplotlib.pyplot as plt
from generateSineSignal import sinus_med_pakke, generer_sinus


def krysskorrelasjon(x, y, fs, remove_dc=True, max_lag=None):
    """
    Beregn krysskorrelasjon r_xy(m) = sum_n x[n] * y[n+m].
    Setter remove_dc=True for å fjerne DC-offset (trekker fra middelverdi).

    Parametre:
        remove_dc: fjern DC-offset (trekker fra middelverdi)
        max_lag: maks |m| som skal sjekkes (i samples). None = alle.

    Returnerer:
        lag_samples: m-verdien (i samples) der |r_xy(m)| er størst
        lag_time_s: tidsforsinkelse i sekunder (m / fs)
        r_xy: selve krysskorrelasjonen
        lags: m-verdier som hører til r_xy
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x og y må være 1D-arrays")
    if fs <= 0:
        raise ValueError("fs må være > 0")
    if remove_dc:
        x = x - np.mean(x)
        y = y - np.mean(y)

    if max_lag is not None:
        if max_lag < 0:
            raise ValueError("max_lag må være >= 0")
        max_lag = int(max_lag)

    # numpy.correlate definisjon: sum a[n+k]*v[n]. Bruk a=y, v=x for å få r_xy(k).
    r_xy = np.correlate(y, x, mode="full")
    lags = np.arange(-(len(x) - 1), len(y))

    if max_lag is not None:
        lag_mask = (lags >= -max_lag) & (lags <= max_lag)
        lags_eval = lags[lag_mask]
        r_xy_eval = r_xy[lag_mask]
    else:
        lags_eval = lags
        r_xy_eval = r_xy

    max_index = int(np.argmax(np.abs(r_xy_eval)))
    lag_samples = int(lags_eval[max_index])
    lag_time_s = lag_samples / fs

    return lag_samples, lag_time_s, r_xy_eval, lags_eval

def krysskorrelasjon_upscaled(x, y, fs, upsample_factor=16, remove_dc=True, max_lag=None):
    """
    Finn forsinkelse mellom to signaler x og y ved hjelp av krysskorrelasjon med oppsampling.

    Parametre:
        upsample_factor: faktor for oppsampling (f.eks. 16)
        remove_dc: fjern DC-offset (trekker fra middelverdi)
        max_lag: maks |m| som skal sjekkes (i samples). None = alle.
    Returnerer:
        lag_samples: forsinkelse i opprinnelige samples
        lag_time_s: tidsforsinkelse i sekunder
        r_xy: krysskorrelasjon fra oppsamplet signal
        lags: lag-verdier (i oppsamplet samples)
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    
    # Oppsampling ved hjelp av numpy.interp
    n_original = len(x)
    n_upsampled = n_original * upsample_factor
    
    # Nye tidsindekser for oppsampling
    t_original = np.arange(n_original)
    t_upsampled = np.linspace(0, n_original - 1, n_upsampled)
    
    # Interpoler signalene
    x_upsampled = np.interp(t_upsampled, t_original, x)
    y_upsampled = np.interp(t_upsampled, t_original, y)
    
    # Kjør krysskorrelasjon på oppsamplet signaler
    fs_upsampled = fs * upsample_factor
    lag_samples_upsampled, lag_time_s, r_xy, lags = krysskorrelasjon(
        x_upsampled, y_upsampled, fs_upsampled, remove_dc=remove_dc, max_lag=max_lag
    )
    
    # Konverter lag tilbake til opprinnelige samples
    lag_samples = lag_samples_upsampled / upsample_factor
    
    return lag_samples, lag_time_s, r_xy, lags
    


def finn_forsinkelse_test():
    """
    Testfunksjon for krysskorrelasjon.
    """
    fs = 1000  # Hz
    varighet = 1.0  # sekunder
    frekvens = 5  # Hz
    delay_samples = 7  # samples

    t = np.arange(0, varighet, 1 / fs)
    x = generer_sinus(t, frekvens, 0, fs)
    y = generer_sinus(t, frekvens, 10, fs)
    # x = sinus_med_pakke(t, frekvens, fs, delay_samples=0)
    # y = sinus_med_pakke(t, frekvens, fs, delay_samples=delay_samples)

    lag_samples, lag_time_s, r_xy, lags = krysskorrelasjon(x, y, fs, True)

    print(f"Forventet forsinkelse: {delay_samples} samples")
    print(f"Funnet forsinkelse:    {lag_samples} samples ({lag_time_s} sekunder)")
	
    plt.figure()
    plt.plot(lags, r_xy)
    plt.title("Krysskorrelasjon r_xy(m)")
    plt.axvline(x=delay_samples, color="green", linestyle="--", label=f"Forventet: {delay_samples} samples")
    plt.axvline(x=lag_samples, color="red", linestyle="--", label=f"Funnet: {lag_samples} samples")
    plt.legend()
    plt.xlim(-500, 500)
    plt.xlabel("Samples (m)")
    plt.ylabel("r_xy")
    plt.grid(True)
    plt.show()

    return lag_samples, lag_time_s, r_xy, lags

if __name__ == "__main__":
    finn_forsinkelse_test()