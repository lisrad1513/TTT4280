"""
Noise comparison: PCB (kretskortTest-utenPaadrag, CH3) vs breadboard (ADC-3.csv)
All measurements are without driving signal ("uten pådrag").

PCB CH1 and CH2 were unconnected during this recording (std < 1 LSB).
Only CH3 (PCB column 2 vs ADC-3.csv) is compared.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from raspi_import import raspi_import

# -----------------------------
# Settings
# -----------------------------
VREF       = 3.3
RESOLUTION = (2**12) - 1    # 12-bit ADC
SKIP       = 5               # startup samples to drop from PCB binary file
PCB_CH_IDX = 2               # column index in the PCB binary file for CH3
V_FS_PEAK  = VREF / 2.0     # 0 dBFS reference — same as compare_pcb_vs_breadboard.py

HERE     = Path(__file__).resolve().parent
PCB_PATH = HERE / "kretskortTest-utenPaadrag"
CSV_PATH = HERE.parent / "Støy" / "ADC-3.csv"

LABEL_BB  = "Breadboard (ADC-3.csv)"
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
    cg  = np.sum(win) / N
    amp = np.abs(X) / (N * cg)
    amp[1:-1] *= 2
    db  = 20.0 * np.log10(np.maximum(amp, 1e-15) / V_FS_PEAK)
    return np.fft.rfftfreq(N, d=1.0/fs), db

def psd(signal_v, fs):
    """One-sided PSD in V²/Hz (Hanning-windowed)."""
    N   = len(signal_v)
    win = np.hanning(N)
    X   = np.fft.rfft(signal_v * win)
    w2  = np.sum(win ** 2)
    P   = (np.abs(X) ** 2) / (fs * w2)
    P[1:-1] *= 2
    return np.fft.rfftfreq(N, d=1.0/fs), P

def snr_fullscale_db(noise_rms_v):
    """SNR re. full-scale sine RMS = VREF/(2√2). Also returns ENOB."""
    v_fs_rms = VREF / (2.0 * np.sqrt(2.0))
    snr  = 20.0 * np.log10(v_fs_rms / noise_rms_v)
    enob = (snr - 1.76) / 6.02
    return snr, enob

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
sp_pcb, data_pcb = raspi_import(str(PCB_PATH), PCB_CH_IDX + 1)
v_pcb_raw = counts_to_volts(data_pcb)[SKIP:, PCB_CH_IDX]
fs_pcb    = 1.0 / sp_pcb
v_pcb     = v_pcb_raw - v_pcb_raw.mean()

d3    = np.genfromtxt(str(CSV_PATH), delimiter=',', skip_header=1)
t3    = d3[:, 0]
v_bb  = d3[:, 1] - d3[:, 1].mean()
fs_bb = 1.0 / float(np.mean(np.diff(t3)))

# ------------------------------------------------------------------
# Numerical comparison
# ------------------------------------------------------------------
bb_rms,  pcb_rms  = np.std(v_bb),  np.std(v_pcb)
bb_snr,  bb_enob  = snr_fullscale_db(bb_rms)
pcb_snr, pcb_enob = snr_fullscale_db(pcb_rms)

bb_nf_dbfs  = 20.0 * np.log10(bb_rms  / V_FS_PEAK)
pcb_nf_dbfs = 20.0 * np.log10(pcb_rms / V_FS_PEAK)

def median_noise_floor_dbfs(signal_v, fs):
    """Median of the one-sided dBFS spectrum (robust to spikes)."""
    _, db = fft_dbfs(signal_v, fs)
    return float(np.median(db[1:]))  # skip DC bin

bb_nf_median_dbfs  = median_noise_floor_dbfs(v_bb,  fs_bb)
pcb_nf_median_dbfs = median_noise_floor_dbfs(v_pcb, fs_pcb)

print("=" * 65)
print(f"  NOISE COMPARISON — CH3, uten pådrag")
print(f"  (0 dBFS = VREF/2 = {V_FS_PEAK:.2f} V — same ref as signal file)")
print("=" * 65)
print(f"\n{'Source':<25} {'fs (Hz)':>10} {'N samples':>12}")
print("-" * 50)
print(f"{'Breadboard (CSV)':<25} {fs_bb:>10.1f} {len(v_bb):>12}")
print(f"{'PCB (raspi binary)':<25} {fs_pcb:>10.1f} {len(v_pcb):>12}")

print(f"""
{'Metric':<22} {'Breadboard':>12} {'PCB':>12} {'Δ (PCB−BB)':>12}
{'-'*60}
{'RMS noise (mV)':<22} {bb_rms*1e3:>12.3f} {pcb_rms*1e3:>12.3f} {(pcb_rms-bb_rms)*1e3:>+12.3f}
{'Noise floor (dBFS)':<22} {bb_nf_dbfs:>12.1f} {pcb_nf_dbfs:>12.1f} {pcb_nf_dbfs-bb_nf_dbfs:>+12.1f}
{'SNR (dB)':<22} {bb_snr:>12.2f} {pcb_snr:>12.2f} {pcb_snr-bb_snr:>+12.2f}
{'ENOB (bits)':<22} {bb_enob:>12.2f} {pcb_enob:>12.2f} {pcb_enob-bb_enob:>+12.2f}
""")
print("SNR  = 20·log10(V_fs_rms / noise_rms),  V_fs_rms = VREF/(2√2)")
print("ENOB = (SNR − 1.76) / 6.02")
print("⚠  BB fs ≪ PCB fs — BB misses high-freq noise. PSD gives fairer comparison.")
print("=" * 65)

# ------------------------------------------------------------------
# Styling
# ------------------------------------------------------------------
plt.close("all")
plt.rcParams.update({
    "figure.dpi": 140, "axes.titlesize": 11, "axes.labelsize": 11,
    "font.size": 10, "lines.linewidth": 1.2, "grid.alpha": 0.25,
    "grid.linestyle": ":", "legend.frameon": True,
    "legend.framealpha": 0.9, "legend.fontsize": 9,
})

TSHOW_S = 0.05
t_bb_plot  = np.arange(len(v_bb))  / fs_bb
t_pcb_plot = np.arange(len(v_pcb)) / fs_pcb

# ============================================================
# FIGURE 1 — Time domain
# ============================================================
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(t_bb_plot [t_bb_plot  <= TSHOW_S] * 1e3,
         v_bb      [t_bb_plot  <= TSHOW_S] * 1e3,
         color=COLOR_BB,  alpha=0.85, label=LABEL_BB,  lw=1.0)
ax1.plot(t_pcb_plot[t_pcb_plot <= TSHOW_S] * 1e3,
         v_pcb     [t_pcb_plot <= TSHOW_S] * 1e3,
         color=COLOR_PCB, alpha=0.85, label=LABEL_PCB, lw=1.0)
ax1.axhline(0, color="gray", lw=0.8, alpha=0.4, ls=":")
ax1.set_xlabel("Tid [ms]"); ax1.set_ylabel("Støy [mV]")
ax1.set_title(f"CH3 — Tidsdomene (første {TSHOW_S*1e3:.0f} ms, uten pådrag)")
ax1.legend(); ax1.grid(True)
fig1.tight_layout()

# ============================================================
# FIGURE 2 — dBFS FFT  (main comparison — same reference as signal file)
# ============================================================
fig2, ax2 = plt.subplots(figsize=(10, 5))

f_bb,  db_bb  = fft_dbfs(v_bb,  fs_bb)
f_pcb, db_pcb = fft_dbfs(v_pcb, fs_pcb)

ax2.plot(f_bb[1:],  db_bb[1:],  color=COLOR_BB,  alpha=0.85,
         label=f"{LABEL_BB} (fs={fs_bb:.0f} Hz)",  lw=1.1)
ax2.plot(f_pcb[1:], db_pcb[1:], color=COLOR_PCB, alpha=0.85,
         label=f"{LABEL_PCB} (fs={fs_pcb:.0f} Hz)", lw=1.1)

# Noise floor lines (median of FFT bins — robust to spikes)
ax2.axhline(bb_nf_median_dbfs,  color=COLOR_BB,  lw=1.2, ls=":", alpha=0.8,
            label=f"BB støygulv (median): {bb_nf_median_dbfs:.1f} dBFS")
ax2.axhline(pcb_nf_median_dbfs, color=COLOR_PCB, lw=1.2, ls=":", alpha=0.8,
            label=f"PCB støygulv (median): {pcb_nf_median_dbfs:.1f} dBFS")

# SNR annotation
ax2.text(0.99, 0.04,
         f"SNR — {LABEL_BB}: {bb_snr:.1f} dB  |  {LABEL_PCB}: {pcb_snr:.1f} dB",
         transform=ax2.transAxes, va="bottom", ha="right", fontsize=9,
         bbox=dict(boxstyle="round,pad=0.3", alpha=0.15, lw=0.5))

ax2.set_xlim(0, 2000)
ax2.set_xlabel("Frekvens [Hz]"); ax2.set_ylabel("Amplitude [dBFS]")
ax2.set_title(f"CH3 — dBFS FFT, uten pådrag  (0 dBFS = {V_FS_PEAK:.2f} V = VREF/2)\n"
              f"Prikkede linjer = median støygulv (robust mot støytopper)")
ax2.legend(loc="upper right"); ax2.grid(True, which="both")
fig2.tight_layout()

# ============================================================
# FIGURE 3 — RMS noise + SNR bar chart
# ============================================================
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(9, 4))

x, w     = np.array([0, 1]), 0.5
xlabels  = ["Breadboard", "PCB"]
rms_vals = [bb_rms * 1e3, pcb_rms * 1e3]
snr_vals = [bb_snr, pcb_snr]

b1 = ax3a.bar(x, rms_vals, w, color=[COLOR_BB, COLOR_PCB], alpha=0.8)
ax3a.bar_label(b1, fmt="%.3f mV", padding=3, fontsize=9)
ax3a.set_xticks(x); ax3a.set_xticklabels(xlabels)
ax3a.set_ylabel("Støy RMS [mV]")
ax3a.set_title("Støy RMS  (lavere = bedre)\n⚠ ulik båndbredde — se ESD for rettferdig sammenligning")
ax3a.grid(True, axis="y", alpha=0.3)

b2 = ax3b.bar(x, snr_vals, w, color=[COLOR_BB, COLOR_PCB], alpha=0.8)
ax3b.bar_label(b2, fmt="%.1f dB", padding=3, fontsize=9)
ax3b.set_xticks(x); ax3b.set_xticklabels(xlabels)
ax3b.set_ylabel("SNR [dB]")
ax3b.set_title("SNR rel. full-skala  (høyere = bedre)\n"
               f"ENOB: BB={bb_enob:.2f} bit,  PCB={pcb_enob:.2f} bit")
ax3b.grid(True, axis="y", alpha=0.3)

# Subplot-etiketter
for ax, label in zip([ax3a, ax3b], ['(a)', '(b)']):
    ax.text(0.02, 0.97, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')

fig3.suptitle("CH3 — Breadboard vs PCB støysammenligning", fontsize=13)
fig3.tight_layout()

# ============================================================
# FIGURE 4 — PSD  (bandwidth-fair spectral comparison)
# ============================================================
fig4, ax4 = plt.subplots(figsize=(10, 4))

f_bb_p,  P_bb  = psd(v_bb,  fs_bb)
f_pcb_p, P_pcb = psd(v_pcb, fs_pcb)

ax4.semilogy(f_bb_p,  P_bb,  color=COLOR_BB,  alpha=0.85,
             label=f"{LABEL_BB} (fs={fs_bb:.0f} Hz)",  lw=1.1)
ax4.semilogy(f_pcb_p, P_pcb, color=COLOR_PCB, alpha=0.85,
             label=f"{LABEL_PCB} (fs={fs_pcb:.0f} Hz)", lw=1.1)
ax4.set_xlim(0, 2000)
ax4.set_xlabel("Frekvens [Hz]"); ax4.set_ylabel("ESD [V²/Hz]")
ax4.set_title("CH3 — Effektspektraltetthet  (båndbreddenormalisert V²/Hz)\n"
              "Rettferdig sammenligning: samme støygulvnivå betyr samme støytetthet")
ax4.legend(); ax4.grid(True, which="both")
fig4.tight_layout()

plt.show()
