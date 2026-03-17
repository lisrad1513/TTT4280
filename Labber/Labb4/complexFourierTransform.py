import numpy as np
from scipy.signal import butter, filtfilt


def complex_fourier_transform(
    i_signal,
    q_signal,
    sample_period,
    use_window=True,
    remove_dc=True,
    apply_filter=False,
    filter_type="bandpass",
    lowcut=None,
    highcut=None,
    filter_order=4
):
    """
    Perform a complex Fourier transform on I and Q signals and return
    the Doppler spectrum in Hz.

    Args:
        i_signal: In-phase signal array
        q_signal: Quadrature signal array
        sample_period: Sampling period in seconds
        cut_seconds_start: Number of seconds to remove from the start
        cut_seconds_end: Number of seconds to remove from the end
        use_window: Apply Hann window if True
        remove_dc: Remove mean value if True

        apply_filter: Apply Butterworth filter if True
        filter_type: "lowpass", "highpass", "bandpass", or "bandstop"
        lowcut: Lower cutoff frequency in Hz
        highcut: Upper cutoff frequency in Hz
        filter_order: Butterworth filter order

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
    if sample_period <= 0:
        raise ValueError("sample_period must be positive.")

    # Sampling frequency
    fs = 1 / sample_period
    nyquist = fs / 2

    # Optional filtering
    if apply_filter:
        if filter_type not in ["lowpass", "highpass", "bandpass", "bandstop"]:
            raise ValueError(
                "filter_type must be 'lowpass', 'highpass', 'bandpass', or 'bandstop'."
            )

        if filter_order <= 0:
            raise ValueError("filter_order must be a positive integer.")

        if filter_type in ["lowpass", "highpass"]:
            cutoff = highcut if filter_type == "lowpass" else lowcut

            if cutoff is None:
                raise ValueError(
                    f"{filter_type} requires {'highcut' if filter_type == 'lowpass' else 'lowcut'} to be set."
                )
            if not (0 < cutoff < nyquist):
                raise ValueError(
                    f"Cutoff frequency must satisfy 0 < cutoff < Nyquist ({nyquist:.3f} Hz)."
                )

            wn = cutoff / nyquist
            b, a = butter(filter_order, wn, btype="low")

            if filter_type == "highpass":
                b, a = butter(filter_order, wn, btype="high")

        else:
            if lowcut is None or highcut is None:
                raise ValueError(f"{filter_type} requires both lowcut and highcut.")
            if not (0 < lowcut < highcut < nyquist):
                raise ValueError(
                    f"Cutoffs must satisfy 0 < lowcut < highcut < Nyquist ({nyquist:.3f} Hz)."
                )

            wn = [lowcut / nyquist, highcut / nyquist]
            btype = "bandpass" if filter_type == "bandpass" else "bandstop"
            b, a = butter(filter_order, wn, btype=btype)

        i_signal = filtfilt(b, a, i_signal)
        q_signal = filtfilt(b, a, q_signal)

    complex_signal = i_signal + 1j * q_signal

    if use_window:
        window = np.hanning(len(complex_signal))
        complex_signal = complex_signal * window

    fft_result = np.fft.fft(complex_signal)
    frequencies = np.fft.fftfreq(len(complex_signal), d=sample_period)

    fft_shifted = np.fft.fftshift(fft_result)
    frequencies_shifted = np.fft.fftshift(frequencies)

    spectrum = np.abs(fft_shifted)
    db_spectrum = 10 * np.log10(spectrum + 1e-12)  # Add small value to avoid log(0)
    db_spectrum = db_spectrum - np.max(db_spectrum)  # Normalize to max at 0 dB
    doppler_shift = frequencies_shifted

    return frequencies_shifted, spectrum, db_spectrum, doppler_shift