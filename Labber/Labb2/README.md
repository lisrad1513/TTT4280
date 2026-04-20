# Labb 2 - TTT4280 Sensorer og instrumentering

Hello! This is Labb 2 for the subject TTT4280. Below is a description of relevant files and where they are placed.

---

## Root-level scripts

| File | Description |
|------|-------------|
| `generateSineSignal.py` | Generates synthetic sine wave signals for testing |
| `finnForsinkelse.py` | Finds/calculates signal delay and phase shift between sensors |
| `ekteSignalRegning.py` | Processes and calculates from real recorded signals |
| `vectorRegning.py` | Vector math utilities used in angle estimation |
| `raspi_import.py` | Utilities for importing data recorded with Raspberry Pi |

---

## `endeligLabb2Filer/` — Final lab scripts

The main scripts used for the final lab submission.

| File | Description |
|------|-------------|
| `forberedelse1.py` | Preparation task 1 — signal analysis and setup |
| `forberedelse2.py` | Preparation task 2 — further signal processing |
| `laboppgave_2_3_4.py` | Solutions to lab tasks 2, 3, and 4 |
| `laboppgave_5.py` | Solution to lab task 5 |
| `krysskorrelasjon_demo.py` | Demonstration of cross-correlation between microphone channels |
| `krysskorrelasjon_visualisering.py` | Visualization of cross-correlation results |
| `polar_visualisering.py` | Polar plot showing estimated sound source direction |

---

## `endeligLabb2Maalinger/` — Final lab measurements

Measurement data used for the final submission.

- `konsekventTesting/` — 12 binary recordings at three angles: +60°, -60°, and -120°
- `test/` — Early test recordings

---

## `Maalinger/` — Older measurements

Earlier measurement sets from development and testing.

- `KonsekventTesting/` — Chirp recordings at three fixed positions (5 recordings each)
- `MinusTilPluss/` — Chirp and clap recordings sweeping from negative to positive angles
- `Gamle målinger/` — Archive of legacy recordings (clap, snap, 500 Hz / 1 kHz sine signals)

---

## Documentation

| File | Description |
|------|-------------|
| `TTT4280_Sensors_and_instrumentation___lab (7).pdf` | Official lab assignment specification |
