import numpy as np
from scipy import signal

def complex_fourier_transform(i_signal, q_signal, sample_period, use_window=True, remove_dc=True):
    """
    Perform a complex Fourier transform on I and Q signals and return
    the Doppler spectrum in Hz.

    Args:
        i_signal: In-phase signal array
        q_signal: Quadrature signal array
        sample_period: Sampling period in seconds
        use_window: Apply Hann window if True
        remove_dc: Remove mean value if True

    Returns:
        frequencies_shifted: Frequency axis in Hz
        spectrum: Magnitude spectrum
        doppler_shift: Same as frequencies_shifted
    """
    i_signal = np.asarray(i_signal)
    q_signal = np.asarray(q_signal)

    if i_signal.ndim == 0:
        raise ValueError("i_signal is a scalar, not an array.")
    if q_signal.ndim == 0:
        raise ValueError("q_signal is a scalar, not an array.")
    if len(i_signal) != len(q_signal):
        raise ValueError("i_signal and q_signal must have the same length")

    if remove_dc:
        i_signal = i_signal - np.mean(i_signal)
        q_signal = q_signal - np.mean(q_signal)

    complex_signal = i_signal + 1j * q_signal

    if use_window:
        window = np.hanning(len(complex_signal))
        complex_signal = complex_signal * window

    fft_result = np.fft.fft(complex_signal)
    frequencies = np.fft.fftfreq(len(complex_signal), d=sample_period)

    fft_shifted = np.fft.fftshift(fft_result)
    frequencies_shifted = np.fft.fftshift(frequencies)

    spectrum = np.abs(fft_shifted)
    doppler_shift = frequencies_shifted

    return frequencies_shifted, spectrum, doppler_shift