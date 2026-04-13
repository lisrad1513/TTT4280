import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

# -----------------------------
# Settings
# -----------------------------
CHANNELS    = 3
FREQ_IN     = 1000           # Hz
PERIODS     = 10
VREF        = 3.3
RESOLUTION  = (2**12) - 1   # 12-bit ADC
N_HARMONICS = 5
SKIP        = 5
V_FS_PEAK   = VREF / 2.0    # 0 dBFS reference (full-scale peak amplitude)

HERE     = Path(__file__).resolve().parent
PCB_PATH = HERE / "kretskortTest-1kHz"
BB_PATH  = HERE.parent / "1000Hz" / "31250Samples1_65VOffset1_65V1000Hz"

LABEL_BB  = "Breadboard"
LABEL_PCB = "PCB (kretskort)"
COLOR_BB  = "steelblue"
COLOR_PCB = "tomato"

def counts_to_volts(counts):
    return (counts / RESOLUTION) * VREF

# ------------------------------------------------------------------
# Analysis helpers
# ------------------------------------------------------------------
def fft_dbfs(signal_v, fs):
    """One-sided FFT amplitude in dBFS.  0 dBFS = V_FS_PEAK = VREF/2."""
    N   = len(signal_v)
    win = np.hanning(N)
    X   = np.fft.rfft(signal_v * win)
    cg  = np.sum(win) / N          # coherent gain of Hanning ≈ 0.5
    amp = np.abs(X) / (N * cg)
    amp[1:-1] *= 2                 # one-sided
    freqs = np.fft.rfftfreq(N, d=1.0/fs)
    db  = 20.0 * np.log10(np.maximum(amp, 1e-15) / V_FS_PEAK)
    return freqs, db

def noise_floor_snr_db(signal_v, fs, f_signal, bw_bins=3):
    """Signal power / broadband noise power (harmonics excluded). Returns dB."""
    N   = len(signal_v)
    win = np.hanning(N)
    X   = np.fft.rfft(signal_v * win)
    P   = np.abs(X) ** 2 / N
    freqs = np.fft.rfftfreq(N, d=1.0/fs)

    harmonic_mask = np.zeros(len(P), dtype=bool)
    for h in range(1, N_HARMONICS + 1):
        fh = h * f_signal
        if fh > fs / 2: break
        kh = int(round(fh * N / fs))
        harmonic_mask[max(1, kh-bw_bins):min(len(P)-1, kh+bw_bins)+1] = True

    k0 = int(round(f_signal * N / fs))
    sig_mask = np.zeros(len(P), dtype=bool)
    sig_mask[max(1, k0-bw_bins):min(len(P)-1, k0+bw_bins)+1] = True

    sig_power   = P[sig_mask].sum()
    noise_power = P[~harmonic_mask & (freqs > 0)].sum()
    return 10.0 * np.log10(sig_power / noise_power) if noise_power else np.inf

def residual_noise_rms(signal_v, fs, f_signal):
    """RMS (V) after subtracting DC + all harmonics up to Nyquist."""
    N    = len(signal_v)
    t    = np.arange(N) / fs
    X    = np.fft.rfft(signal_v)
    recon = np.full(N, np.mean(signal_v))
    for h in range(1, N_HARMONICS + 1):
        fh = h * f_signal
        if fh >= fs / 2: break
        kh  = int(round(fh * N / fs))
        A   = 2.0 * np.abs(X[kh]) / N
        phi = np.angle(X[kh]) + np.pi / 2
        recon += A * np.sin(2 * np.pi * fh * t + phi)
    return float(np.std(signal_v - recon))

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
sp_bb,  data_bb  = raspi_import(str(BB_PATH),  CHANNELS)
sp_pcb, data_pcb = raspi_import(str(PCB_PATH), CHANNELS)

v_bb  = counts_to_volts(data_bb) [SKIP:]
v_pcb = counts_to_volts(data_pcb)[SKIP:]

fs_bb  = 1.0 / sp_bb
fs_pcb = 1.0 / sp_pcb

t_bb  = np.arange(v_bb.shape[0])  * sp_bb
t_pcb = np.arange(v_pcb.shape[0]) * sp_pcb
mask_bb  = t_bb  <= PERIODS / FREQ_IN
mask_pcb = t_pcb <= PERIODS / FREQ_IN

