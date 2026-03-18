import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from complexFourierTransform import complex_fourier_transform
from resolution import estimate_doppler_resolution
from snr_comp import estimate_snr_from_spectrum
from speedConversion import (
    convert_distance_and_time_to_speed,
    convert_doppler_shift_to_speed,
)

sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import


# Constants
SAMPLING_FREQUENCY = 31250          # Hz
RADAR_FREQUENCY = 24.13e9           # Hz
CHANNELS = 3
SPEEDS_TESTED = 3
READINGS_PER_SPEED = 4
DECIMALS = 2

SPECIFICATIONS_FILE = "ELSYSS6/Sensor/Labber/Labb4/speed_test/specifications.csv"

#SPECTRUM_TO_PLOT_INDEX = 1  # Index of the measurement for which to plot the spectrum (0-based)
#SPECTRUM_TO_PLOT_INDEX = 6  # Index of the measurement for which to plot the spectrum (0-based)
#SPECTRUM_TO_PLOT_INDEX = 7  # Index of the measurement for which to plot the spectrum (0-based)
SPECTRUM_TO_PLOT_INDEX = 10  # Index of the measurement for which to plot the spectrum (0-based)
#SPECTRUM_TO_PLOT_INDEX = 11  # Index of the measurement for which to plot the spectrum (0-based)


