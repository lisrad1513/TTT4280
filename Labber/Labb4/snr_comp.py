import numpy as np

def estimate_snr_from_spectrum(
    frequencies,
    spectrum,
    spectrum_unit="linear",
    dc_exclusion_hz=20.0,
    guard_hz=10.0,
    search_band=None,
    use_peak_power=True,
):
    """
    Estimate SNR from a Doppler spectrum.

    Parameters
    ----------
    frequencies : array-like
        Frequency axis in Hz.
    spectrum : array-like
        Spectrum values. Can be:
        - linear magnitude
        - linear power
        - dB magnitude
        - dB power
    spectrum_unit : str
        One of:
        - "linear"            -> treated as linear magnitude
        - "linear_magnitude"  -> treated as linear magnitude
        - "linear_power"      -> treated as linear power
        - "db"                -> treated as dB power
        - "db_power"          -> treated as dB power
        - "db_magnitude"      -> treated as dB magnitude
    dc_exclusion_hz : float
        Exclude frequencies around 0 Hz when looking for the signal
        and when estimating noise.
    guard_hz : float
        Exclude frequencies around the detected signal peak when
        estimating the noise floor.
    search_band : tuple or None
        Optional frequency search interval for signal detection:
        (f_min, f_max).
        Example: (-500, 500)
    use_peak_power : bool
        If True, use the peak bin power as signal power.
        If False, integrate power in the guard region around the peak.

    Returns
    -------
    result : dict
        Dictionary with:
        - snr_db
        - snr_linear
        - signal_freq_hz
        - signal_power
        - noise_power
        - peak_index
    """
    frequencies = np.asarray(frequencies, dtype=float)
    spectrum = np.asarray(spectrum, dtype=float)

    if frequencies.ndim != 1 or spectrum.ndim != 1:
        raise ValueError("frequencies and spectrum must be 1D arrays.")

    if len(frequencies) != len(spectrum):
        raise ValueError("frequencies and spectrum must have the same length.")

    if len(frequencies) < 3:
        raise ValueError("Need at least 3 spectrum points.")

    unit = spectrum_unit.lower()

    # Convert input spectrum to linear power
    if unit in ["linear", "linear_magnitude"]:
        power_spectrum = np.abs(spectrum) ** 2
    elif unit in ["db", "db_power"]:
        power_spectrum = 10 ** (spectrum / 10.0)
    elif unit == "db_magnitude":
        magnitude_linear = 10 ** (spectrum / 20.0)
        power_spectrum = magnitude_linear ** 2
    else:
        raise ValueError(
            "spectrum_unit must be one of: "
            "'linear', 'linear_magnitude', 'linear_power', "
            "'db', 'db_power', 'db_magnitude'"
        )

    if np.any(power_spectrum < 0):
        raise ValueError("Power spectrum contains negative values.")

    # Build mask for candidate signal region
    signal_mask = np.ones_like(frequencies, dtype=bool)

    # Exclude DC region
    signal_mask &= np.abs(frequencies) > dc_exclusion_hz

    # Restrict to optional search band
    if search_band is not None:
        f_min, f_max = search_band
        signal_mask &= (frequencies >= f_min) & (frequencies <= f_max)

    if not np.any(signal_mask):
        raise ValueError("No valid bins left for signal search.")

    # Find strongest peak outside excluded regions
    candidate_indices = np.where(signal_mask)[0]
    peak_index = candidate_indices[np.argmax(power_spectrum[candidate_indices])]
    signal_freq_hz = frequencies[peak_index]

    # Build noise mask: exclude DC and signal neighborhood
    noise_mask = np.ones_like(frequencies, dtype=bool)
    noise_mask &= np.abs(frequencies) > dc_exclusion_hz
    noise_mask &= np.abs(frequencies - signal_freq_hz) > guard_hz

    if search_band is not None:
        noise_mask &= (frequencies >= f_min) & (frequencies <= f_max)

    if not np.any(noise_mask):
        raise ValueError("No valid bins left for noise estimation.")

    # Estimate noise power
    # Using median is more robust than mean against extra peaks/spurs
    noise_power = np.median(power_spectrum[noise_mask])

    # Estimate signal power
    if use_peak_power:
        signal_power = power_spectrum[peak_index]
    else:
        signal_region = np.abs(frequencies - signal_freq_hz) <= guard_hz
        signal_power = np.sum(power_spectrum[signal_region])

    if noise_power <= 0:
        raise ValueError("Estimated noise power is non-positive.")

    snr_linear = signal_power / noise_power
    snr_db = 10.0 * np.log10(snr_linear)

    return {
        "snr_db": snr_db,
        "snr_linear": snr_linear,
        "signal_freq_hz": signal_freq_hz,
        "signal_power": signal_power,
        "noise_power": noise_power,
        "peak_index": peak_index,
    }