# ------------------------------------------------------------------
# Numerical comparison
# ------------------------------------------------------------------
print("=" * 70)
print(f"  COMPARISON  —  {FREQ_IN} Hz input signal  (0 dBFS = VREF/2 = {V_FS_PEAK:.2f} V)")
print("=" * 70)
print(f"\n{'Dataset':<20} {'fs (Hz)':>10} {'N samples':>12}")
print("-" * 45)
print(f"{'Breadboard':<20} {fs_bb:>10.1f} {v_bb.shape[0]:>12}")
print(f"{'PCB':<20} {fs_pcb:>10.1f} {v_pcb.shape[0]:>12}")

print(f"\n{'CH':<5} {'BB fund (V)':>12} {'PCB fund (V)':>13} "
      f"{'BB noise (mV)':>14} {'PCB noise (mV)':>15} "
      f"{'BB SNR (dB)':>12} {'PCB SNR (dB)':>13} {'ΔSNR (dB)':>10}")
print("-" * 97)

for ch in range(CHANNELS):
    bb_v,  pcb_v = v_bb[:, ch], v_pcb[:, ch]

    def fundamental_amp(v, fs):
        X  = np.fft.rfft(v)
        k0 = int(round(FREQ_IN * len(v) / fs))
        return 2.0 * np.abs(X[k0]) / len(v)

    bb_fund  = fundamental_amp(bb_v,  fs_bb)
    pcb_fund = fundamental_amp(pcb_v, fs_pcb)
    bb_noise  = residual_noise_rms(bb_v,  fs_bb,  FREQ_IN) * 1e3
    pcb_noise = residual_noise_rms(pcb_v, fs_pcb, FREQ_IN) * 1e3
    bb_snr    = noise_floor_snr_db(bb_v,  fs_bb,  FREQ_IN)
    pcb_snr   = noise_floor_snr_db(pcb_v, fs_pcb, FREQ_IN)
    d_snr     = pcb_snr - bb_snr

    print(f"  CH{ch+1}  {bb_fund:>12.4f} {pcb_fund:>13.4f} "
          f"{bb_noise:>14.3f} {pcb_noise:>15.3f} "
          f"{bb_snr:>12.2f} {pcb_snr:>13.2f} {d_snr:>+10.2f}")

print("=" * 70)
print("\nSNR = signal power / broadband noise power (harmonics excluded).")
print("Positive ΔSNR = PCB is better.\n")

# ------------------------------------------------------------------
# Styling
# ------------------------------------------------------------------
plt.close("all")
plt.rcParams.update({
    "figure.dpi": 140, "axes.titlesize": 11, "axes.labelsize": 11,
    "font.size": 10, "lines.linewidth": 1.3, "grid.alpha": 0.25,
    "grid.linestyle": ":", "legend.frameon": True,
    "legend.framealpha": 0.9, "legend.fontsize": 9,
})

CH_LABELS = [f"CH{i+1}" for i in range(CHANNELS)]

# ============================================================
# FIGURE 1 — Time domain
# ============================================================
fig1, axs1 = plt.subplots(CHANNELS, 1, figsize=(10, 7))
for ch in range(CHANNELS):
    ax = axs1[ch]
    ax.plot(t_bb [mask_bb]  * 1e3, v_bb [mask_bb,  ch],
            color=COLOR_BB,  alpha=0.75, label=LABEL_BB,  lw=1.2)
    ax.plot(t_pcb[mask_pcb] * 1e3, v_pcb[mask_pcb, ch],
            color=COLOR_PCB, alpha=0.85, label=LABEL_PCB, lw=1.2)
    ax.axhline(VREF/2, ls="--", lw=1.0, alpha=0.3, color="gray")
    ax.set_ylabel("Spenning [V]"); ax.set_ylim(-0.1, 3.4)
    ax.set_title(f"{CH_LABELS[ch]} — Tidsdomene ({PERIODS} perioder @ {FREQ_IN} Hz)")
    ax.legend(loc="upper right"); ax.grid(True)
axs1[-1].set_xlabel("Tid [ms]")
fig1.suptitle("Tidsdomene: Breadboard vs PCB", fontsize=13, y=0.995)
fig1.tight_layout()