def read_specifications_csv(filename):
    """
    Read measurement specifications from CSV file.

    Returns
    -------
    dict
        Dictionary containing lists for each column.
    """
    rows = []

    with open(filename, mode="r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # Not used directly, but kept in case needed later

        for row in csvreader:
            rows.append(row)

    specifications = {
        "name": [row[0] for row in rows],
        "file_path": [row[1] for row in rows],
        "time_cut_first": [float(row[2]) for row in rows],
        "time_cut_last": [float(row[3]) for row in rows],
        "filter_lower": [float(row[4]) for row in rows],
        "filter_upper": [float(row[5]) for row in rows],
        "length": [float(row[6]) for row in rows],
        "time": [float(row[7]) for row in rows],
    }

    return specifications


def load_measurement_data(file_path, time_cut_first, time_cut_last, sampling_frequency, channels):
    """
    Load measurement data and cut away unwanted parts at start and end.

    Returns
    -------
    tuple
        sample_period, i_channel, q_channel
    """
    sample_period, data = raspi_import(file_path, channels)

    cut_samples_start = int(time_cut_first * sampling_frequency)
    cut_samples_end = int(len(data) - (time_cut_last * sampling_frequency))

    # I and Q channels
    i_channel = data[cut_samples_start:cut_samples_end, 2]
    q_channel = data[cut_samples_start:cut_samples_end, 1]

    return sample_period, i_channel, q_channel


def analyze_single_measurement(specifications, measurement_index):
    """
    Analyze one measurement and return all relevant results.

    Returns
    -------
    dict
        Results for one measurement.
    """
    sample_period, i_channel, q_channel = load_measurement_data(
        file_path=specifications["file_path"][measurement_index],
        time_cut_first=specifications["time_cut_first"][measurement_index],
        time_cut_last=specifications["time_cut_last"][measurement_index],
        sampling_frequency=SAMPLING_FREQUENCY,
        channels=CHANNELS,
    )

    frequencies_shifted, spectrum, db_spectrum, doppler = complex_fourier_transform(
        i_channel,
        q_channel,
        sample_period,
        True,                                            # apply_window
        True,                                            # remove_dc
        True,                                            # shift_frequencies
        "highpass",                                      # filter_type
        specifications["filter_lower"][measurement_index],  # filter_lower
        None,                                            # filter_upper
        4,                                               # filter_order
    )

    peak_index = np.argmax(spectrum)
    doppler_frequency = frequencies_shifted[peak_index]

    speed_doppler = convert_doppler_shift_to_speed(doppler_frequency, RADAR_FREQUENCY)
    speed_timer = convert_distance_and_time_to_speed(
        specifications["length"][measurement_index],
        specifications["time"][measurement_index],
    )

    snr_result = estimate_snr_from_spectrum(
        frequencies=frequencies_shifted,
        spectrum=db_spectrum,
        spectrum_unit="db_magnitude",
        dc_exclusion_hz=20,
        guard_hz=15,
        search_band=(-600, 600),
        use_peak_power=True,
    )

    resolution_result = estimate_doppler_resolution(
        frequencies=frequencies_shifted,
        spectrum=db_spectrum,
        sample_period=sample_period,
        spectrum_unit="db_magnitude",
        dc_exclusion_hz=20,
        search_band=(-600, 600),
    )

    return {
        "speed_doppler": speed_doppler,
        "speed_timer": speed_timer,
        "snr_db": snr_result["snr_db"],
        "resolution_3db_hz": resolution_result["bandwidth_3db_hz"],
        "frequencies_shifted": frequencies_shifted,
        "db_spectrum": db_spectrum,
        "spectrum": spectrum,
        "doppler_frequency": doppler_frequency,
    }


def summarize_group(values):
    """
    Return mean and standard deviation of a list of values.
    """
    return np.mean(values), np.std(values)


def plot_spectrum(
    frequencies_shifted,
    db_spectrum,
    doppler_frequency,
    x_label="Frekvens [Hz]",
    y_label="Magnitude [dB]",
    title="Doppler-spektrum",
    type="db",
    x_padding_factor=1.6,
    y_padding_db=5.0,
    y_padding_mag=5.0,
    show_peak=True,
    show_peak_line=True,
    focus_on_peak=True,
):
    """
    Plot a Doppler spectrum in a clean and readable way.

    Parameters
    ----------
    frequencies_shifted : array-like
        Frequency axis in Hz.
    db_spectrum : array-like
        Spectrum magnitude in dB.
    doppler_frequency : float
        Detected Doppler frequency in Hz.
    x_label : str
        Label for x-axis.
    y_label : str
        Label for y-axis.
    title : str
        Plot title.
    show_peak : bool
        If True, mark the detected Doppler peak with a point.
    show_peak_line : bool
        If True, draw a vertical line at the Doppler frequency.
    focus_on_peak : bool
        If True, zoom around the Doppler peak.
    x_padding_factor : float
        Width multiplier for x-axis zoom around the Doppler frequency.
    y_padding_db : float
        Extra padding added above and below the plotted dB range.
    y_padding_mag : float
        Extra padding added above and below the plotted magnitude range
    """
    frequencies_shifted = np.asarray(frequencies_shifted, dtype=float)
    db_spectrum = np.asarray(db_spectrum, dtype=float)

    if frequencies_shifted.ndim != 1 or db_spectrum.ndim != 1:
        raise ValueError("frequencies_shifted and db_spectrum must be 1D arrays.")

    if len(frequencies_shifted) != len(db_spectrum):
        raise ValueError("frequencies_shifted and db_spectrum must have the same length.")

    if len(frequencies_shifted) == 0:
        raise ValueError("Input arrays must not be empty.")

    # Find nearest spectrum point to the provided Doppler frequency
    peak_index = int(np.argmin(np.abs(frequencies_shifted - doppler_frequency)))
    peak_frequency = frequencies_shifted[peak_index]
    peak_magnitude = db_spectrum[peak_index]

    # Create figure
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)

    # Main spectrum line
    ax.plot(
        frequencies_shifted,
        db_spectrum,
        linewidth=2.2,
        alpha=0.95,
        label="Doppler-spektrum",
    )

    # Highlight peak
    if show_peak:
        ax.plot(
            peak_frequency,
            peak_magnitude,
            marker="o",
            markersize=8,
            linestyle="None",
            label=f"Toppunkt: {peak_frequency:.1f} Hz",
        )

    # Vertical line at Doppler frequency
    if show_peak_line:
        ax.axvline(
            peak_frequency,
            linestyle=":",
            linewidth=1.8,
            alpha=0.9,
        )

    # Labels and title
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    ax.set_title(title, fontsize=18, pad=14)

    # Grid
    ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.45)
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.2)

    # Remove top and right spines for cleaner look
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Tick styling
    ax.tick_params(axis="both", labelsize=11)

    # X limits
    if focus_on_peak and doppler_frequency != 0:
        x_half_range = abs(doppler_frequency) * x_padding_factor

        # Avoid too tiny x-range if frequency is small
        if x_half_range < 50:
            x_half_range = 50

        ax.set_xlim(-x_half_range, x_half_range)
    else:
        ax.set_xlim(np.min(frequencies_shifted), np.max(frequencies_shifted))

    # Y limits with padding
    visible_mask = (
        (frequencies_shifted >= ax.get_xlim()[0]) &
        (frequencies_shifted <= ax.get_xlim()[1])
    )

    if np.any(visible_mask):
        if type == "db":
            visible_spectrum = db_spectrum[visible_mask]
            y_min = np.min(visible_spectrum) - y_padding_db
            y_max = np.max(visible_spectrum) + y_padding_db
            ax.set_ylim(y_min, y_max)
        if type == "linear":
            visible_spectrum = db_spectrum[visible_mask]
            y_min = np.min(visible_spectrum) - y_padding_mag
            y_max = np.max(visible_spectrum) + y_padding_mag
            ax.set_ylim(y_min, y_max)

    # Legend
    ax.legend(frameon=True, fontsize=11, loc="best")

    plt.tight_layout()
    plt.show()


