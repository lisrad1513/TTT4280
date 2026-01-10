import numpy as np

#Oppgave 1
maalinger = [20.6, 20.4, 20.4, 20.6, 20.4, 20.8, 20.5, 20.5, 20.5, 20.4, 20.5, 20.5, 20.5, 20.5, 20.4, 20.4, 20.4, 20.5, 20.3, 20.6]
n = len(maalinger)

#Oppgave 1 a) Standardavvik
sigma = np.std(maalinger)
print(f"Standardavvik: {round(sigma, 3)}")

#Oppgave 1 b) 95% konfidensintervall
x_bar = np.mean(maalinger)
z = 1.96 #95%
s = sigma

CI_plus = x_bar + (z * (s / np.sqrt(n)))
CI_minus = x_bar - (z * (s / np.sqrt(n)))

print(f"95% konfidensintervall: [{round(CI_minus, 3)}, {round(CI_plus, 3)}]")

#Oppgave 1 c) 95% Prediksjonsintervall
m_T = x_bar
s_T = sigma
t_p = 2.093 #Fra tabell, n = 20, p = 0.975

PI_plus = m_T + (t_p * s_T * np.sqrt(1 + (1 / n)))
PI_minus = m_T - (t_p * s_T * np.sqrt(1 + (1 / n)))

print(f"95% prediksjonsintervall: [{round(PI_minus, 3)}, {round(PI_plus, 3)}]")