# ============================================================
# FIGURE 2 — dBFS FFT  (the main comparison figure)
# ============================================================
fig2, axs2 = plt.subplots(CHANNELS, 1, sharex=True, figsize=(10, 8))
FMAX_PLOT = 5000   # Hz — shows fundamental + first 4 harmonics

for ch in range(CHANNELS):
    ax = axs2[ch]
    bb_v,  pcb_v = v_bb[:, ch], v_pcb[:, ch]

    f_bb,  db_bb  = fft_dbfs(bb_v,  fs_bb)
    f_pcb, db_pcb = fft_dbfs(pcb_v, fs_pcb)

    ax.plot(f_bb,  db_bb,  color=COLOR_BB,  alpha=0.85, label=LABEL_BB,  lw=1.1)
    ax.plot(f_pcb, db_pcb, color=COLOR_PCB, alpha=0.85, label=LABEL_PCB, lw=1.1)

    # Noise floor lines (median of FFT bins — robust to spikes/harmonics)
    for v, fs, color in [
        (bb_v,  fs_bb,  COLOR_BB),
        (pcb_v, fs_pcb, COLOR_PCB),
    ]:
        _, db  = fft_dbfs(v, fs)
        nf_dbfs = float(np.median(db[1:]))
        ax.axhline(nf_dbfs, color=color, lw=1.0, ls=":", alpha=0.7)

    # Harmonic markers
    for h in range(1, N_HARMONICS + 1):
        fh = h * FREQ_IN
        if fh > FMAX_PLOT: break
        ax.axvline(fh, lw=0.8, alpha=0.25, color="gray", ls="--")

    # SNR annotation box
    bb_snr  = noise_floor_snr_db(bb_v,  fs_bb,  FREQ_IN)
    pcb_snr = noise_floor_snr_db(pcb_v, fs_pcb, FREQ_IN)
    ax.text(0.99, 0.04,
            f"SNR — {LABEL_BB}: {bb_snr:.1f} dB  |  {LABEL_PCB}: {pcb_snr:.1f} dB",
            transform=ax.transAxes, va="bottom", ha="right", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", alpha=0.15, lw=0.5))

    ax.set_ylabel("Amplitude [dBFS]")
    ax.set_title(f"{CH_LABELS[ch]} — FFT  (prikkede linjer = median støygulv)")
    ax.set_ylim(-140, 5)
    ax.legend(loc="upper right"); ax.grid(True, which="both")

axs2[-1].set_xlabel("Frekvens [Hz]")
axs2[0].set_xlim(0, FMAX_PLOT)
fig2.suptitle(f"dBFS FFT: Breadboard vs PCB  —  0 dBFS = {V_FS_PEAK:.2f} V (VREF/2)",
              fontsize=13, y=0.995)
fig2.tight_layout()

# ============================================================
# FIGURE 3 — SNR bar chart
# ============================================================
fig3, ax3 = plt.subplots(figsize=(7, 4))

snr_bb_vals  = [noise_floor_snr_db(v_bb[:,  ch], fs_bb,  FREQ_IN) for ch in range(CHANNELS)]
snr_pcb_vals = [noise_floor_snr_db(v_pcb[:, ch], fs_pcb, FREQ_IN) for ch in range(CHANNELS)]

x, w = np.arange(CHANNELS), 0.35
b1 = ax3.bar(x - w/2, snr_bb_vals,  w, label=LABEL_BB,  color=COLOR_BB,  alpha=0.8)
b2 = ax3.bar(x + w/2, snr_pcb_vals, w, label=LABEL_PCB, color=COLOR_PCB, alpha=0.8)
ax3.bar_label(b1, fmt="%.1f dB", padding=3, fontsize=9)
ax3.bar_label(b2, fmt="%.1f dB", padding=3, fontsize=9)
ax3.set_xticks(x); ax3.set_xticklabels(CH_LABELS)
ax3.set_ylabel("SNR [dB]")
ax3.set_title(f"Støygulv-SNR @ {FREQ_IN} Hz  (høyere = bedre)\n"
              f"Signal / bredbånds støy, {N_HARMONICS} harmoniske ekskludert")
ax3.legend(); ax3.grid(True, axis="y", alpha=0.3)
fig3.tight_layout()

plt.show()