def print_results(measurement_summaries, names, readings_per_speed, decimals):
    """
    Print averaged results for each tested speed.
    """
    print("Målte hastigheter:")

    for group_index, result in enumerate(measurement_summaries):
        name_index = group_index * readings_per_speed

        print(f"{names[name_index]}:")
        print(
            f"  Doppler-hastighet: {result['doppler_avg']:.{decimals}f} m/s "
            f"(std: {result['doppler_std']:.2f} m/s)"
        )
        print(
            f"  Timer-hastighet: {result['timer_avg']:.{decimals}f} m/s "
            f"(std: {result['timer_std']:.2f} m/s)"
        )
        print(
            f"  SNR: {result['snr_avg']:.{decimals}f} dB "
            f"(std: {result['snr_std']:.2f} dB)"
        )
        print(
            f"  Doppler-oppløsning: {result['resolution_avg']:.{decimals}f} Hz "
            f"(std: {result['resolution_std']:.2f} Hz)"
        )
        print()


def main():
    specifications = read_specifications_csv(SPECIFICATIONS_FILE)

    measurement_summaries = []

    for speed_index in range(SPEEDS_TESTED):
        doppler_speeds = []
        timer_speeds = []
        snr_values = []
        resolution_values = []

        for reading_index in range(READINGS_PER_SPEED):
            measurement_name = specifications["name"][speed_index * READINGS_PER_SPEED + reading_index]
            measurement_index = speed_index * READINGS_PER_SPEED + reading_index

            result = analyze_single_measurement(specifications, measurement_index)

            doppler_speeds.append(result["speed_doppler"])
            timer_speeds.append(result["speed_timer"])
            snr_values.append(result["snr_db"])
            resolution_values.append(result["resolution_3db_hz"])

            if speed_index * READINGS_PER_SPEED + reading_index == SPECTRUM_TO_PLOT_INDEX:
                plot_spectrum(
                    result["frequencies_shifted"],
                    result["spectrum"],
                    result["doppler_frequency"],
                    x_label="Frekvens [Hz]",
                    y_label="Magnitude [linear]",
                    title=f"Doppler-spektrum til måling {measurement_name}",
                    type="linear",
                    y_padding_mag = 10000

                )
                plot_spectrum(
                    result["frequencies_shifted"],
                    result["db_spectrum"],
                    result["doppler_frequency"],
                    x_label="Frekvens [Hz]",
                    y_label="Magnitude [dB]",
                    title=f"Doppler-spektrum til måling {measurement_name}",
                    y_padding_db = 5
                )

        doppler_avg, doppler_std = summarize_group(doppler_speeds)
        timer_avg, timer_std = summarize_group(timer_speeds)
        snr_avg, snr_std = summarize_group(snr_values)
        resolution_avg, resolution_std = summarize_group(resolution_values)

        measurement_summaries.append(
            {
                "doppler_avg": doppler_avg,
                "doppler_std": doppler_std,
                "timer_avg": timer_avg,
                "timer_std": timer_std,
                "snr_avg": snr_avg,
                "snr_std": snr_std,
                "resolution_avg": resolution_avg,
                "resolution_std": resolution_std,
            }
        )

    print_results(
        measurement_summaries,
        specifications["name"],
        READINGS_PER_SPEED,
        DECIMALS,
    )


if __name__ == "__main__":
    main()