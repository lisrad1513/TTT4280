import numpy as np

def estimate_doppler_resolution(
    frequencies,
    spectrum,
    sample_period,
    spectrum_unit="db_magnitude",
    dc_exclusion_hz=20.0,
    search_band=None,
    peak_min_distance_hz=None,
):
    """
    Estimate measured Doppler resolution from the 3 dB width of the main peak
    and compare it with theoretical Doppler resolution.

    Parameters
    ----------
    frequencies : array-like
        Frequency axis in Hz.
    spectrum : array-like
        Spectrum values.
        Allowed units:
        - "db_magnitude"
        - "db_power"
        - "linear_magnitude"
        - "linear_power"
    sample_period : float
        Sampling period in seconds.
    spectrum_unit : str
        Unit of input spectrum.
    dc_exclusion_hz : float
        Exclude bins around 0 Hz when searching for the Doppler peak.
    search_band : tuple or None
        Optional tuple (f_min, f_max) restricting where the peak is searched.
    peak_min_distance_hz : float or None
        Optional parameter reserved for future use if you want to reject
        nearby multiple peaks. Currently not used.

    Returns
    -------
    result : dict
        Dictionary containing:
        - peak_frequency_hz
        - peak_value_db
        - threshold_3db
        - f_left_3db
        - f_right_3db
        - bandwidth_3db_hz
        - theoretical_resolution_hz
        - frequency_bin_spacing_hz
        - observation_time_s
        - num_samples_estimated
        - ratio_measured_to_theory
    """

    frequencies = np.asarray(frequencies, dtype=float)
    spectrum = np.asarray(spectrum, dtype=float)

    if frequencies.ndim != 1 or spectrum.ndim != 1:
        raise ValueError("frequencies and spectrum must both be 1D arrays.")

    if len(frequencies) != len(spectrum):
        raise ValueError("frequencies and spectrum must have the same length.")

    if len(frequencies) < 3:
        raise ValueError("Need at least 3 points in the spectrum.")

    if sample_period <= 0:
        raise ValueError("sample_period must be positive.")

    unit = spectrum_unit.lower()

    # Convert to dB magnitude scale for 3 dB width detection
    if unit == "db_magnitude":
        spectrum_db = spectrum.copy()
    elif unit == "db_power":
        # In power dB, a 3 dB drop is still a 3 dB drop
        spectrum_db = spectrum.copy()
    elif unit == "linear_magnitude":
        eps = 1e-30
        spectrum_db = 20.0 * np.log10(np.maximum(np.abs(spectrum), eps))
    elif unit == "linear_power":
        eps = 1e-30
        spectrum_db = 10.0 * np.log10(np.maximum(spectrum, eps))
    else:
        raise ValueError(
            "spectrum_unit must be one of: "
            "'db_magnitude', 'db_power', 'linear_magnitude', 'linear_power'"
        )

    # Sort by frequency in case input is not sorted
    sort_idx = np.argsort(frequencies)
    frequencies = frequencies[sort_idx]
    spectrum_db = spectrum_db[sort_idx]

    # Frequency spacing
    df_array = np.diff(frequencies)
    df = float(np.median(df_array))

    if df <= 0:
        raise ValueError("Frequency axis must be strictly increasing.")

    # Estimate number of time samples from df and sample_period:
    # df = 1 / (N * sample_period)
    # N = 1 / (df * sample_period)
    num_samples_estimated = int(round(1.0 / (df * sample_period)))
    observation_time_s = num_samples_estimated * sample_period
    theoretical_resolution_hz = 1.0 / observation_time_s

    # Build mask for signal peak search
    peak_mask = np.ones_like(frequencies, dtype=bool)
    peak_mask &= np.abs(frequencies) > dc_exclusion_hz

    if search_band is not None:
        f_min, f_max = search_band
        peak_mask &= (frequencies >= f_min) & (frequencies <= f_max)

    if not np.any(peak_mask):
        raise ValueError("No frequencies left after applying search constraints.")

    candidate_indices = np.where(peak_mask)[0]
    peak_index = candidate_indices[np.argmax(spectrum_db[candidate_indices])]

    peak_frequency_hz = frequencies[peak_index]
    peak_value_db = spectrum_db[peak_index]
    threshold_3db = peak_value_db - 3.0

    # Find left crossing
    left_index = peak_index
    while left_index > 0 and spectrum_db[left_index] > threshold_3db:
        left_index -= 1

    if left_index == 0 and spectrum_db[left_index] > threshold_3db:
        raise ValueError("Could not find left 3 dB crossing.")

    # Linear interpolation for better crossing estimate
    if left_index == peak_index:
        f_left_3db = frequencies[left_index]
    else:
        f1, f2 = frequencies[left_index], frequencies[left_index + 1]
        y1, y2 = spectrum_db[left_index], spectrum_db[left_index + 1]

        if y2 == y1:
            f_left_3db = f1
        else:
            f_left_3db = f1 + (threshold_3db - y1) * (f2 - f1) / (y2 - y1)

    # Find right crossing
    right_index = peak_index
    while right_index < len(spectrum_db) - 1 and spectrum_db[right_index] > threshold_3db:
        right_index += 1

    if right_index == len(spectrum_db) - 1 and spectrum_db[right_index] > threshold_3db:
        raise ValueError("Could not find right 3 dB crossing.")

    # Linear interpolation for better crossing estimate
    if right_index == peak_index:
        f_right_3db = frequencies[right_index]
    else:
        f1, f2 = frequencies[right_index - 1], frequencies[right_index]
        y1, y2 = spectrum_db[right_index - 1], spectrum_db[right_index]

        if y2 == y1:
            f_right_3db = f2
        else:
            f_right_3db = f1 + (threshold_3db - y1) * (f2 - f1) / (y2 - y1)

    bandwidth_3db_hz = f_right_3db - f_left_3db
    ratio_measured_to_theory = bandwidth_3db_hz / theoretical_resolution_hz

    return {
        "peak_frequency_hz": peak_frequency_hz,
        "peak_value_db": peak_value_db,
        "threshold_3db": threshold_3db,
        "f_left_3db": f_left_3db,
        "f_right_3db": f_right_3db,
        "bandwidth_3db_hz": bandwidth_3db_hz,
        "theoretical_resolution_hz": theoretical_resolution_hz,
        "frequency_bin_spacing_hz": df,
        "observation_time_s": observation_time_s,
        "num_samples_estimated": num_samples_estimated,
        "ratio_measured_to_theory": ratio_measured_to_theory,
    }