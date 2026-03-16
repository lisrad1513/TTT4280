import numpy as np
from scipy import signal

def complex_fourier_transform(i_signal, q_signal):
    """
    Performs a complex Fourier transform on I and Q signals to find the spectrum
    and detect both positive and negative Doppler shifts.
    
    Args:
        i_signal: In-phase (I) component array
        q_signal: Quadrature (Q) component array
    
    Returns:
        frequencies: Frequency array
        spectrum: Complex spectrum (magnitude)
        doppler_shift: Doppler shift values
    """
    # Convert to numpy arrays if needed
    i_signal = np.asarray(i_signal)
    q_signal = np.asarray(q_signal)

    #remove DC component
    i_signal = signal.detrend(i_signal)
    q_signal = signal.detrend(q_signal)
    
    # Combine I and Q into complex signal
    complex_signal = i_signal + 1j * q_signal
    
    # Compute FFT
    fft_result = np.fft.fft(complex_signal)
    
    # Get frequencies (centered around 0)
    frequencies = np.fft.fftfreq(len(complex_signal))
    
    # Shift zero frequency to center
    fft_shifted = np.fft.fftshift(fft_result)
    frequencies_shifted = np.fft.fftshift(frequencies)
    
    # Calculate magnitude spectrum
    spectrum = np.abs(fft_shifted)
    
    # Doppler shift corresponds to frequency offset
    doppler_shift = frequencies_shifted
    
    return frequencies_shifted, spectrum, doppler_shift