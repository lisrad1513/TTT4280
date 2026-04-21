# kretskortTest

PCB validation for Lab 1 in ELSYSS6 (TTT4288/4280 – Sensors and Instrumentation).

A custom PCB was designed as an alternative to the breadboard prototype built earlier in the lab. These scripts load binary ADC recordings from the PCB and compare its performance against the breadboard baseline.

Data is captured by `adc_sampler.c` running on a Raspberry Pi and stored as raw binary files. The shared `raspi_import.py` utility (in the parent directory) handles loading them.

---

## Files

### Python scripts

| File | Description |
|------|-------------|
| [`ADC-testDataPent.py`](ADC-testDataPent.py) | Simple visualization of the PCB's 1 kHz recording. Plots voltage vs. time for all 3 channels over 10 periods. |
| [`compare_pcb_vs_breadboard.py`](compare_pcb_vs_breadboard.py) | Compares PCB and breadboard performance with a 1 kHz sine wave input. Produces time-domain overlay, dBFS FFT, and SNR bar charts for all 3 channels. |
| [`compare_noise_pcb_vs_bb.py`](compare_noise_pcb_vs_bb.py) | Compares noise floors of both implementations with no signal applied. Produces time-domain noise traces, FFT spectrum, RMS/SNR bar charts, and power spectral density plots. Also calculates ENOB. |

### Data files

| File | Description |
|------|-------------|
| [`kretskortTest-1kHz`](kretskortTest-1kHz) | Raw binary ADC recording from the PCB with a 1 kHz sine wave applied. ~31 250 samples across 3 channels. |
| [`kretskortTest-utenPaadrag`](kretskortTest-utenPaadrag) | Raw binary ADC recording from the PCB with no input signal ("uten pådrag"). Used for noise floor characterisation. |

---

## Data format

Binary files are written by `adc_sampler.c` on the Raspberry Pi:

- **First 8 bytes:** sample period as a `double` (microseconds)
- **Remaining bytes:** `uint16` ADC counts, interleaved across 3 channels, reshaped to `(N_samples, 3)`

The `raspi_import(path, channels=3)` function in the parent directory handles this format.
