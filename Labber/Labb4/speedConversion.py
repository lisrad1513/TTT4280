import numpy as np

def convert_doppler_shift_to_speed(f_D, wavelength, c, f_0):
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
    print(f"Doppler shift: {f_D:.2f} Hz")
    print(f"Wavelength: {wavelength:.2e} m")
    print(f"Speed of light: {c:.2e} m/s")
    print(f"Radar frequency: {f_0:.2e} Hz")

    speed = (f_D * c) / (2 * f_0)

    return speed
