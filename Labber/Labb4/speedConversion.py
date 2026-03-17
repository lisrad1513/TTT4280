import numpy as np

def convert_doppler_shift_to_speed(f_D, f_0):
    """
    Convert Doppler shift to speed.

    Args:
        f_D: Doppler shift in Hz
        wavelength: Wavelength of the radar signal in meters
        c: Speed of light in m/s
        f_0: Radar frequency in Hz

    Returns:
        Speed in m/s
    """
    c = 299792458  # Lysets hastighet i m/s

    speed = (f_D * c) / (2 * f_0)

    return speed

def convert_distance_and_time_to_speed(distance, time):
    """
    Convert distance and time to speed.

    Args:
        distance: Distance traveled in meters
        time: Time taken in seconds

    Returns:
        Speed in m/s
    """
    speed = distance / time if time != 0 else 0
    return speed