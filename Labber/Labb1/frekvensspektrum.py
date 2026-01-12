import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple


def next_pow2(n: int) -> int:
    """Next power of 2 >= n."""
    n = int(n)
    if n <= 1:
        return 1
    return 1 << (n - 1).bit_length()


def get_window(name: str, n: int) -> np.ndarray:
    """
    Return a window of length n using only numpy.
    Supported: "rect", "hann", "hamming", "blackman"
    """
    name = (name or "rect").lower()
    if name in ["rect", "rectangular", "none"]:
        return np.ones(n)

    if n == 1:
        return np.ones(1)

    i = np.arange(n)

    if name == "hann":
        return 0.5 - 0.5 * np.cos(2.0 * np.pi * i / (n - 1))
    if name == "hamming":
        return 0.54 - 0.46 * np.cos(2.0 * np.pi * i / (n - 1))
    if name == "blackman":
        return (
            0.42
            - 0.5 * np.cos(2.0 * np.pi * i / (n - 1))
            + 0.08 * np.cos(4.0 * np.pi * i / (n - 1))
        )

    raise ValueError("Unknown window '{}'. Use rect, hann, hamming, or blackman.".format(name))


def quantize_adc(x: np.ndarray, bits: int, full_scale: float = 1.0) -> np.ndarray:
    """
    Simple uniform quantizer to emulate an ADC.

    Input range assumed: [-full_scale, +full_scale]
    Step: q = 2*full_scale / (2^bits)
    """
    bits = int(bits)
    if bits <= 0:
        raise ValueError("bits must be a positive integer")

    x_clip = np.clip(x, -full_scale, full_scale)
    levels = 2 ** bits
    q = 2.0 * full_scale / levels
    return q * np.round(x_clip / q)


def simulate_data(
    n: int,
    fs: float,
    f0: float = 1000.0,
    amplitude: float = 0.8,
    noise_std: float = 0.02,
    phase: float = 0.0,
    dc: float = 0.0,
    adc_bits: Optional[int] = None,
    full_scale: float = 1.0,
    rng_seed: Optional[int] = None,
) -> np.ndarray:
    """
    Return an array of length n with a known sine + random noise.
    Optionally quantize to emulate ADC bit depth.
    """
    n = int(n)
    fs = float(fs)
    t = np.arange(n) / fs

    rng = np.random.default_rng(rng_seed)
    noise = rng.normal(loc=0.0, scale=noise_std, size=n)

    x = dc + amplitude * np.sin(2.0 * np.pi * f0 * t + phase) + noise

    if adc_bits is not None:
        x = quantize_adc(x, bits=adc_bits, full_scale=full_scale)

    return x


def one_sided_fft_spectrum(
    x: np.ndarray,
    fs: float,
    window: str = "hann",
    nfft: Optional[int] = None,
    pad_factor: float = 1.0,
    use_next_pow2: bool = False,
    to_db: bool = True,
    db_ref: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute a one-sided amplitude spectrum using rFFT.

    Returns:
    f (Hz), mag (linear amplitude or dB re db_ref)
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    fs = float(fs)

    w = get_window(window, n)
    xw = x * w

    if nfft is None:
        nfft_candidate = int(np.ceil(n * float(pad_factor)))
        if use_next_pow2:
            nfft_candidate = next_pow2(nfft_candidate)
        nfft = max(nfft_candidate, n)

    X = np.fft.rfft(xw, n=nfft)
    f = np.fft.rfftfreq(nfft, d=1.0 / fs)

    sw = np.sum(w)

    mag = (2.0 / sw) * np.abs(X)

    mag[0] = (1.0 / sw) * np.abs(X[0])
    if (nfft % 2) == 0:
        mag[-1] = (1.0 / sw) * np.abs(X[-1])

    if to_db:
        eps = 1e-20
        mag_db = 20.0 * np.log10(np.maximum(mag, eps) / float(db_ref))
        return f, mag_db

    return f, mag


def main():
    fs = 48000.0
    n = 4096
    f0 = 3000.0

    x = simulate_data(
        n=n,
        fs=fs,
        f0=f0,
        amplitude=0.8,
        noise_std=0.02,
        phase=0.3,
        dc=0.0,
        adc_bits=None,
        full_scale=1.0,
        rng_seed=1,
    )

    window = "hann"
    pad_factor = 4.0
    use_next_pow2 = False

    f, mag_db = one_sided_fft_spectrum(
        x,
        fs=fs,
        window=window,
        pad_factor=pad_factor,
        use_next_pow2=use_next_pow2,
        to_db=True,
        db_ref=1.0,
    )

    plt.figure()
    plt.plot(f, mag_db)
    plt.title("One-sided FFT spectrum (window={}, pad_factor={})".format(window, pad_factor))
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude [dB re 1.0]")
    plt.grid(True)

    plt.axvline(f0, linestyle="--")
    plt.text(f0, np.max(mag_db) - 10, "f0", rotation=90, va="top")

    plt.xlim(0, fs / 2.0)
    plt.show()


if __name__ == "__main__":
    main()
