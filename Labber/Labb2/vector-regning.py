import numpy as np
import matplotlib.pyplot as plt

from forsinkelse import finn_forsinkelse, finn_forsinkelse_med_oppampling
from generateSineSignal import sinus_med_pakke

# Parametere
frekvens = 50
fs = 4000
varighet = 1.0

# Velg forsinkelser du vil simulere (samples)
d21 = 10
d31 = 10
d32 = 0

c = 343  #m/s

# Tid
t = np.arange(0, varighet, 1 / fs)

# Tre signaler med forksjellige forsinkelser, kan byttes til ekte målinger
sig1 = sinus_med_pakke(t, frekvens, fs, d21) #Ingen forsinkelse
sig2 = sinus_med_pakke(t, frekvens, fs, d31) #Forsinkelse på d21 samples
sig3 = sinus_med_pakke(t, frekvens, fs, d32) #Forsinkelse på d31 samples

oppsamplet = False
oppsamplingsfaktor = 16

if not oppsamplet:
    #Heltalls samples
    m21, tau_21, r21, l21 = finn_forsinkelse(sig2, sig1, fs)
    m31, tau_31, r31, l31 = finn_forsinkelse(sig3, sig1, fs) 
    m32, tau_32, r32, l32 = finn_forsinkelse(sig3, sig2, fs)
else:
    #Med oppsampling
    m21, tau_21, r21, l21 = finn_forsinkelse_med_oppampling(sig2, sig1, fs, L=oppsamplingsfaktor, vindu=40)
    m31, tau_31, r31, l31 = finn_forsinkelse_med_oppampling(sig3, sig1, fs, L=oppsamplingsfaktor, vindu=40)
    m32, tau_32, r32, l32 = finn_forsinkelse_med_oppampling(sig3, sig2, fs, L=oppsamplingsfaktor, vindu=40)

plotPulse = False
if plotPulse:
    plt.figure()
    plt.plot(t, sig1, label="sig1 (0 samples)")
    plt.plot(t, sig2, label=f"sig2 ({d31} samples)", alpha=0.7)
    plt.plot(t, sig3, label=f"sig3 ({d32} samples)", alpha=0.7)
    plt.xlim(0.465, 0.535)
    plt.title("Tre signaler med kjent forsinkelse")
    plt.xlabel("Tid [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.show()

tau_ij = [tau_21, tau_31, tau_32]
n_ij = [tau/fs for tau in tau_ij]

p1 = np.array([0.0, 0.0, 0.0])
p2 = np.array([0.2, 0.0, 0.0])
p3 = np.array([0.1, 0.1732, 0.0])

# Vektorer mellom sensorer: x_ji = p_j - p_i
x_21 = p2 - p1
x_31 = p3 - p1
x_32 = p3 - p2

x_ij = [x_21, x_31, x_32]

for i in range(3):
    tau = tau_ij[i]
    print(f"Tau = {tau}")

#Finne vinklene (Bruker vi ikke posisjonene??)
teller = (n_ij[1] + n_ij[0])
nevner = (n_ij[1] - n_ij[0] + 2*n_ij[2])

if nevner == 0:
    print("Warning: nevner er null, kan ikke beregne vinkel theta.")
    theta_deg = None
else:
    theta_rad = np.atan(np.sqrt(3) * (teller/nevner))
    if nevner < 0:
        theta_rad += np.pi #Legger til 180 grader hvis nevner er negativ
    
    theta_deg = np.degrees(theta_rad)
    print(f"Vinkel theta: {theta_deg:.2f}\u00b0")

